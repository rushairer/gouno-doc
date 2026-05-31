# Code Generation

[中文](./zh-CN/code-generation.md)

gouno's code generator creates DDD-structured modules from templates. It saves you from writing the same boilerplate for every new entity, service, or task.

## Generate a Complete Module

The `suite` command generates domain, repository, and service files in one step:

```bash
gouno gen suite user
```

Output:

```
internal/
├── domain/user.go         ← Entity struct
├── repository/user.go     ← Data access interface
└── service/user.go        ← Business logic interface
```

## Generate Individual Files

```bash
gouno gen domain order              # → internal/domain/order.go
gouno gen repository order          # → internal/repository/order.go
gouno gen service order             # → internal/service/order.go
gouno gen controller order          # → controller/order.go
gouno gen task send_email           # → internal/task/send_email.go
```

## Command Aliases

```bash
gouno gen d order    # domain
gouno gen r order    # repository
gouno gen s order    # service
gouno gen c order    # controller
gouno gen t send_email  # task
```

## Options

Every generation command supports:

| Flag | Description | Default |
|------|-------------|---------|
| `--path, -p` | Output directory | Depends on type (see below) |
| `--force, -f` | Overwrite existing files | false |
| `--template-set` | Template set to use | From .gouno.yaml or built-in |

Default output paths:

| Type | Default Path |
|------|-------------|
| domain | `internal/domain/` |
| repository | `internal/repository/` |
| service | `internal/service/` |
| controller | `controller/` |
| task | `internal/task/` |

## Examples

```bash
# Generate with custom path
gouno gen suite user --path ./pkg/user

# Force overwrite existing files
gouno gen suite user --force

# Use a specific template set
gouno gen suite user --template-set gorm

# Generate only the domain entity
gouno gen domain product
```

## Naming Convention

The name you pass is automatically converted to CamelCase for struct names:

```bash
gouno gen suite foo_bar    # → struct FooBar, FooBarService, FooBarRepository
gouno gen suite my_order   # → struct MyOrder, MyOrderService, MyOrderRepository
gouno gen suite user       # → struct User, UserService, UserRepository
```

## What's Next

- [Template Sets](./template-sets.md) — Customize the generated code style
