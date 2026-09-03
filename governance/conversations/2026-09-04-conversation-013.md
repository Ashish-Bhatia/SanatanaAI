# Conversation 013

Date: 2026-09-04

## Objective
Strengthen the Foundation CI quality gate under issue #4 without introducing paid tooling or bypassing existing validation.

## Requirements
- Add formatting and lint enforcement.
- Add static type checking.
- Add dependency vulnerability auditing.
- Add backend build validation.
- Add documentation structure validation.
- Preserve JSON, agent-contract, artifact-schema, backend-test, and secret checks.
- Use open-source tooling available in GitHub Actions.

## Decisions
- Use Ruff for formatting and linting.
- Use mypy for backend static type checking.
- Use pip-audit for Python dependency vulnerability checks.
- Use Python build for package build validation.
- Validate ADR structural sections in CI.
- Keep all gates in the existing Foundation workflow rather than adding unnecessary workflow sprawl.

## Actions
- Created `feature/ci-quality-gates` from the validated main baseline.
- Added Ruff and mypy configuration to `backend/pyproject.toml`.
- Extended CI with formatting, lint, type, dependency-audit, build, and ADR-structure gates.
- Preserved the existing JSON, registry, test, and secret checks.

## Validation
- Fresh PR CI is required. The first run will expose any formatting, typing, dependency, or build defects that must be corrected before merge.

## Unresolved
- Provenance-specific validation remains part of issue #6.
- Additional integration/regression coverage will grow with the platform.
- CI workflow optimization and caching remain future improvements after correctness is established.
