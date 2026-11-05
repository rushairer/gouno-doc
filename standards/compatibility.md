# Compatibility Matrix

[中文](../zh-CN/standards/compatibility.md)

This matrix records released artifacts only. Branch heads, local replacements, and pseudo-versions are not compatibility baselines.

## Coordinated project-creation chain

| Repository release | Contract / dependency baseline | Supported Go CI | Verified release commit |
| --- | --- | --- | --- |
| [gouno v1.4.0](https://github.com/rushairer/gouno/releases/tag/v1.4.0) | Stable Codegen Specification `gouno.dev/codegen/v1`; Go 1.26 minimum; patched HTTP/2 dependency baseline | 1.26.x, 1.27.x | `20efba0af181cb3e03c5bcb199576bfcdec1bd7f` |
| [gouno-template v1.4.0](https://github.com/rushairer/gouno-template/releases/tag/v1.4.0) | Core v1.4.0; default Flat Layered profile and template-owned Codegen v1 policy | 1.26.x, 1.27.x | `9f0cba9c8a6be6331f48596c83663efbec5490a2` |
| [gouno-cli v1.3.0](https://github.com/rushairer/gouno-cli/releases/tag/v1.3.0) | Project Template Contract v1; live-default and pinned Template v1.4.0 Bootstrap with verbatim Codegen resources | 1.26.x, 1.27.x | `087c00a523a6ec8c512d5eb9c65f657f6be8d5fb` |

The recommended released chain is:

```text
gouno-cli v1.3.0
        ↓ project bootstrap
gouno-template v1.4.0
        ↓ runtime / Codegen protocol
gouno v1.4.0
```

Both supported Go series passed tidy, individual/composition generation, race and vet in the CLI integration gate. Template CI additionally passed lint and govulncheck on Go 1.26.10 and 1.27.3. Core and CLI resolve through the public Go module proxy. Template's root `go.mod` is a bootstrap template, not a publishable Go module.

A custom project template does not have to depend on the Gouno runtime or enable Codegen unless its own design requires those capabilities. Compatibility claims for custom templates belong to those templates.

## Other released baselines

| Repository release | Published relationship / acceptance boundary |
| --- | --- |
| [Gosso v1.6.1](https://github.com/rushairer/gosso/releases/tag/v1.6.1) | Released identity-provider baseline; the new global administrator OAuth2 client-governance API is not part of this version |
| [GOSSO Admin v0.7.24](https://github.com/rushairer/gosso-admin/releases/tag/v0.7.24) | Last released Admin; candidate 0.7.25 is excluded until certification and release acceptance pass |
| [Gouno Blog v1.5.26](https://github.com/rushairer/gouno-blog/releases/tag/v1.5.26) | Last released Blog; newer main-branch BFF compatibility evidence against Gosso v1.6.1 does not establish a new Blog release |
| [@gouno/ui v0.4.9](https://github.com/rushairer/gouno-ui/releases/tag/v0.4.9) | Published canonical UI npm package; Showcase-only changes do not imply a new package version |
| @gosso/client v0.9.3 | Published npm client used by the current consumers; application release acceptance remains separate |
| [gouno-agent-demo v0.3.0](https://github.com/rushairer/gouno-agent-demo/releases/tag/v0.3.0) | Core v1.4.0; Go 1.26.x / 1.27.x; Agent, SSE and provider adapter tests |
| [gouno-doc v1.3.0](https://github.com/rushairer/gouno-doc/releases/tag/v1.3.0) | Last released documentation baseline |

Agent Demo v0.3.0 is now published independently of the main chain at `ca372fc72379dbf63e6794f5d4e65af7c88e8ba7`. Its historical changelog entry v0.2.0 had no public tag or GitHub Release and remains excluded from the formal baseline.

When a coordinated release changes project-template or Codegen contracts, update this matrix from published artifacts and exact integration evidence. Do not promote Gosso or Blog candidates here before their releases exist.
