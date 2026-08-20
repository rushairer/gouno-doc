# 快速开始

[English](../getting-started.md)

## 前置要求

- Go 1.23+
- Git

## 安装 gouno-cli

```bash
go install github.com/rushairer/gouno-cli@latest
```

验证安装：

```bash
gouno-cli --help
```

## 创建项目

```bash
gouno-cli new my-service -m github.com/you/my-service
```

从默认模板（`gouno-template`）创建一个新的 Go Web 项目。可选参数：

| 参数 | 缩写 | 默认值 | 说明 |
|------|------|--------|------|
| `--module` | `-m` | 项目名称 | Go module 路径（例如 `github.com/you/my-service`） |
| `--template` | `-t` | `./templates` | 模板来源（Git 仓库 URL 或本地目录路径，默认从 GitHub 克隆 gouno-template） |
| `--skip-tidy` | | `false` | 创建项目后跳过执行 `go mod tidy` |

使用自定义模板仓库创建项目：

```bash
gouno-cli new order-service \
  -t https://github.com/myorg/custom-gouno-template \
  -m github.com/myorg/order-service
```

## 构建运行

```bash
cd my-service
make build
make run
```

开发模式（热重载）：

```bash
make dev
```

服务启动在 `http://localhost:8080`。

## 验证

```bash
curl http://localhost:8080/test/alive
# → {"code":200,"message":"success","data":"pong"}
```

## CLI 参数

```bash
my-service web [flags]

参数:
  -c, --config_path string   配置文件路径（默认 "./config"）
  -a, --address string       监听地址（默认 "0.0.0.0"）
  -p, --port string          监听端口（默认 "8080"）
  -d, --debug                调试模式
  -e, --env string           环境：development, test, production（默认 "production"）
```

## 下一步

- [代码生成](./code-generation.md) — 生成 DDD 模块
