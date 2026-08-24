# 发布规范

[English](../../standards/release.md)

创建发布 tag 前，工作区必须 clean，`git diff --check` 和全部必需 CI 必须通过，目标 tag 与 GitHub Release 均不得已存在。带日期的 CHANGELOG 条目必须说明面向用户和安全相关变化。tag、包和镜像 manifest 均不可变，绝不覆盖。

每个 workflow 在 `main` 至少成功运行一次后，在 GitHub 保护 `main`：`Settings` → `Branches` → `main` 规则 → 要求 PR、要求已更新的必需状态检查，选择质量检查和 Conventional PR 标题检查，并禁止 force push。
