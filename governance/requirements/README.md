# Requirements Governance

Requirements are versioned repository artifacts. A substantive requirement change must update the relevant requirement document and project state in the same development cycle.

## Requirement record

Each major requirement should capture:

- ID
- statement
- rationale
- priority
- acceptance criteria
- dependencies
- constraints
- status
- related ADRs
- related missions/tasks

## Rules

- Do not derive permanent requirements only from conversation context.
- Do not implement ambiguous requirements without recording the assumption or resolving the ambiguity.
- Requirement changes that materially affect architecture require an ADR.
- Acceptance criteria should be testable where practical.
