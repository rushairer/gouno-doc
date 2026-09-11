# 项目模板

[English](../project-templates.md)

Gouno 的 **Project Template（项目模板）**是 `gouno-cli new` 使用的完整项目骨架。

Template 自己拥有项目结构和开发约定。它可以选择 Gin、Echo、Fiber、`net/http`、DDD、Clean Architecture、其它架构，甚至完全不采用固定分层。官方 [`gouno-template`](https://github.com/rushairer/gouno-template) 只是默认参考模板，不是所有 Gouno 项目的强制架构。

## 使用默认 Template

```bash
gouno-cli new my-service -m github.com/you/my-service
```

在通常的默认环境下，如果本地没有 `./templates` 目录，`gouno-cli` 会使用官方 Template。

## 使用自定义远程 Template

HTTPS：

```bash
gouno-cli new my-service \
  -t https://github.com/myorg/custom-gouno-template \
  -m github.com/myorg/my-service
```

SSH：

```bash
gouno-cli new my-service \
  -t git@github.com:myorg/custom-gouno-template.git \
  -m github.com/myorg/my-service
```

## 固定 Template 版本

远程 Template 默认跟随仓库默认分支；传入 `--template-ref` 后会按指定 branch/tag 克隆。

为了保证创建过程可复现，推荐固定到不可变的 Release Tag：

```bash
gouno-cli new my-service \
  -t https://github.com/myorg/custom-gouno-template \
  --template-ref v2.3.0 \
  -m github.com/myorg/my-service
```

持续移动的分支适合 Template 开发过程，但不是不可变的正式发布输入。

## 使用本地 Template

```bash
gouno-cli new my-service \
  -t /path/to/my-local-template \
  -m github.com/you/my-service
```

这种方式适合在发布之前开发和测试自己的 Project Template。

## Bootstrap 行为

从高层看，`gouno-cli new` 会：

1. 克隆或读取所选的完整 Project Template；
2. 在普通 Bootstrap 文件中按需渲染 `{{.ModulePath}}`、`{{.ProjectName}}` 等第一阶段项目值；
3. 将 `.gouno/codegen*` 下的 Codegen v1 Runtime Resources 原样复制；
4. 过滤保留路径和私有文件；
5. 在安全权限掩码下保留可执行权限；
6. 默认执行 `go mod tidy`，除非传入 `--skip-tidy`；
7. 渲染或依赖整理失败时删除未完成的目标项目。

精确、具有约束力的行为由 [`gouno-cli` Project Template Contract v1](https://github.com/rushairer/gouno-cli/blob/main/docs/project-template-contract.md) 定义。本指南只解释用法，不复制第二份规范。

### 两阶段模板模型

启用 Codegen 的项目可以同时存在两个互相独立的渲染阶段：

```text
Stage 1: gouno-cli new
  Bootstrap 数据：ModulePath / ProjectName

Stage 2: gouno gen ...
  项目 Codegen 数据：arguments / flags / Codegen functions
```

`.gouno/codegen.yaml` 与 `.gouno/codegen/**` 在 Stage 1 会被原样复制，因此 Stage 2 的表达式不会在创建项目时被提前消费。

Project Template **不要求**支持 Codegen。如果没有 `.gouno/codegen.yaml`，生成项目完全可以没有 `gen` 命令。

## 历史保留的 `templates/` 路径

为了兼容早期 Gouno Template，`gouno-cli` 目前仍会过滤名为 `templates/` 的路径段。

它**不是** Codegen v1 的目录。新的 Codegen Template 应使用：

```text
.gouno/codegen.yaml
.gouno/codegen/
```

不要依赖 `templates/` 被复制到生成项目。

## 关于开发自己的 Template

自定义 Template 应从 Project Template Contract 出发，而不是从官方默认 Template 的 DDD/Gin 目录开始。一个最小合法 Template 可以只是很小的项目骨架、少量 Bootstrap 变量，并且完全没有 Codegen。

官方 [`gouno-template`](https://github.com/rushairer/gouno-template) 适合作为生产向默认栈的参考实现，但是否采用它的全部架构选择由 Template 作者自己决定。

在专门的 Authoring Guide 落地前，开发自定义 Template 时应通过 `gouno-cli new` 生成临时项目，再执行 `go mod tidy` 和生成项目自己的 build/test 检查。当前没有公开的 `template validate` 子命令，不要把它当成已经存在的工具写入使用说明。

## 下一步

- [代码生成](./code-generation.md) — 理解 Template 定义的 Codegen 能力
- [配置管理](./configuration.md) — 默认 Template 使用的配置方式
