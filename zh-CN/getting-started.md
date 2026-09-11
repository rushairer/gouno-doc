# 快速开始

[English](../getting-started.md)

## 前置要求

- Go 1.25.0 或更高版本
- Git

当前 Gouno 质量门禁覆盖 Go 1.25.x 与 1.26.x。

## 安装 gouno-cli

```bash
go install github.com/rushairer/gouno-cli@latest
```

验证：

```bash
gouno-cli --version
```

## 创建项目

```bash
gouno-cli new my-service -m github.com/you/my-service
```

在通常的默认环境下，这会使用官方 `gouno-template` 创建项目。

常用参数：

| 参数 | 缩写 | 默认值 | 说明 |
|------|------|--------|------|
| `--module` | `-m` | 项目名称 | Go module 路径 |
| `--template` | `-t` | `./templates` | 本地 Template 目录或受支持的远程 Git URL |
| `--template-ref` | | 空 | 远程 Template 的 branch/tag 选择器 |
| `--skip-tidy` | | `false` | 创建项目后跳过 `go mod tidy` |

使用自定义 Template：

```bash
gouno-cli new order-service \
  -t https://github.com/myorg/custom-gouno-template \
  -m github.com/myorg/order-service
```

固定已发布的 Template 版本以保证脚手架过程可复现：

```bash
gouno-cli new order-service \
  -t https://github.com/myorg/custom-gouno-template \
  --template-ref v2.3.0 \
  -m github.com/myorg/order-service
```

官方 Template 是参考实现。自定义 Template 可以采用完全不同的框架和架构，也可以提供不同的 Codegen 能力，甚至完全不支持 Codegen。

## 构建并运行默认 Template

```bash
cd my-service
make build
make run
```

开发时也可以使用热重载：

```bash
make dev
```

默认 Template 在没有其它配置或参数覆盖时监听 8080 端口。

## 验证默认 Template

```bash
curl http://localhost:8080/test/alive
```

## 项目 CLI

默认 Template 包含 `web` 命令：

```bash
./bin/gouno web --help
```

它还主动启用了 Template-defined Codegen v1，因此当前默认项目会暴露：

```bash
./bin/gouno gen --help
```

不要假设自定义 Template 一定存在 `gen`。只有 Template 提供对应 manifest/capability 时，项目才拥有 Codegen 命令。

## 下一步

- [项目模板](./project-templates.md) — 选择并固定完整 Project Template
- [代码生成](./code-generation.md) — 理解 Template 定义的 Codegen
- [配置管理](./configuration.md) — 默认 Template 的配置方式
