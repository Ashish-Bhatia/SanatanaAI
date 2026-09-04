# REQ-006 Provenance Evidence Pipeline

Status: In progress
Issue: #6

## Requirement

SanatanaAI must represent substantive knowledge as a source-to-claim evidence chain. Every claim must retain explicit provenance to addressable source evidence and processing history.

## Required artifacts

- Source with stable identity and metadata.
- Passage with stable source linkage, locator, text, and language.
- Atomic claim with explicit evidence class and provenance identifier.
- Evidence reference linking a claim to a passage and provenance record.
- Processing record capturing operation, agent, inputs, outputs, and timestamp.
- Provenance record capturing source linkage, evidence class, processing history, and schema version.

## Invariants

- Every artifact has a stable non-empty identifier.
- Sources carry metadata.
- Passages are addressable and tied to a source.
- Claims identify their evidence class and provenance.
- Evidence references identify both claim and passage.
- Processing history is explicit and non-empty.
- Schema versions are explicit and validated.
- Invalid or incomplete provenance fails closed.
- Original-language, transliteration, and translation representations remain distinguishable.
- AI synthesis is never classified as primary textual evidence.

## Acceptance

The implementation is complete only after schemas, backend validation, representative fixtures, automated tests, CI validation, architecture documentation, review, and merge all pass.
