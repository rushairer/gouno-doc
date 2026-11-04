# 发布规范

[English](../../standards/release.md)

创建发布 tag 前，工作区必须 clean，`git diff --check` 和全部必需 CI 必须通过，目标 tag 与 GitHub Release 均不得已存在。带日期的 CHANGELOG 条目必须说明面向用户和安全相关变化。tag、包和镜像 manifest 均不可变，绝不覆盖。

每个 workflow 在 `main` 至少成功运行一次后，在 GitHub 保护 `main`：`Settings` → `Branches` → `main` 规则 → 要求 PR、要求已更新的必需状态检查，选择质量检查和 Conventional PR 标题检查，并禁止 force push。

## 多仓库协调发布

将跨仓库发布视为依赖图，必须按拓扑顺序发布：先发布依赖，再发布消费者。当前兼容性矩阵记录的 `gouno-cli → gouno-template → gouno` 链，实际发布顺序应为 **Gouno Core → 默认 Template → CLI**。

- 禁止消费者指向尚未发布的版本、浮动分支或仅供开发使用的 pseudo-version 后就创建 tag 或发布。
- 依赖 tag 正式存在后，消费者才能将 `go.mod` 和 `go.sum` 更新到该精确发布版本；随后执行 `go mod tidy`，通过完整的 Go 支持矩阵和渲染后模板验证，最后才能发布消费者。
- 消费者可以有意继续使用较早的已发布依赖，但必须在 CHANGELOG 和兼容性矩阵中明确记录该选择。
- 只有对应 tag/package 已公开发布后，才能更新兼容性矩阵。记录精确版本、源码 commit、最低 Go 版本、测试的 Go 系列及依赖链；计划中的版本不得提前写成已发布条目。
- 如果发布提高最低 Go 版本，必须在同一发布列车中同步 README、CONTRIBUTING、发布清单、迁移指南和兼容性矩阵。

对于默认模板，下一版若要采用更新的 Gouno Core，必须等待 Core tag 发布；随后将生成项目的 Core 依赖更新到精确版本，并在 Go 1.26.x 与 1.27.x 上验证全新渲染的项目，之后才能发布模板。
