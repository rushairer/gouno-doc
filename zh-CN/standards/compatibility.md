# 兼容性矩阵

[English](../../standards/compatibility.md)

本矩阵只记录**已经发布的正式产物**。分支 HEAD、本地 `replace` 和 pseudo-version 都不是兼容性基线。

## 最新独立 Core 正式版本

| 仓库发布版本 | 契约 / 依赖基线 | 支持的 Go CI |
| --- | --- | --- |
| gouno v1.4.0 | 稳定版 Codegen Specification `gouno.dev/codegen/v1`；最低 Go 1.26；HTTP/2 依赖安全基线 | 1.26.x、1.27.x |

Gouno Core v1.4.0 已作为 Go module 公开发布，Tag 指向经过审核的正式发布提交。GitHub Release 页面可以单独补发；公开 Go module proxy 已经验证可正常解析该版本。

## 最新完整协调的项目创建链

| 仓库发布版本 | 契约 / 依赖基线 | 支持的 Go CI |
| --- | --- | --- |
| gouno v1.3.0 | Codegen Specification `gouno.dev/codegen/v1` | 1.25.x、1.26.x |
| gouno-template v1.3.0 | 依赖 gouno v1.3.0；默认 Codegen v1 Policy | 1.25.x、1.26.x |
| gouno-cli v1.2.1 | Project Template Contract v1；保留 Codegen v1 Runtime Resources | 1.25.x、1.26.x |

因此，目前完整协调的正式发布链仍然是：

```text
gouno-cli v1.2.1
        ↓ Project Bootstrap
gouno-template v1.3.0
        ↓ Runtime / Codegen Protocol
gouno v1.3.0
```

较新的独立 Core v1.4.0 尚未被已发布的 Template/CLI 链消费。只有在 gouno-template v1.4.0 和 gouno-cli v1.3.0 正式打 Tag 且集成门禁通过后，完整协调发布链才会升级。

自定义 Project Template 不要求必须依赖 Gouno Runtime，也不要求必须启用 Codegen；是否使用这些能力由 Template 自己决定。自定义 Template 的版本兼容声明也应由对应 Template 自己维护。

## 其它已发布基线

| 仓库发布版本 | 基线 | 支持的 Go CI |
| --- | --- | --- |
| gouno-agent-demo v0.2.0 | gouno v1.2.0 | 1.25.x、1.26.x |
| gouno-doc v1.3.0 | 当前文档 / 契约基线 | 不适用 |

当协调发布改变 Project Template 或 Codegen Contract 时，应依据已经发布的正式版本更新本矩阵，而不是根据分支状态推断。
