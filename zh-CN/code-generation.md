# 代码生成

[English](../code-generation.md)

gouno 的代码生成器从模板创建 DDD 结构的模块，省去每个新实体、服务或任务都要写的样板代码。

## 生成完整模块

`suite` 命令一步生成 domain、repository 和 service 文件：

```bash
gouno gen suite user
```

输出：

```
internal/
├── domain/user.go         ← 实体结构体
├── repository/user.go     ← 数据访问接口
└── service/user.go        ← 业务逻辑接口
```

## 单独生成文件

```bash
gouno gen domain order              # → internal/domain/order.go
gouno gen repository order          # → internal/repository/order.go
gouno gen service order             # → internal/service/order.go
gouno gen controller order          # → controller/order.go
gouno gen task send_email           # → internal/task/send_email.go
```

## 命令别名

```bash
gouno gen d order       # domain
gouno gen r order       # repository
gouno gen s order       # service
gouno gen c order       # controller
gouno gen t send_email  # task
```

## 选项

所有生成命令支持：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--path, -p` | 输出目录 | 根据类型不同（见下表） |
| `--force, -f` | 覆盖已有文件 | false |
| `--template-set` | 使用的模板集 | 从 .gouno.yaml 读取或使用内置默认 |

默认输出路径：

| 类型 | 默认路径 |
|------|---------|
| domain | `internal/domain/` |
| repository | `internal/repository/` |
| service | `internal/service/` |
| controller | `controller/` |
| task | `internal/task/` |

## 示例

```bash
# 自定义输出路径
gouno gen suite user --path ./pkg/user

# 强制覆盖已有文件
gouno gen suite user --force

# 使用指定模板集
gouno gen suite user --template-set gorm

# 只生成 domain 实体
gouno gen domain product
```

## 命名规则

传入的名称会自动转为驼峰命名作为结构体名：

```bash
gouno gen suite foo_bar    # → struct FooBar, FooBarService, FooBarRepository
gouno gen suite my_order   # → struct MyOrder, MyOrderService, MyOrderRepository
gouno gen suite user       # → struct User, UserService, UserRepository
```

## 下一步

- [模板集](./template-sets.md) — 自定义生成的代码风格
