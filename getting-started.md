# Getting Started

[中文](./zh-CN/getting-started.md)

## Prerequisites

- Go 1.25.0 or newer
- Git

Current Gouno quality gates cover Go 1.25.x and 1.26.x.

## Install gouno-cli

```bash
go install github.com/rushairer/gouno-cli@latest
```

Verify:

```bash
gouno-cli --version
```

## Create a project

```bash
gouno-cli new my-service -m github.com/you/my-service
```

This creates a project from the official default `gouno-template` in the normal default setup.

Useful options:

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--module` | `-m` | project name | Go module path |
| `--template` | `-t` | `./templates` | Local template directory or supported remote Git URL |
| `--template-ref` | | empty | Branch/tag selector for a remote template |
| `--skip-tidy` | | `false` | Skip `go mod tidy` after project creation |

Use a custom template:

```bash
gouno-cli new order-service \
  -t https://github.com/myorg/custom-gouno-template \
  -m github.com/myorg/order-service
```

Pin a released template for reproducible scaffolding:

```bash
gouno-cli new order-service \
  -t https://github.com/myorg/custom-gouno-template \
  --template-ref v2.3.0 \
  -m github.com/myorg/order-service
```

The official template is a reference implementation. A custom template may use a different framework or architecture and may expose different Codegen capabilities—or none at all.

## Build and run the default template

```bash
cd my-service
make build
make run
```

Or use hot reload:

```bash
make dev
```

The default template listens on port 8080 unless configuration or flags override it.

## Verify the default template

```bash
curl http://localhost:8080/test/alive
```

## Project CLI

The default template includes a `web` command:

```bash
./bin/gouno web --help
```

It also opts into template-defined Codegen v1, so its project CLI exposes:

```bash
./bin/gouno gen --help
```

Do not assume a custom template has `gen`; Codegen exists only when the project template provides the corresponding manifest/capability.

## What's next

- [Project Templates](./project-templates.md) — choose and pin full project templates
- [Code Generation](./code-generation.md) — understand template-defined Codegen
- [Configuration](./configuration.md) — default-template configuration
