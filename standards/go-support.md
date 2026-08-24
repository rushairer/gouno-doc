# Go Support Policy

[中文](../zh-CN/standards/go-support.md)

Gouno v1.2.0 establishes Go 1.25.0 as the minimum supported version. Go repositories test the latest security patch of Go 1.25 and Go 1.26 on every pull request and default-branch push. Applications should keep their patch release current.

A new minor release may raise the minimum supported Go version. The release notes, README, compatibility matrix, and migration guidance must state the change; older Go versions are unsupported after that release.

Required Go quality gates are `gofmt`, tidy-without-diff, race tests, vet, `govulncheck@v1.6.0`, and `golangci-lint v2.12.2`. Template repositories run these checks only against a freshly rendered temporary project.
