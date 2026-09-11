# Gouno Architecture Profiles

[中文](./zh-CN/architecture-profiles.md)

Gouno Core does not prescribe an application architecture. Project Templates and projects own their directory layout, dependency boundaries, and Codegen policy.

For the official Gouno ecosystem, two reference profiles cover the common cases without turning architecture into Core behavior:

- **Flat Layered** for simpler applications;
- **Capability Module** for complex applications with multiple business capabilities.

These are recommended project/template conventions, not protocol requirements. A custom template may use another architecture when its project needs justify it.

## 1. Flat Layered

Use **Flat Layered** when the application has a small number of business areas and the global layers remain easy to navigate.

Typical layout:

```text
internal/
├── domain/
├── repository/
├── service/
└── controller/
```

Typical ownership is by implementation layer first:

```text
internal/domain/user.go
internal/repository/user.go
internal/service/user.go
internal/controller/user.go
```

This profile favors low ceremony and obvious layer boundaries. It is a good default for small APIs, CRUD-oriented services, internal tools, and applications whose business surface is still compact.

The official [`gouno-template`](https://github.com/rushairer/gouno-template) is the reference implementation of this profile. Its concrete generator catalog is template policy, not a Gouno Core API.

### Codegen convention

A Flat Layered project may expose generators such as:

```text
domain
repository
service
controller
suite
```

`suite` is a composition action in the default template. It does not define an architecture by itself and must not be reinterpreted as Capability Module generation.

## 2. Capability Module

Use **Capability Module** when the application has multiple substantial business areas, global layer directories become ownership buckets, or teams frequently need to reason about one business capability as a coherent unit.

Typical layout:

```text
internal/
├── account/
│   ├── domain/
│   ├── repository/
│   ├── service/
│   └── controller/
├── article/
│   ├── domain/
│   ├── repository/
│   ├── service/
│   └── controller/
└── media/
    └── ...
```

Ownership is capability first, implementation layer second:

```text
internal/<capability>/<layer>/
```

A capability contains only the layers it actually needs. Infrastructure capabilities, adapters, observability, encryption, or test-support packages must not create empty `domain`, `repository`, `service`, or `controller` packages merely for symmetry.

`module.go` or another composition root is optional. Add one only when the capability actually needs explicit dependency assembly.

### Dependency direction

Inside a business capability, prefer inward dependencies such as:

```text
controller -> service -> repository
                |          |
                +-> domain <-+
```

Cross-capability dependencies should target narrow, stable APIs. Do not solve cross-capability reuse by moving business behavior back into global layer buckets.

### Codegen convention

A Capability Module project may expose a distinct generator such as:

```text
module
```

that creates a capability skeleton under `internal/<capability>/`.

The generator should remain conservative. Do not automatically generate database access, migrations, routes, dependency injection, security policy, cross-capability imports, or mandatory composition files unless those conventions have been proven by the project and are intentionally part of its Codegen policy.

## 3. Choosing a profile

Prefer **Flat Layered** when most of these are true:

- the project has few business areas;
- global layers are still easy to navigate;
- most changes touch a small number of layer files;
- team/domain ownership is simple;
- the extra directory depth of capability modules would add more ceremony than clarity.

Prefer **Capability Module** when most of these are true:

- the project has many business capabilities or bounded contexts;
- global `service`, `repository`, or `controller` directories have become large ownership buckets;
- one feature routinely spans domain, persistence, service, and HTTP behavior;
- cross-team or cross-domain ownership needs to be explicit;
- the project is already developing capability-specific infrastructure and composition rules.

Do not switch profiles merely because a project has reached a certain file count. The decision is about ownership clarity and dependency locality.

## 4. Migration rule

When a Flat Layered project evolves into Capability Module organization, migrate incrementally by coherent capability slices:

1. identify the capability and its real ownership boundary;
2. separate genuinely shared infrastructure from business-specific code;
3. move canonical implementation into `internal/<capability>/...`;
4. retain narrow compatibility facades when moving all consumers at once would create unnecessary blast radius;
5. move tests with the canonical implementation so coverage remains meaningful;
6. update consumers gradually;
7. remove legacy facades and global ownership buckets only after no real business ownership remains there.

Do not perform filename-only moves. A file named `category_repository.go` may still contain multiple responsibilities and must be decomposed before it can become a clean capability repository.

## 5. Relationship to Gouno Core and Codegen

The architecture profile belongs to the project/template.

Gouno Core owns reusable mechanisms and the Codegen protocol/runtime. It must not contain `Flat Layered`, `Capability Module`, `domain`, `repository`, `service`, `controller`, `suite`, or `module` as mandatory application concepts.

A project's `.gouno/codegen.yaml`, when present, should express the architecture the project actually uses. Changing project architecture and leaving generator output paths unchanged is architecture drift and should be treated as a contract bug.

## References

- [Template Authoring](./template-authoring.md)
- [Code Generation](./code-generation.md)
- [Official default Flat Layered template](https://github.com/rushairer/gouno-template)
- [Gouno Codegen Specification v1](https://github.com/rushairer/gouno/blob/main/docs/codegen-template-spec.md)
