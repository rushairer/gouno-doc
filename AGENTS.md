# Gouno Documentation Agent Contract

This file defines documentation-governance invariants for humans and coding agents working on `rushairer/gouno-doc`.

## Documentation role

`gouno-doc` is the user-facing guide and standards repository. It explains how to use Gouno projects and how to author project templates, but it does not redefine protocol contracts owned by implementation repositories.

Normative ownership is split intentionally:

- `rushairer/gouno/docs/codegen-template-spec.md` owns the Codegen protocol/schema;
- `rushairer/gouno-cli/docs/project-template-contract.md` owns project bootstrap semantics;
- `rushairer/gouno-template` is the default reference implementation;
- this repository owns explanatory guides, shared engineering standards, and compatibility documentation.

Do not copy a normative specification here as a second source of truth. Summarize it for users and link to the authoritative repository.

## Architecture-neutral language

Gouno Core does not prescribe DDD, Clean Architecture, Gin, Cobra, Viper, database technology, or generator names.

When documentation uses `domain`, `repository`, `service`, `controller`, `task`, `suite`, Gin, Cobra, Viper, or other choices from `gouno-template`, explicitly identify them as behavior of the **default template**, not as Gouno protocol requirements.

A custom template may expose different generators or no `gen` command at all.

## Historical records

Do not rewrite historical CHANGELOG entries merely to make old terminology match current architecture. If an old entry accurately describes the released version at that time, preserve it.

Fix current-state guides, READMEs, standards, and compatibility matrices when architecture changes. Add new CHANGELOG entries for the documentation change rather than editing history.

## Bilingual contract

English and Chinese user guides are maintained as paired documents. When changing a guide under the repository root, update the corresponding `zh-CN/` guide in the same change unless the file is intentionally language-specific.

Keep terminology semantically aligned across languages; do not allow one language to imply stronger framework or architecture requirements than the other.

## Compatibility matrix

Review `standards/compatibility.md` and `zh-CN/standards/compatibility.md` after coordinated releases of `gouno`, `gouno-cli`, `gouno-template`, or other listed repositories.

Published version relationships must describe released artifacts, not branch heads or pseudo-versions.

## Template authoring guidance

Template author documentation must start from the minimum contract rather than from the default template's architecture. Explain explicitly that a valid project template can:

- use any project structure or supported technology choices;
- omit Gouno runtime helpers when it does not need them;
- omit Codegen entirely;
- define its own Codegen command tree when it opts into Codegen v1.

Always explain the two-stage template model: bootstrap rendering by `gouno-cli new`, then optional project Codegen rendering by `gouno gen`.

## Validation

Run `scripts/check-docs.sh` and all repository CI checks. Relative links, bilingual standards, workflow pinning, and current compatibility claims must remain valid.
