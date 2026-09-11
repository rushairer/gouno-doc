# 代码生成

[English](../code-generation.md)

现代 Gouno 中的代码生成是一个 **Project Template Capability**。

Gouno Core 提供 Codegen 协议和执行引擎；当前项目/Template 决定是否存在 Codegen，以及启用后具体的命令名、Generator 清单、参数、Flag、输出路径、组合关系和源码模板。

Gouno Core 不再内置一套固定的 DDD Generator 清单。

## 先发现当前项目实际支持什么

官方 `gouno-template` 会携带 `.gouno/codegen.yaml`，当前使用 `gen` 作为 Codegen 命令：

```bash
gouno gen --help
```

其它 Template 可以提供完全不同的 Generator 清单；没有 `.gouno/codegen.yaml` 的 Template 可以完全没有 Codegen 命令。

因此在当前项目 manifest/help 没有声明之前，不要默认 `domain`、`repository`、`service`、`controller`、`task` 或 `suite` 一定存在。

## 官方默认 `gouno-template` 示例

默认 Template 当前定义：

```bash
gouno gen domain order
gouno gen repository order
gouno gen service order
gouno gen controller order
gouno gen task send_email
gouno gen suite order
```

默认 `suite` 是 Template 自己定义的组合：

```text
domain
repository
service
```

这个组合不是 Gouno Core 规则。

### 默认输出目录

官方默认 Template 当前使用：

| Generator | 默认输出 |
|-----------|----------|
| `domain` | `internal/domain/<name>.go` |
| `repository` | `internal/repository/<name>.go` |
| `service` | `internal/service/<name>.go` |
| `controller` | `internal/controller/<name>.go` |
| `task` | `internal/task/<name>.go` |

这些路径全部来自默认 Template 的 `.gouno/codegen.yaml`。

### 默认 Flags

默认 Template 的单文件 Generator 当前声明：

```text
--path, -p
--force, -f
```

例如：

```bash
gouno gen service order --path internal/application
gouno gen service order --force
```

默认 `suite` 当前只声明 `--force`，并没有公共 `--path` 参数。不要假设所有 Generator 参数都一样，应以：

```bash
gouno gen <generator> --help
```

为准。

当 manifest 声明名为 `force` 的 bool Flag 时，Codegen v1 Engine 会把它解释成覆盖策略；默认情况下已存在文件会被跳过。

## Generator Policy 属于项目

另一个 Template 完全可以定义：

```text
gouno gen handler user
gouno gen usecase user
gouno gen gateway user
```

也可以只提供：

```text
gouno gen module user
```

还可以完全不支持 Codegen。

这是有意的架构边界：项目架构属于 Template / 当前项目，Gouno 只拥有通用机制。

## Codegen Runtime Resources

启用 Codegen 的项目通常携带：

```text
.gouno/
├── codegen.yaml
└── codegen/
    └── *.tmpl
```

这些文件会跟随生成项目一起保存，因此后续执行 Codegen 时使用的是项目创建时固化下来的策略，而不是每次去远端 Template 拉取最新版本。

## Template Expressions

Codegen v1 支持的模板函数包括：

```text
arg
flag
camel
snake
kebab
lower
upper
```

例如源码模板可以使用位置参数构造 Go 类型名，同时由 manifest 决定输出路径。

Manifest 字段、表达式语义、组合规则、安全规则以及保留的 `force` 行为，以 [Gouno Template Codegen Specification v1](https://github.com/rushairer/gouno/blob/main/docs/codegen-template-spec.md) 为唯一规范。

## 安全模型

Codegen v1 会校验项目相对路径、拒绝逃逸项目根目录的模板/输出路径、格式化生成的 Go 文件，并且不提供任意 Shell Hook 或 Executable Plugin。

生成代码写入项目后就是普通项目代码，不能因为来自 Generator 就绕过代码评审、安全约束、包边界或测试要求。

## 下一步

- [项目模板](./project-templates.md) — 选择并固定 Project Template
- [配置管理](./configuration.md) — 默认 Template 的配置行为
