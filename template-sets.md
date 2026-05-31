# Template Sets

[中文](./zh-CN/template-sets.md)

Template sets are the extension mechanism for gouno's code generator. They let you customize what `gouno gen` produces without modifying gouno's source code.

A template set is a directory containing `.tmpl` files. Each file is a Go `text/template` used to generate one type of code (domain, repository, service, etc.).

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

### Step 1: Create the Directory Structure

```bash
mkdir my-template-set
cd my-template-set
```

Create the five template files:

```
my-template-set/
├── domain.tmpl
├── repository.tmpl
├── service.tmpl
├── controller.tmpl
└── task.tmpl
```

You don't need all five. Only create the ones you want to customize. Missing files will fall back to the built-in default templates.

### Step 2: Write the Templates

Each `.tmpl` file is a Go `text/template`. Use `%s` as the placeholder for the struct name (it appears 5 times in each template).

**Minimal example — `domain.tmpl`:**

```
package domain

type %s struct {
    ID   uint   `json:"id"`
    Name string `json:"name"`
}

func New%s() *%s {
    return &%s{}
}
```

**With GORM — `domain.tmpl`:**

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

**With interfaces — `service.tmpl`:**

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

**With interfaces — `repository.tmpl`:**

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

**Gin controller — `controller.tmpl`:**

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

**Background task — `task.tmpl`:**

```
package task

import "context"

type %sTask struct {
}

func New%sTask() *%sTask {
    return &%sTask{}
}

func (t *%sTask) Run(ctx context.Context) error {
    // TODO: implement
    return nil
}
```

### Template Variable Reference

The `%s` placeholder is replaced with the CamelCase version of the name you pass to `gouno gen`:

| Command | `%s` becomes |
|---------|-------------|
| `gouno gen suite user` | `User` |
| `gouno gen suite foo_bar` | `FooBar` |
| `gouno gen suite my_order` | `MyOrder` |
| `gouno gen suite sendEmail` | `SendEmail` |

The placeholder appears **5 times** in each template (this is the convention for the struct name, constructor, and receiver).

### Step 3: Test Locally

Install your template set from the local directory:

```bash
gouno-cli template install my-set /path/to/my-template-set
```

Create a test project:

```bash
gouno-cli new test-project --template-set my-set -m github.com/test/test-project
cd test-project
go mod tidy
```

Generate code and verify:

```bash
gouno gen suite user
cat internal/domain/user.go     # Check the generated domain
cat internal/service/user.go    # Check the generated service
go build ./...                  # Verify it compiles
```

If something is wrong, edit the `.tmpl` files and reinstall:

```bash
gouno-cli template install my-set /path/to/my-template-set --force
gouno gen suite user --force    # Regenerate with updated templates
```

### Step 4: Publish

Push your template set to a git repository:

```bash
cd my-template-set
git init
git add .
git commit -m "initial template set"
git remote add origin https://github.com/myorg/my-template-set
git push -u origin main
```

Others can install it with:

```bash
gouno-cli template install my-set https://github.com/myorg/my-template-set
```

### Naming Convention

Template set names are arbitrary. Use a name that describes the tech stack or style:

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

When you run `gouno gen suite <name>`, it generates domain + repository + service using their respective templates.

## FAQ

**Q: What happens if a template file is missing from my set?**

A: gouno falls back to the built-in default template for that type. You only need to create templates for the types you want to customize.

**Q: Can I use Go template syntax (`{{.Field}}`) in `.tmpl` files?**

A: No. The templates use `fmt.Sprintf` with `%s`, not Go's `text/template` engine. This is because Go code naturally contains `{{` and `}}` (e.g., map literals), which would conflict with template parsing.

**Q: Where are template sets stored?**

A: `~/.gouno/templates/<name>/`. Each template set is a directory containing `.tmpl` files.

**Q: Can I have project-specific templates?**

A: Not directly. The `.gouno.yaml` file only stores the template set name. The actual templates live in `~/.gouno/templates/`. If you need project-specific templates, create a template set for that project.
