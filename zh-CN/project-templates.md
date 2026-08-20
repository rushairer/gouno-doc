# 项目模板

[English](../project-templates.md)

项目模板（Project Template）是 `gouno-cli new` 用于初始化生成 Go Web 项目的骨架仓库。

`gouno-cli` 摒弃了复杂的本地模板集仓库维护，直接通过 `-t, --template` 参数支持任意标准的 Git 远程仓库或本地目录。

## 使用项目模板

### 默认模板

默认情况下，`gouno-cli` 会自动克隆官方的 [gouno-template](https://github.com/rushairer/gouno-template)：

```bash
gouno-cli new my-service -m github.com/you/my-service
```

### 自定义远程 Git 模板

通过 `-t` 指定任意 Git 仓库地址（支持 HTTPS 和 SSH）：

```bash
# HTTPS 协议
gouno-cli new my-service \
  -t https://github.com/myorg/custom-gouno-template \
  -m github.com/myorg/my-service

# SSH 协议
gouno-cli new my-service \
  -t git@github.com:myorg/custom-gouno-template.git \
  -m github.com/myorg/my-service
```

### 本地目录模板

通过 `-t` 指定本地已有的模板文件夹：

```bash
gouno-cli new my-service \
  -t /path/to/my-local-template \
  -m github.com/you/my-service
```

---

## 模板渲染工作机制

当运行 `gouno-cli new` 创建新项目时：

1. **克隆 / 复制**：将远程仓库克隆至临时目录，或直接读取本地目录。
2. **变量替换**：仅对包含 `{{` 占位符的文件执行 Go `text/template` 模板渲染，支持以下变量：
   - `{{.ModulePath}}`：通过 `-m` 指定的 Go module 路径（例如 `github.com/you/my-service`）。
   - `{{.ProjectName}}`：命令行传入的项目名称（例如 `my-service`）。
   不含 `{{` 的文件将原样直接复制。
3. **自动文件过滤**：复制过程中会自动跳过以下文件和目录，防止敏感信息或脚手架元数据泄露：
   - `.git/`
   - `.idea/`
   - `.DS_Store`
   - `bin/`
   - `templates/`（代码生成器脚手架模板）
   - `.env` 与 `.env.*`
   - `*.local.yaml`（本地私有配置覆盖文件）
4. **权限保护**：保留源脚本文件的可执行权限（如 `scripts/*.sh`），同时移除过度宽松的组与其他用户写权限。
5. **依赖整理**：生成完成后自动在新工程根目录执行 `go mod tidy`（可通过 `--skip-tidy` 跳过）。
6. **原子回滚**：若渲染或 `go mod tidy` 失败，会自动清理已创建的半成品目录。

---

## 创建团队自定义项目模板

为团队构建专属的基础工程模板非常简单：

### 1. 组织模板目录结构

参考 [gouno-template](https://github.com/rushairer/gouno-template) 搭建标准 DDD 结构：

```
my-team-template/
├── cmd/
│   ├── gouno/
│   │   ├── root.go
│   │   └── web.go
│   └── main.go              ← 包含：import "{{.ModulePath}}/cmd/gouno"
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
└── go.mod                   ← 包含：module {{.ModulePath}}
```

### 2. 插入模板占位符

在需要引用 module path 或项目名的文件（如 `go.mod`、`main.go`、`config/development.yaml`）中使用 Go template 占位符：

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

### 3. 发布与共享

将模板推送到 GitHub、GitLab 或内网 Git 服务器：

```bash
git init
git add .
git commit -m "feat: initial project template"
git remote add origin https://github.com/myorg/my-team-template.git
git push -u origin main
```

团队成员即可通过一行命令快速开箱使用：

```bash
gouno-cli new billing-service -t https://github.com/myorg/my-team-template -m github.com/myorg/billing-service
```

---

## 下一步

- [代码生成](./code-generation.md) — 在项目中快速生成 DDD 模块代码
- [配置管理](./configuration.md) — Viper 多环境 YAML 配置
