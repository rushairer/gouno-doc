# Go 支持政策

[English](../../standards/go-support.md)

Gouno Core、gouno-cli 与官方 gouno-template 的下一轮协调 minor 发布，将 Go 1.26.0 作为最低支持工具链版本。这是因为修复 HTTP/2 漏洞的 golang.org/x/net v0.60.0 要求 Go 1.26，也确保 gouno-cli new 能够使用本机 Go 工具链对生成的默认模板执行 go mod tidy。

当前 CI 矩阵为 Go 1.26.x 和 Go 1.27.x，覆盖前一个与当前受支持的 Go 系列。所有第一方 Go 仓库都必须在 PR 和默认分支推送时测试这两个系列的最新补丁版本。业务应用也应持续使用对应系列的最新 patch。

已经发布的产物仍遵循各自 go.mod 和[兼容性矩阵](./compatibility.md)中记录的要求。不得根据下一轮发布基线推断历史正式版本的最低 Go 版本。

未来的 minor 发布可以提高最低 Go 版本。发布说明、README、兼容性矩阵和迁移指南必须明确说明变化；新版本发布后，旧 Go 版本不再受支持。

必需 Go 质量门禁为 gofmt、tidy 后无差异、race 测试、vet、govulncheck@v1.6.0 和 golangci-lint v2.12.2。模板仓库只对新渲染的临时项目执行这些检查。
