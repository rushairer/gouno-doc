# Go 支持政策

[English](../../standards/go-support.md)

Gouno v1.2.0 将最低支持版本确立为 Go 1.25.0。每个 PR 与默认分支推送均测试 Go 1.25 和 Go 1.26 的最新安全补丁版本；应用应持续使用对应系列的最新 patch。

新的 minor 发布可以提高最低 Go 版本。发布说明、README、兼容性矩阵和迁移说明必须明确该变化；发布后较旧 Go 版本不再受支持。

必需 Go 质量门禁为 `gofmt`、tidy 后无差异、race 测试、vet、`govulncheck@v1.6.0` 和 `golangci-lint v2.12.2`。模板仓库只对新渲染的临时项目执行这些检查。
