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

从默认模板创建一个新的 Go Web 项目。可选参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-m, --module` | Go module 路径 | 与项目名相同 |
| `-t, --template` | 模板来源（git URL 或本地路径） | 从 GitHub 克隆 gouno-template |
| `--template-set` | 代码生成使用的模板集 | （使用内置默认模板） |

使用自定义模板集创建项目：

```bash
gouno-cli new order-service \
  --template-set gorm \
  -m github.com/myorg/order-service
```

## 构建运行

```bash
cd my-service
go mod tidy
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
- [模板集](./template-sets.md) — 自定义代码生成模板
- [配置管理](./configuration.md) — 多环境配置
