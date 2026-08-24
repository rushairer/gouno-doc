# Release Standard

[中文](../zh-CN/standards/release.md)

Before tagging a release, the worktree must be clean, `git diff --check` and all required CI checks must pass, and the target tag and release must not already exist. A dated CHANGELOG entry must explain user-visible and security changes. Tags, packages, and image manifests are immutable and are never overwritten.

After each workflow has passed once on `main`, protect `main` in GitHub: `Settings` → `Branches` → rule for `main` → require a pull request, require up-to-date required status checks, select the quality and Conventional PR title checks, and disallow force pushes.
