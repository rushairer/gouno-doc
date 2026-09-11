# 兼容性矩阵

[English](../../standards/compatibility.md)

本矩阵只记录**已经发布的正式产物**。分支 HEAD、本地 `replace` 和 pseudo-version 都不是兼容性基线。

## 当前 Gouno 项目创建链

| 仓库发布版本 | 契约 / 依赖基线 | 支持的 Go CI |
| --- | --- | --- |
| gouno v1.3.0 | Codegen Specification `gouno.dev/codegen/v1` | 1.25.x、1.26.x |
| gouno-template v1.3.0 | 依赖 gouno v1.3.0；默认 Codegen v1 Policy | 1.25.x、1.26.x |
| gouno-cli v1.2.1 | Project Template Contract v1；保留 Codegen v1 Runtime Resources | 1.25.x、1.26.x |

因此当前推荐的正式发布链为：

```text
gouno-cli v1.2.1
        ↓ Project Bootstrap
gouno-template v1.3.0
        ↓ Runtime / Codegen Protocol
gouno v1.3.0
```

自定义 Project Template 不要求必须依赖 Gouno Runtime，也不要求必须启用 Codegen；是否使用这些能力由 Template 自己决定。自定义 Template 的版本兼容声明也应由对应 Template 自己维护。

## 其它已发布基线

| 仓库发布版本 | 基线 | 支持的 Go CI |
| --- | --- | --- |
| gouno-agent-demo v0.2.0 | gouno v1.2.0 | 1.25.x、1.26.x |
| gouno-doc v1.2.0 | reusable CI / 工程规范 | 不适用 |

当协调发布改变 Project Template 或 Codegen Contract 时，应依据已经发布的正式版本更新本矩阵，而不是根据分支状态推断。
