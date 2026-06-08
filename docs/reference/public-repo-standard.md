# NWarila Public Repo Standard v1

The bar every public `NWarila` repository is held to. It exists so a staff/
principal engineer landing cold on any repo can, in under a minute, understand
what it is, trust how it is built, and reproduce it. Each rule is grounded in a
primary source (linked) or a portfolio ADR.

> **How to read this.** **MUST** = required for conformance; **SHOULD** =
> expected unless an ADR records why not. The [conformance checklist](#conformance-checklist)
> at the end is the per-repo scorecard.

## 1. README

A reader should never have to open the file tree to understand the repo.

- **MUST** open with: one-sentence *what*, a *why it exists*, and a badge row
  (CI status, OpenSSF Scorecard where published, License; plus "Use this
  template" for template repos).
- **MUST** include a **Quickstart** (the shortest path to a working result) and,
  for templates, the "Use this template" → rename steps.
- **MUST** include an **architecture** explanation *or* an embedded/linked
  diagram (see §5), and a **Documentation** section linking the `docs/` genres.
- **SHOULD** state the **security model** in-README (what is and is not in scope)
  and link `SECURITY.md`.

## 2. CI baseline

- **MUST** set a least-privilege top-level `permissions:` on every workflow
  (`contents: read` or `{}`), and elevate per-job only to the exact scopes
  needed. When any permission is named, unspecified scopes default to none.
  [docs.github.com — controlling GITHUB_TOKEN permissions](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/controlling-permissions-for-github_token)
- **MUST** pin every third-party and cross-repo `uses:` to a full 40-char commit
  SHA with a `# vX.Y.Z` comment. [docs.github.com — secure use](https://docs.github.com/en/actions/reference/security/secure-use)
- **MUST** set `timeout-minutes` on every job (default is 6h) and a `concurrency`
  group on any state-mutating workflow (`cancel-in-progress: false` for
  deploy/release; `true` for PR validation).
  [timeouts](https://docs.github.com/en/actions/reference/limits) ·
  [concurrency](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/control-the-concurrency-of-workflows-and-jobs)
- **MUST** call the namespace's universal reusable workflows by SHA rather than
  duplicating them (org ADR-0007); **SHOULD** consume CodeQL, OpenSSF Scorecard,
  and IaC-security (Trivy/Gitleaks/zizmor) reusables.
- **MUST NOT** check out untrusted code in a `pull_request_target`/`workflow_run`
  job, and **MUST** isolate any such trigger in its own minimal workflow file.
  [secure use](https://docs.github.com/en/actions/reference/security/secure-use)
- **SHOULD** never interpolate `github.event.*` into `run:`; pass via `env:`.
- **SHOULD** use OIDC (`id-token: write` + cloud login) over long-lived secrets,
  scoping the trust policy by `job_workflow_ref`.
  [OIDC reference](https://docs.github.com/actions/reference/openid-connect-reference)

## 3. Security baseline

- **MUST** protect `main` with a ruleset (rulesets, not classic protection):
  required PR + code-owner review, signed commits, linear history, no
  force-push. [about rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- **MUST** enforce **`required_status_checks`** so the repo's blocking gates
  actually block merge — advisory CI cannot. Where code scanning is the gate,
  the **Require Code Scanning Results** ruleset rule is the native mechanism.
  [available rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- **MUST** ship a `SECURITY.md` (private vulnerability reporting + scope) and a
  `CODEOWNERS` that includes `/.github/workflows/`.
- **MUST** use a deny-all `.gitignore` with credential re-ignores (org ADR-0003).
  Secret scanning push protection is on by default for public repos.
  [push protection](https://docs.github.com/en/code-security/concepts/secret-security/about-push-protection)
- **MUST** keep **one** dependency-update tool. Renovate is the standard
  (org ADR-0004); Dependabot *version* updates MUST be disabled where Renovate
  runs (Dependabot security alerts may remain as a safety net). Renovate config
  uses `pinDigests: true` and a `minimumReleaseAge`.
- **SHOULD**, where a repo ships a build artifact or image, emit SLSA build
  provenance and an SBOM as signed attestations with `actions/attest@v4` (the
  `attest-build-provenance`/`attest-sbom` actions are now wrappers); verify with
  `gh attestation verify`. Free for public repos.
  [artifact attestations](https://docs.github.com/en/actions/concepts/security/artifact-attestations) ·
  [SLSA v1.2](https://slsa.dev/spec/v1.2/)
- **SHOULD** triage the Security tab: dismiss non-applicable Scorecard findings
  with a documented rationale rather than leaving them open.

## 4. Tests / validation

- **MUST** have *some* executable validation that runs in CI and can fail the
  build — even a contract/lint/render check. A template with no runnable
  validation is not conformant.
- Language-specific: Python → `ruff` + `pytest` (src layout, `pyproject.toml`
  PEP 621, PEP 639 SPDX license). [ruff](https://docs.astral.sh/ruff/) ·
  [pyproject](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/).
  PowerShell → `PSScriptAnalyzer` (PSGallery preset) + Pester v5, module manifest
  with explicit `FunctionsToExport`.
  [PSScriptAnalyzer](https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/using-scriptanalyzer) ·
  [Pester](https://pester.dev/docs/usage/configuration).
  Terraform → `fmt -check` + `validate` + TFLint + Trivy/Checkov (tfsec is
  retired into Trivy). Packer → `fmt -check` + `init` + `validate`. Ansible →
  `ansible-lint` (shared profile) + Molecule. OCI → multi-stage, non-root,
  digest-pinned base, exec-form `HEALTHCHECK`, OpenSCAP/STIG where RHEL-family.
  [Terraform CI](https://developer.hashicorp.com/terraform/tutorials/automation/automate-terraform) ·
  [Packer validate](https://developer.hashicorp.com/packer/docs/commands/validate) ·
  [ansible-lint profiles](https://docs.ansible.com/projects/lint/profiles/) ·
  [Docker best practices](https://docs.docker.com/build/building/best-practices/)

## 5. Documentation & ADRs

- **MUST** organize `docs/` by [Diátaxis](https://diataxis.fr/) (tutorials,
  how-to, reference, explanation) — org ADR-0002.
- **MUST** carry **≥1 Mermaid `.mmd` diagram** in `docs/diagrams/` (the
  `diagram-conventions.md` convention is enforced; an empty `docs/diagrams/` is
  a conformance failure).
- **MUST** populate every Diátaxis quadrant it advertises — no `.gitkeep`-only
  placeholder directories on `main`.
- **MUST** carry at least one **repo-tier ADR** (`docs/decision-records/repo/`)
  documenting a decision unique to the repo; ADRs follow the three tiers
  (org / template / repo) and the MADR format (org ADR-0001).
- **MUST NOT** commit AI bylines, "generated by" footers, or co-author trailers
  anywhere — including commit messages (org ADR-0010).

## 6. Release & versioning

- **MUST** have a release mechanism (release-please, `release-type: simple` for
  non-package repos) wired and **exercised at least once** (a real semver tag),
  so consumers can pin a version rather than a raw SHA.
- **SHOULD** maintain a floating major tag (`v1`) for caller convenience and
  attach a `CHANGELOG`.

## 7. Template contract (template repos)

- **MUST** set `is_template: true` and offer a working "Use this template" path
  whose result has **green CI out of the box**.
- **MUST** pass a stale-placeholder scan (no `TODO`/`FIXME`/`CHANGEME`/`YOUR_*`
  reaching `main`); intentional blocking placeholders (e.g.
  `:REPLACE-WITH-SIGNED-DIGEST`) are documented conventions, not residue.
- **SHOULD** validate the template/consumer interface with a contract checker
  (the framework/runner contract pattern).

## Conformance checklist

| # | Requirement | Type |
| --- | --- | --- |
| 1 | README: what/why + badges + quickstart + architecture/diagram link | MUST |
| 2 | Least-privilege `permissions:` on all workflows | MUST |
| 3 | All `uses:` SHA-pinned with version comment | MUST |
| 4 | `timeout-minutes` + `concurrency` set appropriately | MUST |
| 5 | Ruleset on `main` + `required_status_checks` enforced | MUST |
| 6 | `SECURITY.md` + `CODEOWNERS` (incl. workflows) | MUST |
| 7 | Deny-all `.gitignore`; one update tool (Renovate), Dependabot version-updates off | MUST |
| 8 | Runnable CI validation that can fail the build | MUST |
| 9 | Diátaxis `docs/` + ≥1 Mermaid diagram + ≥1 repo ADR + no empty quadrants | MUST |
| 10 | No AI bylines anywhere (incl. commit messages) | MUST |
| 11 | Release mechanism exercised (≥1 semver tag) | MUST |
| 12 | Provenance + SBOM attestation where an artifact/image ships | SHOULD |
| 13 | Template: `is_template`, green "Use this template" result, no placeholder residue | MUST (templates) |

*Standard v1 — applies to all public `NWarila` repositories. Revisions are
tracked in git history; material changes get a new version heading.*
