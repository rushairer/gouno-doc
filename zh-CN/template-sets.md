# 模板集

[English](../template-sets.md)

模板集是 gouno 代码生成器的扩展机制。它让你自定义 `gouno gen` 的输出，无需修改 gouno 源码。

模板集就是一个包含 `.tmpl` 文件的目录。每个文件是一个 Go `text/template`，用于生成一种类型的代码（domain、repository、service 等）。

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

### 第一步：创建目录结构

```bash
mkdir my-template-set
cd my-template-set
```

创建五个模板文件：

```
my-template-set/
├── domain.tmpl
├── repository.tmpl
├── service.tmpl
├── controller.tmpl
└── task.tmpl
```

不需要全部创建。只创建你想自定义的类型，缺失的文件会自动使用内置默认模板。

### 第二步：编写模板

每个 `.tmpl` 文件是一个 Go `text/template`。使用 `%s` 作为结构体名占位符（每个模板中出现 5 次）。

**最简示例 — `domain.tmpl`：**

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

**带 GORM — `domain.tmpl`：**

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

**带接口定义 — `service.tmpl`：**

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

**带接口定义 — `repository.tmpl`：**

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

**Gin 控制器 — `controller.tmpl`：**

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

**后台任务 — `task.tmpl`：**

```
package task

import "context"

type %sTask struct {
}

func New%sTask() *%sTask {
    return &%sTask{}
}

func (t *%sTask) Run(ctx context.Context) error {
    // TODO: 实现任务逻辑
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
| `gouno gen suite sendEmail` | `SendEmail` |

每个模板中 `%s` 出现 **5 次**（结构体名、构造函数、接收者等）。

### 第三步：本地测试

从本地目录安装模板集：

```bash
gouno-cli template install my-set /path/to/my-template-set
```

创建测试项目：

```bash
gouno-cli new test-project --template-set my-set -m github.com/test/test-project
cd test-project
go mod tidy
```

生成代码并验证：

```bash
gouno gen suite user
cat internal/domain/user.go     # 检查生成的 domain
cat internal/service/user.go    # 检查生成的 service
go build ./...                  # 验证编译通过
```

如果有问题，修改 `.tmpl` 文件后重新安装：

```bash
gouno-cli template install my-set /path/to/my-template-set --force
gouno gen suite user --force    # 用更新后的模板重新生成
```

### 第四步：发布

将模板集推送到 git 仓库：

```bash
cd my-template-set
git init
git add .
git commit -m "initial template set"
git remote add origin https://github.com/myorg/my-template-set
git push -u origin main
```

其他人可以一条命令安装：

```bash
gouno-cli template install my-set https://github.com/myorg/my-template-set
```

### 命名建议

模板集名称是任意的，建议用描述技术栈或风格的名称：

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

执行 `gouno gen suite <name>` 时，会依次使用 domain、repository、service 三个模板生成文件。

## 常见问题

**Q: 模板集中缺少某个文件会怎样？**

A: gouno 会自动使用内置默认模板。你只需创建想自定义的类型的模板。

**Q: 能在 `.tmpl` 文件中使用 Go 模板语法（`{{.Field}}`）吗？**

A: 不能。模板使用 `fmt.Sprintf` 和 `%s`，不是 Go 的 `text/template` 引擎。因为 Go 代码中天然包含 `{{` 和 `}}`（如 map 字面量），会与模板解析冲突。

**Q: 模板集存储在哪里？**

A: `~/.gouno/templates/<name>/`。每个模板集是一个包含 `.tmpl` 文件的目录。

**Q: 可以有项目专属的模板吗？**

A: 不直接支持。`.gouno.yaml` 只存储模板集名称，实际模板在 `~/.gouno/templates/` 中。如果需要项目专属模板，可以为该项目创建一个模板集。
