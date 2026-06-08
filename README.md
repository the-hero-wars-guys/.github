# .github

[![Repo CI](https://github.com/the-hero-wars-guys/.github/actions/workflows/repo-ci.yml/badge.svg)](https://github.com/the-hero-wars-guys/.github/actions/workflows/repo-ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Default GitHub metadata for repositories owned by
[the-hero-wars-guys](https://github.com/the-hero-wars-guys).

## Purpose

This is the special account-level `.github` repository for the personal
`the-hero-wars-guys` organization. It exists to hold durable defaults that GitHub can reuse
across repositories when a repository does not define its own local version.

## Inherited Defaults

GitHub can reuse the following files from this repository:

| File | Purpose |
|------|---------|
| `CODE_OF_CONDUCT.md` | Default community standards |
| `CONTRIBUTING.md` | Default contribution guidance |
| `SECURITY.md` | Default vulnerability reporting instructions |
| `SUPPORT.md` | Default support routing |
| `.github/FUNDING.yml` | Default sponsorship configuration |
| `.github/ISSUE_TEMPLATE/` | Default issue forms and issue chooser config |
| `.github/pull_request_template.md` | Default pull request template |

## Repo-Local Only

The following files in this repository are important here, but are not
inherited by other repositories:

| File | Why it stays local |
|------|--------------------|
| `README.md` | Documents the operating model of this special repo |
| `LICENSE` | Each repository needs its own license file |
| `.github/workflows/` | These workflows validate this repo itself |

## Dependency Updates

This repository tracks dependency updates via Renovate, the org standard per
[ADR-0004](docs/decision-records/0004-use-renovate-for-dependency-updates.md).
Dependabot **version** updates are not used anywhere under the account — Renovate
opens all version-bump PRs. Dependabot **security** alerts and security updates
remain enabled as a separate safety net.

Per ADR-0004, this org `.github` repository carries its own `.github/renovate.json5`
that governs **only its own** dependencies — the `github-actions` SHA pins in its
reusable workflows — so the org repo's own supply chain stays current. This is
**not** an org-level baseline: no consumer extends it. Consumers extend their
type-template's baseline (e.g.
`NWarila/packer-framework-template/.github/renovate.json5`); there is no _shared_
org Renovate config.

## Override Rules

If a repository has its own version of an inherited file, the local file wins.
GitHub does not merge local and default content.

Repositories that adopt this org baseline through `drift-gate` intentionally
commit local copies of selected inherited files and keep them byte-identical to
this repository's `baseline-manifest.json`. Repo-specific procedure belongs in
that repository's `docs/` tree rather than in drift-gated community-health
files.

For issue templates specifically: if a repository has anything in its own
`.github/ISSUE_TEMPLATE/` directory, GitHub ignores the entire default issue
template directory from this repo for that repository.

## Change Discipline

Changes here can affect every repository under this account that does not have
local overrides. Before merging:

1. Verify policy files and templates still point to the right routes.
2. Test issue form changes in GitHub before broad rollout.
3. Ensure repo CI passes.

## Documentation Rule

Keep durable operating guidance in this `README.md`.

Do not keep temporary planning artifacts in this repository. If a future change
creates a real long-lived architectural decision, capture the rationale in
`docs/decision-records/` at that time instead of maintaining a standing plan document.

## Namespace Mirror

This repository mirrors the namespace-local governance surface from
`NWarila/.github@791fe6af86fcccf8de807a09b9f7c8f38f268532`. The namespace-local
control-plane rule is captured in
[ADR-0006](docs/decision-records/0006-keep-github-control-planes-namespace-local.md),
and the universal reusable workflow placement rule is captured in
[ADR-0007](docs/decision-records/0007-centralize-universal-ci-reusables-within-each-namespace.md).

`workflow-sync-manifest.json` and `tools/apply_workflow_sync_manifest.py` keep
mirrored workflow bodies, policies, tools, docs, and community-health files
aligned with the upstream source pin while applying the owner rewrites declared
in the manifest. The sync manifest is independent of drift-gate's v1/v2
manifest schema.

### Consumer Caller Stub

```yaml
name: Repo Hygiene
on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  repo-hygiene:
    uses: the-hero-wars-guys/.github/.github/workflows/reusable-repo-hygiene.yaml@<40-character-sha>
    with:
      source_ref: <same-40-character-sha>
```

## License

[MIT](LICENSE)
