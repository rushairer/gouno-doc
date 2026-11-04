# Release Standard

[中文](../zh-CN/standards/release.md)

Before tagging a release, the worktree must be clean, `git diff --check` and all required CI checks must pass, and the target tag and release must not already exist. A dated CHANGELOG entry must explain user-visible and security changes. Tags, packages, and image manifests are immutable and are never overwritten.

After each workflow has passed once on `main`, protect `main` in GitHub: `Settings` → `Branches` → rule for `main` → require a pull request, require up-to-date required status checks, select the quality and Conventional PR title checks, and disallow force pushes.

## Coordinated multi-repository releases

Treat a release train as a dependency graph and publish in topological order: dependencies first, consumers afterward. For the currently documented `gouno-cli → gouno-template → gouno` chain, the release order is **Gouno Core → default Template → CLI**.

- Never tag or publish a consumer against an unpublished version, a moving branch, or a pseudo-version intended only for development.
- After the dependency tag exists, update each consumer's `go.mod` and `go.sum` to the exact released tag, run `go mod tidy`, and pass the complete supported Go matrix plus rendered-template verification before tagging that consumer.
- A consumer may intentionally remain on an earlier released dependency, but that choice must be explicit and recorded in its CHANGELOG and the compatibility matrix.
- Update the Compatibility Matrix only after the corresponding tag/package is publicly available. Record the exact version, source commit, minimum Go version, tested Go series, and dependency chain. Planned versions must not appear as released rows.
- If a release raises the minimum Go version, synchronize README, CONTRIBUTING, release checklist, migration guidance, and the compatibility row as part of the same release train.

For the default template, this means the next template release that adopts a newer Gouno Core must wait for the Core tag, then update the generated project's exact Core dependency and verify freshly rendered projects on Go 1.26.x and 1.27.x before publishing the template.
