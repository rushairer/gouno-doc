# 兼容性矩阵

[English](../../standards/compatibility.md)

本矩阵只记录**已经发布的正式产物**。分支 HEAD、本地 `replace` 和 pseudo-version 都不是兼容性基线。

## 协调发布的项目创建链

| 仓库发布版本 | 契约 / 依赖基线 | 支持的 Go CI | 已验证发布提交 |
| --- | --- | --- | --- |
| [gouno v1.4.0](https://github.com/rushairer/gouno/releases/tag/v1.4.0) | 稳定 Codegen Specification `gouno.dev/codegen/v1`；最低 Go 1.26；已修补 HTTP/2 依赖基线 | 1.26.x、1.27.x | `20efba0af181cb3e03c5bcb199576bfcdec1bd7f` |
| [gouno-template v1.4.0](https://github.com/rushairer/gouno-template/releases/tag/v1.4.0) | Core v1.4.0；默认 Flat Layered 架构及模板自有 Codegen v1 Policy | 1.26.x、1.27.x | `9f0cba9c8a6be6331f48596c83663efbec5490a2` |
| [gouno-cli v1.3.0](https://github.com/rushairer/gouno-cli/releases/tag/v1.3.0) | Project Template Contract v1；验证默认分支及固定 Template v1.4.0 Bootstrap，原样保留 Codegen 资源 | 1.26.x、1.27.x | `087c00a523a6ec8c512d5eb9c65f657f6be8d5fb` |

推荐的正式发布链为：

```text
gouno-cli v1.3.0
        ↓ Project Bootstrap
gouno-template v1.4.0
        ↓ Runtime / Codegen Protocol
gouno v1.4.0
```

CLI 集成门禁在两个 Go 系列均通过 tidy、单项/组合生成、Race 和 Vet。Template CI 还在 Go 1.26.10、1.27.3 通过 Lint 与 govulncheck。Core 和 CLI 均可由公开 Go Module Proxy 解析。Template 根目录的 `go.mod` 是 Bootstrap 模板，不是应发布的 Go Module。

自定义 Project Template 不要求必须依赖 Gouno Runtime 或启用 Codegen；是否使用这些能力由 Template 自己决定。自定义 Template 的兼容声明也由对应 Template 自己维护。

## 其它已发布基线

| 仓库发布版本 | 正式发布关系 / 验收边界 |
| --- | --- |
| [Gosso v1.6.1](https://github.com/rushairer/gosso/releases/tag/v1.6.1) | 已发布身份服务基线；不包含新增的管理员 OAuth2 Client 全局治理 API |
| [GOSSO Admin v0.7.24](https://github.com/rushairer/gosso-admin/releases/tag/v0.7.24) | 最近正式 Admin；候选 0.7.25 在认证及发布验收通过前不列为正式基线 |
| [Gouno Blog v1.5.26](https://github.com/rushairer/gouno-blog/releases/tag/v1.5.26) | 最近正式 Blog；新 main 对 Gosso v1.6.1 的 BFF 验收证据不构成新 Blog 发布 |
| [@gouno/ui v0.4.9](https://github.com/rushairer/gouno-ui/releases/tag/v0.4.9) | 已发布的 Canonical UI npm 包；Showcase 改动不等于 npm 包版本变化 |
| @gosso/client v0.9.3 | 当前消费者使用的已发布 npm Client；应用版本仍须独立验收 |
| [gouno-doc v1.3.0](https://github.com/rushairer/gouno-doc/releases/tag/v1.3.0) | 最近正式文档基线 |

审计时 Agent Demo 的历史 CHANGELOG v0.2.0 没有公开 Tag 或 GitHub Release，因此不属于正式兼容基线。它对 Core v1.4.0 的升级独立于主发布链维护。

协调发布改变 Project Template 或 Codegen Contract 时，应依据正式产物及确切集成证据更新矩阵。Gosso、Blog 候选版本在实际发布前不得列为正式版本。
