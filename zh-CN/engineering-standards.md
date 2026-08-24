# Gouno 统一工程规范

## 发布与兼容性

- 各仓库独立遵循语义化版本，并维护带 `Unreleased` 的 Keep a Changelog。
- tag、包版本、镜像版本、API 文档和迁移说明必须对应同一发布；已发布 tag 不得覆盖。
- Go 项目支持当前及前一个稳定系列的最新安全补丁。提高最低 Go 版本必须在 minor 版本、README 和 CHANGELOG 中明确说明。

## 配置、API 与日志

- 环境变量使用 `GOUNO_`、`GOSSO_`、`BLOG_` 等归属前缀；生产 secret 必填且不得有默认值。
- 携带凭据的 CORS 只允许精确 HTTPS Origin；浏览器认证默认使用服务端设置的 HttpOnly Cookie 与 CSRF 防护。
- JSON 错误统一包含稳定机器码、安全消息、请求 ID 和 HTTP 状态；内部错误仅写入脱敏结构化日志。
- 日志统一 timestamp、level、service、version、request_id、event、outcome 字段，禁止记录 token、Cookie、密码、DSN 和私人数据。

## 质量与供应链

- 使用 Conventional Commits；Actions 固定完整 SHA 并使用最小权限。
- Go 门禁包含 gofmt、测试、race、vet、golangci-lint、govulncheck；Node 门禁包含 Prettier、lint、typecheck、覆盖率、构建和 npm audit。
- 生产镜像与部署依赖使用语义版本加 digest；发布物包含 SBOM、provenance 和可验证签名。
- 每仓必须具备 LICENSE、README、CHANGELOG、SECURITY、CONTRIBUTING、CODE_OF_CONDUCT、SUPPORT、RELEASE_CHECKLIST。

存在可达漏洞、敏感信息、兼容性测试失败、浮动生产依赖或未记录的公共契约变化时，PR 不得合并。
