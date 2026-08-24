# 工程规范

[English](../../standards/engineering.md)

所有 Gouno 仓库使用 Conventional Commit 风格的 PR 标题和 Keep a Changelog。任何面向用户的行为、公开配置、生成结果或兼容性变化，均须在发布前记录到 `Unreleased`。

GitHub Actions 必须使用完整 commit SHA、最小权限和并发取消策略。仓库为受支持的包生态启用每周 Dependabot 更新。生产引用必须使用不可变发布版本和镜像 digest；分支与浮动 tag 不是发布输入。

首批强制接入仓库为 `gouno-template`、`gouno-agent-demo` 和 `gouno-cli`。它们必须通过已发布 Gouno Docs 版本的完整 commit SHA 调用本仓库的 reusable workflow。
