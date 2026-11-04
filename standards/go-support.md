# Go Support Policy

[中文](../zh-CN/standards/go-support.md)

The next coordinated minor releases of Gouno Core, gouno-cli, and the official gouno-template use Go 1.26.0 as their minimum supported toolchain. This is required by the patched golang.org/x/net v0.60.0 dependency and ensures that gouno-cli new can run go mod tidy against the generated default template.

The current CI matrix is Go 1.26.x and Go 1.27.x, covering the previous and current supported Go series. Every first-party Go repository must test the latest patch release in both series on pull requests and default-branch pushes. Reusable workflows must set `actions/setup-go` `check-latest: true`; otherwise a GitHub-hosted runner's preinstalled toolchain cache can satisfy `1.26.x` with an older vulnerable patch even when a fixed patch has already been released. Applications should keep their patch release current.

Already-published artifacts retain the requirements in their own go.mod files and the [Compatibility Matrix](./compatibility.md). Do not infer the minimum version of a released artifact from the next-release baseline documented here.

A future minor release may raise the minimum supported Go version. The release notes, README, compatibility matrix, and migration guidance must state the change; older Go versions are unsupported after that release.

Required Go quality gates are gofmt, tidy-without-diff, race tests, vet, govulncheck@v1.6.0, and golangci-lint v2.15.0. Template repositories run these checks only against a freshly rendered temporary project.
