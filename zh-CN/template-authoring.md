# 开发自己的 Gouno Project Template

[English](../template-authoring.md)

Gouno 的 Project Template 是 `gouno-cli new` 使用的完整 Go 项目骨架。

最重要的设计原则只有一句：

> **Gouno 负责机制，Template 负责项目策略。**

你的 Template 可以自行决定 Web 框架、目录结构、依赖集合、架构模式、配置方案、工程约定，以及是否提供 Codegen、提供哪些 Generator。官方 [`gouno-template`](https://github.com/rushairer/gouno-template) 是参考实现，不是所有 Template 必须继承的“基类”。

本指南负责解释 Template Authoring 工作流。项目 Bootstrap 的权威行为由 [`gouno-cli` Project Template Contract v1](https://github.com/rushairer/gouno-cli/blob/main/docs/project-template-contract.md) 定义；可选 Codegen 的协议由 [`gouno` Codegen Specification v1](https://github.com/rushairer/gouno/blob/main/docs/codegen-template-spec.md) 定义。

## 1. 从最小 Template 开始

除非你确实想采用官方默认 Template 的架构，否则不要一开始就复制整套 `gouno-template`。

一个最小 Template 可以只有：

```text
my-gouno-template/
├── cmd/
│   └── main.go
├── go.mod
└── README.md
```

`go.mod`：

```go
module {{.ModulePath}}

go 1.25.0
```

`cmd/main.go`：

```go
package main

import "fmt"

func main() {
    fmt.Println("{{.ProjectName}}")
}
```

这已经足以构成一个用于验证 Project Template Contract 的最小项目。它不要求 Gin、Cobra、DDD、Gouno Runtime，也不要求 Codegen。

### 本地测试

在 Template 仓库之外的目录执行：

```bash
gouno-cli new demo-service \
  -t /absolute/path/to/my-gouno-template \
  -m example.com/demo-service
```

然后检查生成项目：

```bash
cd demo-service
go mod tidy
go build ./...
go test ./...
```

生成后的 `go.mod` 应使用 `example.com/demo-service`，使用 ProjectName 的位置应得到 `demo-service`。

## 2. 理解 Stage 1：Project Bootstrap

`gouno-cli new` 是第一阶段渲染。

Bootstrap 数据刻意保持很小：

```text
{{.ModulePath}}
{{.ProjectName}}
```

只在创建项目时确实需要替换的地方使用它们，例如：

- `go.mod` 的 `module`；
- 包含新 module path 的 import；
- 项目名称或默认标签；
- 由项目名派生的本地默认文件名或标识符。

精确的 parse、copy、rollback 行为属于 Project Template Contract。不要依赖未文档化行为设计 Template。

### 重要的保留路径

`gouno-cli` 当前仍会过滤若干私有/保留路径。尤其是：

```text
templates/
```

这是为了兼容早期 Gouno Template 而保留的**历史路径**，不是 Codegen v1 的目录。

新的 Codegen 资源不要放在这里，应使用 `.gouno/codegen/`。

## 3. 决定生成项目是否需要 Gouno Runtime

从 Project Template Contract 的角度，Template 并不要求必须依赖 `github.com/rushairer/gouno` module。

只有当生成项目确实需要 Gouno 提供的可复用机制时才引入它，例如 Codegen Runtime，或你选择使用的 Middleware / Response 等基础能力。业务架构和项目分层仍然属于 Template / 项目自身。

不要仅仅为了固化目录结构或业务层抽象，就把这些规则搬进 Gouno Core。

如果 Template 声明了 Gouno 依赖，正式发布时应使用已经发布的稳定版本。除非明确属于开发状态，否则不要发布依赖本地 `replace` 或未发布 pseudo-version 的 Template。

## 4. Codegen 是可选能力

没有 `.gouno/codegen.yaml` 的 Template 可以完全没有 Codegen 命令，这是合法且受支持的设计。

如果团队确实需要重复生成源码，可以显式启用 Codegen v1。

例如：

```text
my-gouno-template/
├── .gouno/
│   ├── codegen.yaml
│   └── codegen/
│       └── handler.tmpl
├── cmd/
│   └── ...
├── go.mod
└── ...
```

假设你的架构使用 `handler`，而不是官方默认 Template 的 `controller/service/...` 词汇。

`.gouno/codegen.yaml`：

```yaml
schema: gouno.dev/codegen/v1
command:
  use: gen
  short: Generate project code

generators:
  - name: handler
    short: Generate an HTTP handler
    args:
      - name: name
        required: true
    flags:
      - name: path
        shorthand: p
        type: string
        default: internal/handler
        description: output directory
      - name: force
        shorthand: f
        type: bool
        default: false
        description: overwrite an existing file
    outputs:
      - template: .gouno/codegen/handler.tmpl
        path: '{{ flag "path" }}/{{ arg "name" }}.go'
```

`handler.tmpl` 可以是：

```go
package handler

type {{ camel (arg "name") }}Handler struct{}
```

这样生成项目就可以提供：

```bash
gouno gen handler user
```

`gen` 和 `handler` 都是 Template Policy。其它 Template 可以选择不同的 Codegen 根命令和 Generator 清单。

不要在自己的文档里复制一份完整 Codegen Schema 形成第二个规范源。支持的字段、表达式、组合、覆盖和安全规则统一以 [Codegen Specification v1](https://github.com/rushairer/gouno/blob/main/docs/codegen-template-spec.md) 为准。

## 5. 将 Project-aware Codegen 挂到项目 CLI

Manifest 本身只是数据。项目如果要使用 Gouno Codegen，还需要通过 Gouno Runtime 把当前项目定义的命令挂到项目 CLI。

官方默认 Template 当前使用与下面等价的方式：

```go
package projectcli

import (
    "log"

    "github.com/rushairer/gouno/generator"
    "github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{Use: "my-project"}

func Execute() {
    if _, err := generator.AttachProjectCommand(rootCmd, ""); err != nil {
        log.Fatalf("load project commands: %v", err)
    }
    if err := rootCmd.Execute(); err != nil {
        log.Fatal(err)
    }
}
```

`AttachProjectCommand` 会发现当前项目的 manifest；存在时挂载 manifest 定义的命令，不存在时不会凭空提供 Codegen 命令。

项目其它 Cobra 命令如何组织仍然由你的 Template 自己决定。

## 6. 理解 Stage 2：Project Codegen

支持 Codegen 的 Template 实际包含两套生命周期不同的模板语言：

```text
┌─────────────────────────────────────────────┐
│ Stage 1 — Project Bootstrap                 │
│ owner: gouno-cli                            │
│ command: gouno-cli new                      │
│ values: ModulePath / ProjectName            │
└───────────────────┬─────────────────────────┘
                    │ 生成项目
                    ▼
┌─────────────────────────────────────────────┐
│ Stage 2 — Project Codegen（可选）            │
│ owner: Gouno protocol + project policy      │
│ command: manifest 定义，常见为 gouno gen      │
│ values: args / flags / Codegen functions    │
└─────────────────────────────────────────────┘
```

两阶段的明确边界是：

```text
.gouno/codegen.yaml
.gouno/codegen/**
```

这些文件在 Stage 1 被原样复制，使 Codegen 表达式保留到 Stage 2 才执行。

不要利用“普通文件在 Stage 1 parse 失败后会原样复制”的容错行为来保护 Stage 2 语法。Codegen Runtime Data 应放进正式定义的 `.gouno/codegen*` 边界。

## 7. 保持项目架构与 Generator 同步

当 Template 拥有 Generator Policy 后，manifest 就成为 Template 开发契约的一部分。

例如把：

```text
internal/service/
```

调整成：

```text
internal/application/
```

那么同一次变更中就应该同步修改 Generator 输出路径和对应源码模板。

一个很实用的判断原则是：

> 如果生成代码总需要人工做同一种修补，应修改 Template / Generator，而不是让每个业务项目重复修补。

Generator 写出的源码随后就是普通项目代码，必须遵守和手写代码相同的包边界、安全控制、Lint、错误处理和测试规则。

## 8. 有意识地决定哪些文件要被生成项目继承

目前 `gouno-cli` **没有**通用 `.gounoignore` 或 Template source-only manifest。

除了 Project Template Contract 已明确过滤的路径之外，应把 Template 仓库里的文件视为“可能进入生成项目”的文件。

这对于下面这些文件尤其重要：

```text
AGENTS.md
.github/
scripts/
docs/
Makefile
```

增加文件之前问一个问题：

> 使用这个 Template 创建出来的项目，也应该得到这个文件吗？

如果答案是“应该”，就把它设计成项目契约的一部分；如果答案是“不应该”，不要自己发明一个未文档化隐藏目录并假设 CLI 会排除它。

### 下发 `AGENTS.md`

在 AI 辅助研发环境中，Template 携带 `AGENTS.md` 很有价值，因为工程约束可以和代码结构一起传给新项目。

适合继承的内容包括：

- 当前 Template 自己的包/层级边界；
- Codegen Policy 放在哪里；
- 必须执行的测试和安全检查；
- 生成代码的工程规则；
- 项目自己的依赖、配置或安全边界。

如果某条指令只对“Template 仓库维护者”成立、进入生成项目后就失去意义，就不要放进根 `AGENTS.md`。在通用 source-only 机制出现前，根 `AGENTS.md` 应保证被下游项目继承后依然成立。

可以参考官方 [`gouno-template/AGENTS.md`](https://github.com/rushairer/gouno-template/blob/main/AGENTS.md) 的做法。

## 9. 建立可重复的 Template 验证脚本

不要只测试 Template 源仓库本身，要测试**真正渲染后的项目**。

建议验证链：

```text
渲染 / 创建临时项目
        ↓
检查 module 文件稳定性
        ↓
go mod tidy / download
        ↓
build + test
        ↓
如果存在 Codegen：
  检查 help
  执行代表性 Generator
  执行声明的组合 Generator
  编译 / 测试生成结果
        ↓
gofmt / vet / lint / vulnerability checks
```

官方 [`gouno-template/scripts/verify-template.sh`](https://github.com/rushairer/gouno-template/blob/main/scripts/verify-template.sh) 可以作为这种验证方式的参考，但你应该根据**自己的**架构和 Generator 清单设计 Smoke Test，而不是机械复制它的 DDD 测试项。

Go Template 至少建议验证：

```bash
go mod tidy
go test ./...
go vet ./...
```

面向生产的 Template 通常还应该加入 race test、lint、漏洞扫描，以及团队自己的 architecture/security checks。

### Reusable CI

`gouno-doc` 提供可复用的 Project Template Quality Workflow，会在受支持的 Go 版本矩阵中执行 Template 自己的 `scripts/verify-template.sh`。

调用时应固定到某个**已经发布的 gouno-doc 完整 commit SHA**：

```yaml
jobs:
  template-quality:
    uses: rushairer/gouno-doc/.github/workflows/project-template-quality.yml@<released-gouno-doc-commit-sha>
```

正式 CI 不要固定到 `@main` 等持续移动的 ref。

## 10. 发布之前走一次真实 CLI 链路

打 Tag 之前，应按照用户真实使用路径验证。

本地候选 Template：

```bash
gouno-cli new template-smoke \
  -t /absolute/path/to/your-template \
  -m example.com/template-smoke
```

已经推送到远端的 Release Candidate：

```bash
gouno-cli new template-smoke \
  -t https://github.com/yourorg/your-template \
  --template-ref your-release-candidate-ref \
  -m example.com/template-smoke
```

验证对象应该是生成项目，而不仅仅是 Template Source Repository。

如果启用了 Codegen，还应执行类似：

```bash
./your-project-command --help
./your-project-command gen --help
./your-project-command gen <representative-generator> smoke
```

这里的 `gen` 只是常见/default 选择，实际应使用你项目 manifest 声明的命令。

## 11. 使用不可变版本发布 Template

确认 Template 版本通过验证后，使用不可变 Git Tag 发布，并建议使用者在需要可复现性时通过 `--template-ref` 固定版本。

例如：

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

使用方：

```bash
gouno-cli new billing-service \
  -t https://github.com/yourorg/your-template \
  --template-ref v1.0.0 \
  -m github.com/yourorg/billing-service
```

把 Template 当作真实工程产物维护版本：记录架构变化、依赖变化、生成结果变化、Codegen Policy 变化和兼容性要求。

## 12. 推荐的 Template 仓库形态

下面只是建议，不是强制结构：

```text
my-gouno-template/
├── .github/                 # 如果生成项目也应该继承这些 CI
├── .gouno/                  # 只有启用相关项目工具时才需要
│   ├── codegen.yaml
│   └── codegen/
├── cmd/
├── internal/                # 你的架构，不是 Gouno Core 的架构
├── scripts/                 # 如果生成项目也应该使用这些脚本
├── AGENTS.md                # 可选：下发给生成项目的工程契约
├── CHANGELOG.md
├── Makefile
├── README.md
├── go.mod
└── go.sum
```

你的 Template 完全可以比这个更小；Contract 并不要求这些目录存在。

## 13. 常见错误

避免这些问题：

- 复制官方 Template 后误以为它的架构是 Gouno 强制要求；
- 把新 Codegen 资源放进历史 `templates/` 路径；
- 文档声称存在某个 Generator，但 manifest 实际没有声明；
- 每次执行 Codegen 都去远端 Template 拉最新 Generator；
- 让 Stage 1 提前消费 Stage 2 的 Codegen 表达式；
- 在正式 Template 中无意保留 pseudo-version 或本地 `replace`；
- 把只有 Template 维护者才理解的指令下发进所有生成项目；
- 为了让 Template CI 通过而降低生成项目本身的质量门禁。

## 14. 关于未来的 `template validate` 工具

当前并没有公开的 `gouno-cli template validate` 命令。

未来增加一个轻量 Validator 可能很有价值，但它应该去**实现已经稳定的 Project Template Contract**，而不是借工具之名重新发明语义。合理的未来 Validator 可以展示哪些文件会 Render / Raw Copy / Filter，校验 Codegen Runtime Resources，创建临时项目并执行配置的验证流程，同时避免把 Gouno 演变成 Template Package Manager。

目前权威路径仍然是：

```text
Project Template Contract
        ↓
本 Authoring Guide
        ↓
你的 Template + verification script
        ↓
gouno-cli new smoke test
        ↓
不可变 Release
```

## 参考

- [项目模板：选择和固定 Template](./project-templates.md)
- [代码生成：使用 Template-defined Generator](./code-generation.md)
- [Gouno Project Template Contract v1](https://github.com/rushairer/gouno-cli/blob/main/docs/project-template-contract.md)
- [Gouno Template Codegen Specification v1](https://github.com/rushairer/gouno/blob/main/docs/codegen-template-spec.md)
- [官方默认 Template](https://github.com/rushairer/gouno-template)
