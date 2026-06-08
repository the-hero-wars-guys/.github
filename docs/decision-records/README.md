# Architecture Decision Records

This directory defines the portfolio's Architecture Decision Record (ADR) baseline. Each ADR records one architecturally significant decision: the problem being solved, the decision that was made, the alternatives that were considered, and the consequences to expect.

The directory is named `decision-records` because the full name is more readable to contributors, reviewers, and auditors who may not already know the acronym.

This `the-hero-wars-guys/.github` directory holds the **master copies** of every org-baseline ADR. Each adopting child repository mirrors the master ADRs into its own `docs/decision-records/org/` directory (byte-identical content), may mirror type-template ADRs into `docs/decision-records/template/`, and may add its own `docs/decision-records/repo/` ADRs for repository-scoped decisions, per [ADR-0001](0001-use-architecture-decision-records.md). The same MADR 4.0-aligned format applies to all three scopes.

ADRs may begin as `Proposed` while a decision is being discussed. Once accepted, an ADR becomes part of the repository's permanent historical record and remains editable as a living record for the same `Decision-subject`. Same-subject changes are made in place with an append-only Changelog row; different-subject replacements use supersession; no-longer-applicable subjects use obsolescence.

## What is an ADR?

An Architecture Decision Record is a short Markdown document that answers three questions about a single architectural choice:

1. **What is the problem?** What forces drove the decision?
2. **What was decided?** Concretely, what will we do?
3. **Why?** What alternatives were considered, and what trade-offs are we accepting?

A reader who knows nothing about the codebase should be able to open any ADR and understand why a particular design exists. A reviewer evaluating the repository should be able to reconstruct the project's architectural reasoning without a synchronous conversation. An auditor in a regulated environment should be able to trace important design choices to source-controlled artifacts.

The format used here is established by [ADR-0001](0001-use-architecture-decision-records.md). It is MADR 4.0-aligned, uses a visible Markdown metadata table instead of YAML front matter, and adds fields for decision subject, review cadence, reversibility, traceability, Changelog-backed living updates, and conservative compliance mapping.

## Index

| #                                                      | Title                                                          | Status   | Date       | Summary                                                                                        |
| ------------------------------------------------------ | -------------------------------------------------------------- | -------- | ---------- | ---------------------------------------------------------------------------------------------- |
| [0001](0001-use-architecture-decision-records.md)      | Use Architecture Decision Records to Document Design Rationale | Accepted | 2026-04-22 | Adopt ADRs as the documentation format for architecturally significant decisions.              |
| [0002](0002-adopt-diataxis-documentation-framework.md) | Adopt Diátaxis as the Documentation Framework                  | Accepted | 2026-06-02 | Adopt Diátaxis plus sanctioned diagrams and runbooks subtrees for non-ADR documentation. |
| [0003](0003-use-deny-all-gitignore-strategy.md)        | Use a Deny-All `.gitignore` Strategy                           | Accepted | 2026-04-25 | Adopt deny-all `.gitignore` with explicit allowlist as the default tracking strategy for adopting repositories. |
| [0004](0004-use-renovate-for-dependency-updates.md)    | Use Renovate for Dependency Updates with Per-Template Baselines | Accepted | 2026-06-02 | Standardize on Renovate for all `NWarila/*` repos with explicit type-template preset paths that consuming repos extend. |
| [0005](0005-pin-terraform-and-provider-versions-exactly.md) | Pin Terraform and Provider Versions Exactly              | Accepted | 2026-05-05 | All Terraform configurations in `NWarila/*` pin the Terraform CLI and provider versions exactly using the `=` operator; Renovate uses `rangeStrategy: "pin"`. Refines ADR-0004's rangeStrategy guidance. |
| [0006](0006-keep-github-control-planes-namespace-local.md) | Keep GitHub Control Planes Namespace-Local              | Accepted | 2026-06-01 | Repositories use their owning namespace's `.github` control plane for org ADRs, community files, repo hygiene, and reusable workflow callers. |
| [0007](0007-centralize-universal-ci-reusables-within-each-namespace.md) | Centralize Universal CI Reusables Within Each Namespace | Accepted | 2026-06-02 | Universal CI reusable workflows live once in the owning namespace's `.github` control plane and are called by full commit SHA. |
| [0008](0008-enforce-repo-hygiene-by-repo-type.md) | Enforce Repo Hygiene by Repo Type | Accepted | 2026-06-02 | Apply the same repo-hygiene policy through the invocation mechanism that fits each repository type. |
| [0009](0009-classify-baseline-manifest-byte-identity.md) | Classify Baseline Manifest Byte Identity | Accepted | 2026-06-02 | Use byte identity only for files that are truly uniform inherited governance or directly used by the consumer. |
| [0011](0011-adopt-two-organization-portfolio-structure.md) | Adopt a Two-Organization Portfolio Structure | Proposed | 2026-06-03 | Record the deliberate split between `NWarila` (architecture/planning) and `nwarila-platform` (engineering that proves out the standards); parent of ADR-0006/0007. |

## Status Lifecycle

An ADR moves through the following statuses. Every ADR in the Index above shows its current status.

- **Proposed.** The ADR has been drafted and is under discussion. The decision has not yet been made. A `Review-by` date should be set; if the ADR is not Accepted, Superseded, Obsolete, or withdrawn by that date, it should be revisited or closed.
- **Accepted.** The ADR represents an active decision. The code in the repository should reflect it. This is the working state of most ADRs.
- **Superseded by ADR-NNNN.** The decision was valid at the time but has been replaced by a different-subject ADR. Both ADRs remain in the repository. The superseded ADR points forward to the newer one in its `Superseded by` section, and the newer ADR points back in its `Supersedes` section.
- **Obsolete.** The decision subject is no longer applicable and has no replacement. The ADR remains in the repository and its body freezes except for archival link maintenance.
- **Deprecated.** The ADR is still in force but no longer recommended for new work. This status should be rare and should usually lead to an in-place Accepted update, a Superseded status, or an Obsolete status.

An Accepted ADR may receive substantive same-subject updates in place. Every substantive edit to Context, Decision Outcome, Consequences, metadata, or review posture requires a new Changelog row. A `Last reviewed` bump with no body change still requires a Changelog row that says it was re-reviewed and remains valid.

## Editing Decision Tree

Use this decision tree before changing an ADR:

1. If the same `Decision-subject` still exists and the answer, rationale, consequences, review date, or implementation evidence changed, edit the existing ADR in place and append a Changelog row.
2. If a different decision subject replaces this one, create a new ADR, set the old ADR to `Superseded by ADR-NNNN`, and add reciprocal `Supersedes` / `Superseded by` links.
3. If the subject is no longer applicable and has no replacement, set the ADR to `Obsolete`, add a Changelog row, and freeze the body.
4. If only a typo, broken link, or formatting issue changed, make the editorial correction and add a Changelog row when the change could affect interpretation.

Worked example: if the documentation layout still uses Diátaxis but gains a sanctioned `docs/runbooks/` genre, update ADR-0002 in place because the subject is still the documentation framework. If the organization abandons Diátaxis for a different documentation framework, write a new ADR and supersede ADR-0002.

## How to Contribute a New ADR

1. Decide whether the change is architecturally significant. The four tests are in [ADR-0001](0001-use-architecture-decision-records.md) under `Decision Outcome`. When in doubt, err toward writing the ADR; a short record is cheaper than reconstructing the reasoning later.
2. Decide the **scope**:
   - **Org-baseline** — the decision applies across the `NWarila` organization. Author the ADR in this `the-hero-wars-guys/.github` repository at `docs/decision-records/NNNN-short-kebab-title.md`. After it is accepted, mirror it into every adopting child repository's `docs/decision-records/org/` directory in a follow-up sync PR per repo.
   - **Type-template** — the decision applies to every repository derived from a type-template, but not necessarily to every repository in the organization. Author the ADR in that type-template repository's `docs/decision-records/template/` directory and mirror it into each consumer's `docs/decision-records/template/` directory in follow-up sync PRs.
   - **Repository-specific** — the decision affects only one repository. Author the ADR in that repository at `docs/decision-records/repo/NNNN-short-kebab-title.md`. Do not mirror it elsewhere.
3. Copy [ADR-0001](0001-use-architecture-decision-records.md) to the new file. `NNNN` is the next unused four-digit number in the chosen scope's directory. Numbers are allocated monotonically and never reused. The org, template, and repo namespaces are independent (ADR `org/0001`, `template/0001`, and `repo/0001` can coexist in different directories).
4. Strip the template-instruction HTML comment block at the top of the copied file.
5. Replace the metadata values and every section body with content specific to the new decision. Keep the section headings in the order shown. For sections that genuinely do not apply, write "None." or "N/A (reason)." rather than deleting the heading. A missing heading reads as "I forgot"; an explicit "None." reads as "I considered this and there is nothing to record."
6. Add an initial Changelog row that records the accepted decision or proposed draft.
7. Update the appropriate index. For org-baseline ADRs, update the Index in this README. For type-template and repository-specific ADRs, update the corresponding section of the owning repository's `docs/decision-records/README.md`.
8. Open a pull request in the repository where the new ADR lives. The new ADR and the index update belong in the same PR.

## Conventions

- **Directory layout.** Org-baseline ADRs live in `the-hero-wars-guys/.github/docs/decision-records/` (master copies in this repo) and `docs/decision-records/org/` (mirrored copies in every adopting child repo). Type-template ADRs live in their type-template's `docs/decision-records/template/` and are mirrored to consumers at `docs/decision-records/template/`. Repository-specific ADRs live in `docs/decision-records/repo/` in their owning repository only.
- **Directory naming.** Use `decision-records` as the directory name so the purpose is obvious even to readers who do not know the acronym.
- **Filenames.** `NNNN-short-kebab-title.md`, where `NNNN` is a four-digit zero-padded number and the title is a present-tense verb phrase in kebab case. Example: `0004-pin-github-actions-by-commit-sha.md`.
- **Numbering.** Monotonic. Gaps are allowed. Numbers are never reused, even if a proposed ADR is later abandoned.
- **Titles.** Start with a present-tense imperative verb. Prefer `Pin GitHub Actions by Commit SHA` over `GitHub Actions Pinning Policy`. The title is also the H1 of the file, prefixed with `ADR-NNNN:`.
- **Metadata fields.** The table at the top of every ADR records `ID`, `Scope`, `Status`, `Decision-subject`, `Date accepted`, `Date`, `Last reviewed`, `Authors`, `Decision-makers`, `Consulted`, `Informed`, `Reversibility`, and `Review-by`. `Date accepted` is frozen once accepted. `Date` is the last updated date. `Last reviewed` follows the scope cadence: org-baseline and type-template ADRs every 180 days, repository-specific ADRs every 365 days. `Consulted` and `Informed` follow RACI-style conventions: people whose input was actively sought versus people who were kept in the loop. `Reversibility` is an ease-of-change estimate: `Low` means hard to reverse (deeply committed), `Medium` means reversal is possible but involves meaningful migration or rework, and `High` means easy to reverse.
- **Editing.** Accepted ADRs are living records for the same decision subject. Allowed post-acceptance updates include decision, scope, rationale, consequences, Status, `Supersedes` and `Superseded by` links, `Implementing PRs`, review metadata, and editorial corrections, but every substantive update must append a Changelog row. The Changelog is the primary reader-facing audit trail; git history corroborates it.

## Further Reading

Readers unfamiliar with ADRs as a genre may find the following useful. None of these is required; they are provided for context.

- **Michael Nygard, [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions.html) (2011).** The original post that introduced the ADR concept.
- **[MADR](https://adr.github.io/madr/) (Markdown Architectural Decision Records).** The community template that this baseline aligns with.
- **Joel Parker Henderson, [`architecture-decision-record`](https://github.com/joelparkerhenderson/architecture-decision-record).** A widely referenced collection of ADR formats and examples.
- **ThoughtWorks Technology Radar, [Lightweight Architecture Decision Records](https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records) (Adopt, November 2017).** Recommends keeping ADRs in source control instead of a wiki or website.
