# Project Templates

[中文](./zh-CN/project-templates.md)

Project templates are the skeleton repositories used by `gouno-cli new` to scaffold new Go web projects.

Instead of maintaining a local registry or complex template sets, `gouno-cli` uses standard Git repositories or local directories directly via the `-t, --template` flag.

## Using Project Templates

### Default Template

By default, `gouno-cli` clones [gouno-template](https://github.com/rushairer/gouno-template):

```bash
gouno-cli new my-service -m github.com/you/my-service
```

### Custom Remote Git Template

Point `-t` to any Git repository URL (HTTPS or SSH):

```bash
# HTTPS URL
gouno-cli new my-service \
  -t https://github.com/myorg/custom-gouno-template \
  -m github.com/myorg/my-service

# SSH URL
gouno-cli new my-service \
  -t git@github.com:myorg/custom-gouno-template.git \
  -m github.com/myorg/my-service
```

### Local Directory Template

Point `-t` to a local folder:

```bash
gouno-cli new my-service \
  -t /path/to/my-local-template \
  -m github.com/you/my-service
```

---

## How Template Rendering Works

When `gouno-cli new` scaffolds a project:

1. **Clone / Copy**: Clones the remote repository into a temporary directory, or reads the local template directory.
2. **Variable Substitution**: Any file containing `{{` is parsed as a Go `text/template` with the following variables:
   - `{{.ModulePath}}`: The Go module path specified via `-m` (e.g. `github.com/you/my-service`).
   - `{{.ProjectName}}`: The project name passed as the first argument (e.g. `my-service`).
   Files without `{{` are copied verbatim.
3. **Automatic Filtering**: The following files and directories are automatically skipped during copying to protect privacy and prevent skeleton metadata leakage:
   - `.git/`
   - `.idea/`
   - `.DS_Store`
   - `bin/`
   - `templates/` (internal scaffold files for code generators)
   - `.env` and `.env.*`
   - `*.local.yaml` (private local configuration overrides)
4. **File Mode Preservation**: File executable permissions (e.g., `scripts/*.sh`) are preserved, while group/other write bits are sanitized for security.
5. **Module Tidying**: Automatically runs `go mod tidy` in the generated project unless `--skip-tidy` is specified.
6. **Atomic Rollback**: If template rendering or `go mod tidy` fails, the newly created directory is cleaned up automatically.

---

## Creating Your Own Project Template

To create a reusable project template for your team:

### 1. Structure Your Repository

Create a standard Go project skeleton (like [gouno-template](https://github.com/rushairer/gouno-template)):

```
my-team-template/
├── cmd/
│   ├── gouno/
│   │   ├── root.go
│   │   └── web.go
│   └── main.go              ← contains: import "{{.ModulePath}}/cmd/gouno"
├── config/
│   ├── development.yaml
│   ├── production.yaml
│   └── test.yaml
├── internal/
│   ├── domain/
│   ├── repository/
│   └── service/
├── router/
│   └── web.go
├── Makefile
└── go.mod                   ← contains: module {{.ModulePath}}
```

### 2. Add Template Variables

In files where the module path or project name is referenced (such as `go.mod`, `main.go`, `config/development.yaml`), use Go template placeholders:

```go
// go.mod
module {{.ModulePath}}

go 1.23.0
```

```go
// cmd/main.go
package main

import "{{.ModulePath}}/cmd/gouno"

func main() {
    gouno.Execute()
}
```

```yaml
# config/development.yaml
database:
    drivers:
        sqlite:
            dsn: ./data/{{.ProjectName}}_development.db
```

### 3. Publish and Share

Push your template to GitHub, GitLab, or any Git server:

```bash
git init
git add .
git commit -m "feat: initial project template"
git remote add origin https://github.com/myorg/my-team-template.git
git push -u origin main
```

Your team members can now create new microservices with:

```bash
gouno-cli new billing-service -t https://github.com/myorg/my-team-template -m github.com/myorg/billing-service
```

---

## What's Next

- [Code Generation](./code-generation.md) — Generate DDD modules in your projects
- [Configuration](./configuration.md) — Multi-environment YAML config
