# Repository Governance Design

> **Scope**: Default repository settings, security posture, and operational
> conventions applied across all repositories owned by NWarila.
>
> **Audience**: Maintainers and contributors who need to understand *why*
> every default was chosen, not just *what* it is.

## Design Philosophy

Every default in this governance model follows four principles:

1. **Secure by default.** New repositories inherit the strictest reasonable
   posture. Relaxations are explicit, documented, and opt-in.
2. **Least privilege.** Access, visibility, and permissions start at the
   minimum required. Escalation requires justification.
3. **Auditability.** Every tracked file is explicitly allowed in a deny-all
   `.gitignore`. Every `.gitattributes` rule has a comment explaining why it
   exists. Every governance decision is documented here.
4. **Inheritance over duplication.** Shared policy lives in this `.github`
   repo once. Repositories inherit it automatically. Local overrides are
   permitted but discouraged unless the repo has a genuine reason to diverge.

These principles are informed by:

- [OWASP Top 10](https://owasp.org/Top10/)
- [NIST SP 800-53](https://csf.tools/reference/nist-sp-800-53/r5/) (Security and Privacy Controls)
- [SLSA Framework](https://slsa.dev/) (Supply-chain Levels for Software Artifacts)
- [OpenSSF Scorecard](https://securityscorecards.dev/) (Automated security health metrics)

## Visibility

Repositories default to private. Public visibility is a deliberate publication
decision, not an accident. Each repository's visibility is declared explicitly
and reviewed before any change.

## Branch Protection

The default branch (`main`) is protected across all repositories:

- Direct pushes are blocked. All changes arrive through pull requests.
- Force pushes are prohibited to preserve commit integrity and audit trails.
- Branch deletion is disabled for the default branch.

These rules enforce linear, reviewable history and prevent accidental
destruction of the canonical branch.

## Merge Strategy

Squash merge is the default and preferred strategy. It produces one commit per
pull request on the default branch, which keeps `git log --oneline` readable
and makes `git bisect` effective.

Merge commits and rebase merges are disabled by default to prevent noisy
history from multi-commit branches.

## Security Features

All repositories enable the core set of GitHub security features regardless of
visibility:

- **Secret scanning**: detects known credential patterns in repository
  contents.
- **Push protection**: blocks pushes containing detected secrets before they
  enter the repository. Prevention is orders of magnitude better than
  detection after the fact.
- **Dependency alerts and security updates**: surfaces known vulnerabilities
  in declared dependencies and offers automated remediation.

AI-powered / non-provider secret detection — which catches non-standard
credential formats that provider-pattern scanning misses — is the intended
posture and is enabled opt-in where supported, rather than uniformly enabled
across the fleet today.

These features are free for all repository visibilities and have no meaningful
downside.

## Community Health Files

Shared community health files are maintained in this repository and inherited
by all repositories that do not define their own:

| File | Governance rationale |
|------|---------------------|
| `CODE_OF_CONDUCT.md` | Establishes consistent community standards (Contributor Covenant 3.0) |
| `CONTRIBUTING.md` | Routes contributions through structured templates and a consistent workflow |
| `SECURITY.md` | Directs vulnerability reports to private channels with defined response timelines |
| `SUPPORT.md` | Routes questions to the Issues tab and prevents issue tracker noise |

## Issue and Pull Request Templates

Issue intake uses structured YAML forms (bug report, feature request,
documentation) with required fields. Blank issues are disabled to ensure every
report includes actionable context.

The pull request template requires a summary, related issue link, testing
evidence, and a security-sensitive change checkbox.

## CI Conventions

Every repository runs at minimum:

- **Markdown linting** via `markdownlint-cli2` with a shared configuration.
- **GitHub Actions linting** via `actionlint` where workflows exist.

Additional CI jobs (language-specific linting, testing, security scanning) are
added per repository based on its content.

## Dependency Management

Renovate is the org standard for dependency updates per
[ADR-0004](docs/decision-records/0004-use-renovate-for-dependency-updates.md);
Dependabot **version** updates are not used (Renovate opens all version-bump
PRs), while Dependabot **security** alerts and security updates remain enabled
as a separate safety net. Each type-template owns a self-contained
`.github/renovate.json5` baseline that its consumers extend. GitHub Actions
SHA pins, and any other supported ecosystems, are updated on a weekly cadence
to prevent drift and reduce exposure to supply-chain vulnerabilities. This org
`.github` repository carries its own `.github/renovate.json5` (per ADR-0004) that
governs only its own `github-actions` pins; it is not an org-level baseline and
no consumer extends it.

## File Hygiene Conventions

All repositories follow these conventions:

- **Deny-all `.gitignore`**: every tracked file is explicitly allowed. Nothing
  is tracked by accident.
- **Self-documenting files**: every rule in `.gitignore` and `.gitattributes`
  has a comment explaining why it exists.
- **LF normalization**: all text files are normalized to LF via
  `.gitattributes` for stable diffs across platforms.
- **No editor config in repositories that contain no source code.** Editor
  settings belong only in repositories where code is authored.
