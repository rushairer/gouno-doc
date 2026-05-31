# Template Sets

[中文](./zh-CN/template-sets.md)

Template sets are the extension mechanism for gouno's code generator. They let you customize what `gouno gen` produces without modifying gouno's source code.

## Use an Existing Template Set

### Install

```bash
# From a git repository
gouno-cli template install gorm https://github.com/myorg/gouno-template-gorm

# From a local directory
gouno-cli template install gorm /path/to/my-template-set
```

This copies the template files to `~/.gouno/templates/gorm/`.

### Use in a Project

Option 1: Set when creating a project:

```bash
gouno-cli new order-service --template-set gorm -m github.com/myorg/order-service
```

This saves `template-set: gorm` in `.gouno.yaml`. All subsequent `gouno gen` commands in this project will use the gorm templates.

Option 2: Set per command:

```bash
gouno gen suite user --template-set gorm
```

Option 3: Create `.gouno.yaml` manually in your project root:

```yaml
template-set: gorm
```

### Search Priority

When generating code, gouno looks for templates in this order:

1. **`--template-set` flag** — highest priority
2. **`.gouno.yaml` in project root** — project-level default
3. **Built-in default templates** — fallback (always available)

### Manage

```bash
gouno-cli template list              # List installed template sets
gouno-cli template remove gorm       # Remove a template set
gouno-cli template install gorm <url> --force  # Overwrite existing
```

## Create a Custom Template Set

### Step 1: Understand the File Structure

A template set repository has two parts:

1. **`templates/` directory** — contains the `.tmpl` files (the actual template set)
2. **Project scaffold** — the rest of the repo (cmd/, config/, etc.) used when `gouno-cli new` creates a project from this template

Look at [gouno-template](https://github.com/rushairer/gouno-template) as the reference:

```
gouno-template/                  ← The repo IS the template set + project scaffold
├── templates/                   ← Template set: .tmpl files live here
│   ├── domain.tmpl
│   ├── repository.tmpl
│   ├── service.tmpl
│   ├── controller.tmpl
│   └── task.tmpl
├── cmd/                         ← Project scaffold
│   ├── main.go
│   └── gouno/
├── config/                      ← Project scaffold
├── internal/                    ← Project scaffold
├── Makefile
└── go.mod
```

When you run `gouno-cli template install gorm /path/to/gouno-template`, only the **contents of `templates/`** are copied to `~/.gouno/templates/gorm/`. The project scaffold is not included.

If your template set is **only** templates (no project scaffold), you can put `.tmpl` files directly in the `templates/` directory:

```
my-template-set/
└── templates/
    ├── domain.tmpl
    ├── repository.tmpl
    ├── service.tmpl
    ├── controller.tmpl
    └── task.tmpl
```

### Step 2: Create the Templates

```bash
mkdir -p my-template-set/templates
cd my-template-set/templates
```

Create the five template files. You don't need all five — missing files fall back to built-in defaults.

Each `.tmpl` file uses `%s` as the struct name placeholder (5 occurrences per file).

**`domain.tmpl` — with GORM:**

```
package domain

import "time"

type %s struct {
    ID        uint      `json:"id" gorm:"primaryKey"`
    Name      string    `json:"name" gorm:"size:255;not null"`
    CreatedAt time.Time `json:"created_at"`
    UpdatedAt time.Time `json:"updated_at"`
}

func New%s() *%s {
    return &%s{}
}
```

**`repository.tmpl` — with interfaces:**

```
package repository

import "context"

type %sRepository interface {
    FindByID(ctx context.Context, id uint) (*domain.%s, error)
    Create(ctx context.Context, entity *domain.%s) error
}

func New%sRepository() %sRepository {
    return nil
}
```

**`service.tmpl` — with interfaces:**

```
package service

import "context"

type %sService interface {
    FindByID(ctx context.Context, id uint) (*domain.%s, error)
    Create(ctx context.Context, entity *domain.%s) error
}

type %sServiceImpl struct {
}

func New%sService() %sService {
    return &%sServiceImpl{}
}

func (s *%sServiceImpl) FindByID(ctx context.Context, id uint) (*domain.%s, error) {
    return nil, nil
}

func (s *%sServiceImpl) Create(ctx context.Context, entity *domain.%s) error {
    return nil
}
```

**`controller.tmpl` — Gin handlers:**

```
package controller

import (
    "net/http"
    "github.com/gin-gonic/gin"
    "github.com/rushairer/gouno"
)

type %sController struct {
}

func New%sController() *%sController {
    return &%sController{}
}

func (c *%sController) List(ctx *gin.Context) {
    ctx.JSON(http.StatusOK, gouno.NewSuccessResponse(nil))
}

func (c *%sController) Get(ctx *gin.Context) {
    ctx.JSON(http.StatusOK, gouno.NewSuccessResponse(nil))
}

func (c *%sController) Create(ctx *gin.Context) {
    ctx.JSON(http.StatusOK, gouno.NewSuccessResponse(nil))
}
```

**`task.tmpl` — background task:**

```
package task

import "context"

type %sTask struct {
}

func New%sTask() *%sTask {
    return &%sTask{}
}

func (t *%sTask) Run(ctx context.Context) error {
    return nil
}
```

### Template Variable Reference

`%s` is replaced with the CamelCase version of the name you pass to `gouno gen`:

| Command | `%s` becomes |
|---------|-------------|
| `gouno gen suite user` | `User` |
| `gouno gen suite foo_bar` | `FooBar` |
| `gouno gen suite my_order` | `MyOrder` |

The placeholder appears **5 times** in each template (struct name, constructor, receiver, etc.).

### Step 3: Test Locally

```bash
# Install from local directory
gouno-cli template install my-set /path/to/my-template-set/templates

# Create a test project
gouno-cli new test-project --template-set my-set -m github.com/test/test-project
cd test-project && go mod tidy

# Generate and verify
gouno gen suite user
cat internal/domain/user.go     # Check generated domain
cat internal/service/user.go    # Check generated service
go build ./...                  # Verify compilation
```

Iterate: edit `.tmpl` → reinstall with `--force` → regenerate with `--force`.

### Step 4: Publish

```bash
cd my-template-set
git init && git add . && git commit -m "initial template set"
git remote add origin https://github.com/myorg/my-template-set
git push -u origin main
```

Others install with one command:

```bash
gouno-cli template install my-set https://github.com/myorg/my-template-set
```

### Naming Convention

Use a name that describes the tech stack or style:

```
gorm            — GORM-based data access
ent             — Ent ORM
clean-arch      — Clean Architecture style
my-company      — Company internal conventions
```

## Template File Reference

| File | Generated By | Default Output Path |
|------|-------------|-------------------|
| `domain.tmpl` | `gouno gen domain` | `internal/domain/` |
| `repository.tmpl` | `gouno gen repository` | `internal/repository/` |
| `service.tmpl` | `gouno gen service` | `internal/service/` |
| `controller.tmpl` | `gouno gen controller` | `controller/` |
| `task.tmpl` | `gouno gen task` | `internal/task/` |

`gouno gen suite <name>` generates domain + repository + service using their respective templates.

## FAQ

**Q: What happens if a template file is missing from my set?**

A: gouno falls back to the built-in default template for that type. You only need to create templates for the types you want to customize.

**Q: Can I use Go template syntax (`{{.Field}}`) in `.tmpl` files?**

A: No. The templates use `fmt.Sprintf` with `%s`, not Go's `text/template` engine. Go code naturally contains `{{` and `}}` (e.g., map literals), which would conflict with template parsing.

**Q: Where are template sets stored?**

A: `~/.gouno/templates/<name>/`. Each template set is a directory containing `.tmpl` files.

**Q: Can I have project-specific templates?**

A: Not directly. The `.gouno.yaml` file only stores the template set name. The actual templates live in `~/.gouno/templates/`. If you need project-specific templates, create a dedicated template set.

## What's Next

- [Configuration](./configuration.md) — Multi-environment YAML config
