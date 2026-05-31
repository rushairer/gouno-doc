# 模板集

[English](../template-sets.md)

模板集是 gouno 代码生成器的扩展机制。它让你自定义 `gouno gen` 的输出，无需修改 gouno 源码。

## 使用已有模板集

### 安装

```bash
# 从 git 仓库安装
gouno-cli template install gorm https://github.com/myorg/gouno-template-gorm

# 从本地目录安装
gouno-cli template install gorm /path/to/my-template-set
```

模板文件会被复制到 `~/.gouno/templates/gorm/`。

### 在项目中使用

方式一：创建项目时指定：

```bash
gouno-cli new order-service --template-set gorm -m github.com/myorg/order-service
```

这会在项目根目录生成 `.gouno.yaml`，内容为 `template-set: gorm`。此后在该项目中执行的所有 `gouno gen` 命令都会使用 gorm 模板。

方式二：每次生成时指定：

```bash
gouno gen suite user --template-set gorm
```

方式三：手动创建 `.gouno.yaml`：

```yaml
template-set: gorm
```

### 搜索优先级

生成代码时，gouno 按以下顺序查找模板：

1. **`--template-set` 参数** — 最高优先级
2. **项目根目录 `.gouno.yaml`** — 项目级默认
3. **内置默认模板** — 兜底（始终可用）

### 管理

```bash
gouno-cli template list                        # 列出已安装的模板集
gouno-cli template remove gorm                 # 删除模板集
gouno-cli template install gorm <url> --force  # 覆盖已有模板集
```

## 创建自定义模板集

### 第一步：理解文件结构

一个模板集仓库由两部分组成：

1. **`templates/` 目录** — 包含 `.tmpl` 文件（真正的模板集）
2. **项目脚手架** — 仓库的其余部分（cmd/、config/ 等），用于 `gouno-cli new` 创建项目时的模板

参考 [gouno-template](https://github.com/rushairer/gouno-template) 的结构：

```
gouno-template/                  ← 仓库 = 模板集 + 项目脚手架
├── templates/                   ← 模板集：.tmpl 文件放在这里
│   ├── domain.tmpl
│   ├── repository.tmpl
│   ├── service.tmpl
│   ├── controller.tmpl
│   └── task.tmpl
├── cmd/                         ← 项目脚手架
│   ├── main.go
│   └── gouno/
├── config/                      ← 项目脚手架
├── internal/                    ← 项目脚手架
├── Makefile
└── go.mod
```

执行 `gouno-cli template install gorm /path/to/gouno-template` 时，**只有 `templates/` 里的内容**会被复制到 `~/.gouno/templates/gorm/`。项目脚手架不会被包含。

如果你的模板集**只有模板**（没有项目脚手架），直接把 `.tmpl` 文件放在 `templates/` 目录下即可：

```
my-template-set/
└── templates/
    ├── domain.tmpl
    ├── repository.tmpl
    ├── service.tmpl
    ├── controller.tmpl
    └── task.tmpl
```

### 第二步：编写模板

```bash
mkdir -p my-template-set/templates
cd my-template-set/templates
```

创建五个模板文件。不需要全部创建——缺失的文件会自动使用内置默认模板。

每个 `.tmpl` 文件使用 `%s` 作为结构体名占位符（每个文件出现 5 次）。

**`domain.tmpl` — 带 GORM：**

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

**`repository.tmpl` — 带接口定义：**

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

**`service.tmpl` — 带接口定义：**

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

**`controller.tmpl` — Gin 处理器：**

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

**`task.tmpl` — 后台任务：**

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

### 模板变量参考

`%s` 占位符会被替换为传入名称的驼峰形式：

| 命令 | `%s` 替换为 |
|------|-----------|
| `gouno gen suite user` | `User` |
| `gouno gen suite foo_bar` | `FooBar` |
| `gouno gen suite my_order` | `MyOrder` |

每个模板中 `%s` 出现 **5 次**（结构体名、构造函数、接收者等）。

### 第三步：本地测试

```bash
# 从本地目录安装
gouno-cli template install my-set /path/to/my-template-set/templates

# 创建测试项目
gouno-cli new test-project --template-set my-set -m github.com/test/test-project
cd test-project && go mod tidy

# 生成并验证
gouno gen suite user
cat internal/domain/user.go     # 检查生成的 domain
cat internal/service/user.go    # 检查生成的 service
go build ./...                  # 验证编译通过
```

迭代流程：修改 `.tmpl` → `--force` 重新安装 → `--force` 重新生成。

### 第四步：发布

```bash
cd my-template-set
git init && git add . && git commit -m "initial template set"
git remote add origin https://github.com/myorg/my-template-set
git push -u origin main
```

其他人一条命令安装：

```bash
gouno-cli template install my-set https://github.com/myorg/my-template-set
```

### 命名建议

用描述技术栈或风格的名称：

```
gorm            — 基于 GORM 的数据访问
ent             — Ent ORM 风格
clean-arch      — Clean Architecture 风格
my-company      — 公司内部规范
```

## 模板文件参考

| 文件 | 对应命令 | 默认输出路径 |
|------|---------|------------|
| `domain.tmpl` | `gouno gen domain` | `internal/domain/` |
| `repository.tmpl` | `gouno gen repository` | `internal/repository/` |
| `service.tmpl` | `gouno gen service` | `internal/service/` |
| `controller.tmpl` | `gouno gen controller` | `controller/` |
| `task.tmpl` | `gouno gen task` | `internal/task/` |

`gouno gen suite <name>` 会依次使用 domain、repository、service 三个模板生成文件。

## 常见问题

**Q: 模板集中缺少某个文件会怎样？**

A: gouno 会自动使用内置默认模板。你只需创建想自定义的类型的模板。

**Q: 能在 `.tmpl` 文件中使用 Go 模板语法（`{{.Field}}`）吗？**

A: 不能。模板使用 `fmt.Sprintf` 和 `%s`，不是 Go 的 `text/template` 引擎。Go 代码中天然包含 `{{` 和 `}}`（如 map 字面量），会与模板解析冲突。

**Q: 模板集存储在哪里？**

A: `~/.gouno/templates/<name>/`。每个模板集是一个包含 `.tmpl` 文件的目录。

**Q: 可以有项目专属的模板吗？**

A: 不直接支持。`.gouno.yaml` 只存储模板集名称，实际模板在 `~/.gouno/templates/` 中。如果需要项目专属模板，可以为该项目创建一个模板集。

## 下一步

- [配置管理](./configuration.md) — 多环境 YAML 配置
- [中间件](./middleware.md) — 内置中间件与自定义扩展
