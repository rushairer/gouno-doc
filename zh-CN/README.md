# gouno 文档

[English](../README.md)

---

Gouno 将项目 Bootstrap、可复用运行时/工具机制以及项目自身策略明确分开：

```text
gouno-cli       Project Template Bootstrap 机制
gouno           可复用机制 + Codegen 协议/运行时
gouno-template  官方默认项目/Template 策略
gouno-doc       用户指南 + 工程/兼容性规范
```

官方 `gouno-template` 是参考实现。它选择的 Gin、Cobra、Viper、分层架构以及具体 Generator 名称，都不是 Gouno Core 对所有项目的强制要求。

## 指南

- [快速开始](./getting-started.md) — 安装 CLI、创建项目并运行默认模板
- [项目模板](./project-templates.md) — 选择、固定版本并使用完整 Project Template
- [Template 开发指南](./template-authoring.md) — 设计、验证并发布自己的 Gouno Project Template
- [代码生成](./code-generation.md) — 使用 Template 定义的 Codegen 能力
- [配置管理](./configuration.md) — 默认 Template 的配置行为
- [中间件](./middleware.md) — 可复用中间件与默认 Template 接线
- [工程规范](./standards/engineering.md) — 共享仓库与 CI 规范
- [Go 支持策略](./standards/go-support.md) — 支持的 Go 版本与质量门禁
- [发布规范](./standards/release.md) — 不可变发布与分支保护要求
- [兼容性矩阵](./standards/compatibility.md) — 已发布仓库版本组合

## 权威契约

本仓库的用户指南负责解释，不重新定义协议：

- Codegen 协议/Schema：[`rushairer/gouno/docs/codegen-template-spec.md`](https://github.com/rushairer/gouno/blob/main/docs/codegen-template-spec.md)
- Project Bootstrap 语义：[`rushairer/gouno-cli/docs/project-template-contract.md`](https://github.com/rushairer/gouno-cli/blob/main/docs/project-template-contract.md)

## 相关仓库

| 仓库 | 说明 |
|------|------|
| [gouno](https://github.com/rushairer/gouno) | 可复用机制以及 Codegen 协议/运行时 |
| [gouno-cli](https://github.com/rushairer/gouno-cli) | 与架构无关的 Project Template Bootstrap CLI |
| [gouno-template](https://github.com/rushairer/gouno-template) | 官方默认 Template 与参考 Codegen Policy |
