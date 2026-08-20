# Getting Started

[中文](./zh-CN/getting-started.md)

## Prerequisites

- Go 1.23+
- Git

## Install gouno-cli

```bash
go install github.com/rushairer/gouno-cli@latest
```

Verify:

```bash
gouno-cli --help
```

## Create a Project

```bash
gouno-cli new my-service -m github.com/you/my-service
```

This creates a new Go web project from the default template (`gouno-template`). Options:

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--module` | `-m` | Project name | Go module path (e.g., `github.com/you/my-service`) |
| `--template` | `-t` | `./templates` | Template source (git URL or local directory, default clones gouno-template) |
| `--skip-tidy` | | `false` | Skip running `go mod tidy` after project creation |

Example using a custom project template repository:

```bash
gouno-cli new order-service \
  -t https://github.com/myorg/custom-gouno-template \
  -m github.com/myorg/order-service
```

## Build and Run

```bash
cd my-service
make build
make run
```

Or use hot-reload for development:

```bash
make dev
```

The server starts at `http://localhost:8080`.

## Verify

```bash
curl http://localhost:8080/test/alive
# → {"code":200,"message":"success","data":"pong"}
```

## CLI Flags

```bash
my-service web [flags]

Flags:
  -c, --config_path string   Config file path (default "./config")
  -a, --address string       Listen address (default "0.0.0.0")
  -p, --port string          Listen port (default "8080")
  -d, --debug                Debug mode
  -e, --env string           Environment: development, test, production (default "production")
```

## What's Next

- [Code Generation](./code-generation.md) — Generate DDD modules
