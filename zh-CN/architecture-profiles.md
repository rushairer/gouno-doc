# Gouno 架构 Profile

[English](../architecture-profiles.md)

Gouno Core 不强制应用架构。目录结构、依赖边界与 Codegen Policy 都属于 Project Template 和项目自身。

在官方 Gouno 生态中，推荐用两种参考 Profile 覆盖常见场景，同时避免把应用架构提升为 Core 行为：

- **Flat Layered**：适合较简单的应用；
- **Capability Module**：适合拥有多个复杂业务能力的应用。

它们是推荐的项目/Template 工程约定，不是协议要求。自定义 Template 可以在项目确有需要时采用其它架构。

## 1. Flat Layered

当应用业务域较少、全局 Layer 目录仍然容易理解和导航时，优先使用 **Flat Layered**。

典型结构：

```text
internal/
├── domain/
├── repository/
├── service/
└── controller/
```

它以实现 Layer 作为第一层组织方式，例如：

```text
internal/domain/user.go
internal/repository/user.go
internal/service/user.go
internal/controller/user.go
```

这个 Profile 强调低复杂度和清晰的 Layer 边界，适合小型 API、CRUD 服务、内部工具以及业务面仍然较紧凑的应用。

官方 [`gouno-template`](https://github.com/rushairer/gouno-template) 是该 Profile 的参考实现。它具体提供哪些 Generator 属于 Template Policy，不是 Gouno Core API。

### Codegen 约定

Flat Layered 项目可以提供：

```text
domain
repository
service
controller
suite
```

`Suite` 在默认 Template 中只是多个 Generator 的组合动作，它本身不定义一种架构，也不能被重新解释为 Capability Module Generator。

## 2. Capability Module

当应用包含多个较重业务能力、全局 Layer 目录开始变成巨大 ownership bucket，或者团队经常需要把一个业务能力作为整体理解时，优先采用 **Capability Module**。

典型结构：

```text
internal/
├── account/
│   ├── domain/
│   ├── repository/
│   ├── service/
│   └── controller/
├── article/
│   ├── domain/
│   ├── repository/
│   ├── service/
│   └── controller/
└── media/
    └── ...
```

Ownership 顺序是：

```text
Capability first
Layer second
```

即：

```text
internal/<capability>/<layer>/
```

Capability 只保留它实际需要的 Layer。基础设施、Adapter、可观测性、加密或测试支持包，不应为了目录对称而人为创建空的 `domain`、`repository`、`service`、`controller`。

`module.go` 或其它 composition root 也不是强制文件，只有真正需要显式依赖组装时才添加。

### 依赖方向

业务 Capability 内优先保持向内依赖：

```text
controller -> service -> repository
                |          |
                +-> domain <-+
```

跨 Capability 依赖应该面向窄而稳定的 API。不要为了共享业务逻辑，又把代码重新塞回全局 Layer bucket。

### Codegen 约定

Capability Module 项目可以定义独立的 Generator，例如：

```text
module
```

将基础骨架生成到 `internal/<capability>/`。

Generator 应保持克制。除非项目已经通过真实实践证明并明确纳入 Codegen Policy，否则不要自动生成数据库访问、Migration、Router、依赖注入、安全策略、跨 Capability import 或强制 `module.go`。

## 3. 如何选择

当下面大多数条件成立时，优先 **Flat Layered**：

- 业务域较少；
- 全局 Layer 目录仍然容易导航；
- 大多数需求只涉及少量 Layer 文件；
- 团队和业务 ownership 简单；
- Capability 目录带来的额外层级会比收益更大。

当下面大多数条件成立时，优先 **Capability Module**：

- 存在多个业务 Capability 或 bounded context；
- 全局 `service`、`repository`、`controller` 已经变成大型 ownership bucket；
- 一个需求通常同时涉及 Domain、Persistence、Service、HTTP 行为；
- 跨团队或跨业务域 ownership 需要清晰表达；
- 项目已经出现 capability-specific infrastructure 或 composition rule。

不要只因为文件数量达到某个阈值就切换 Profile。真正判断依据是 ownership clarity 和 dependency locality。

## 4. 迁移规则

Flat Layered 项目演进为 Capability Module 时，必须按完整 Capability Slice 渐进迁移：

1. 识别真实 Capability 及 ownership boundary；
2. 先把真正共享的基础设施与业务代码分离；
3. 将 canonical implementation 移入 `internal/<capability>/...`；
4. 如果一次切换所有消费者会扩大风险，保留窄的 compatibility facade；
5. 测试随 canonical implementation 一起迁移，避免 coverage 失真；
6. 再逐步切换消费者；
7. 只有当全局 Layer bucket 不再拥有真实业务代码时，才删除 legacy facade 和目录。

不要按文件名机械搬家。比如名为 `category_repository.go` 的文件可能同时承载多个职责，必须先拆 ownership，再决定所属 Capability。

## 5. 与 Gouno Core / Codegen 的关系

Architecture Profile 属于 Project Template / Project。

Gouno Core 只拥有可复用机制与 Codegen 协议/运行时，不应把 `Flat Layered`、`Capability Module`、`domain`、`repository`、`service`、`controller`、`suite`、`module` 变成强制应用概念。

项目存在 `.gouno/codegen.yaml` 时，它应表达项目当前真实架构。项目已经改变目录/ownership，而 Generator 仍向旧路径输出，应视为 architecture drift 和契约缺陷。

## 参考

- [Template 开发指南](./template-authoring.md)
- [代码生成](./code-generation.md)
- [官方默认 Flat Layered Template](https://github.com/rushairer/gouno-template)
- [Gouno Codegen Specification v1](https://github.com/rushairer/gouno/blob/main/docs/codegen-template-spec.md)
