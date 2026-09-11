# Compatibility Matrix

[中文](../zh-CN/standards/compatibility.md)

This matrix records released artifacts only. Branch heads, local replacements, and pseudo-versions are not compatibility baselines.

## Current Gouno project-creation chain

| Repository release | Contract / dependency baseline | Supported Go CI |
| --- | --- | --- |
| gouno v1.3.0 | Codegen Specification `gouno.dev/codegen/v1` | 1.25.x, 1.26.x |
| gouno-template v1.3.0 | depends on gouno v1.3.0; default Codegen v1 policy | 1.25.x, 1.26.x |
| gouno-cli v1.2.1 | Project Template Contract v1; preserves Codegen v1 runtime resources | 1.25.x, 1.26.x |

The recommended released chain is therefore:

```text
gouno-cli v1.2.1
        ↓ project bootstrap
gouno-template v1.3.0
        ↓ runtime / Codegen protocol
gouno v1.3.0
```

A custom project template does not have to depend on the Gouno runtime or enable Codegen unless its own design requires those capabilities. Compatibility claims for custom templates belong to those templates.

## Other released baselines

| Repository release | Baseline | Supported Go CI |
| --- | --- | --- |
| gouno-agent-demo v0.2.0 | gouno v1.2.0 | 1.25.x, 1.26.x |
| gouno-doc v1.3.0 | current documentation / contracts baseline | n/a |

When a coordinated release changes the project-template or Codegen contracts, update this matrix from published releases rather than inferred branch state.
