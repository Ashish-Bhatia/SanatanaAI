from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from sanatana_ai.agents.registry import AgentRegistryError, load_registry
from sanatana_ai.contracts.agent import AgentRequest, AgentResult
from sanatana_ai.contracts.artifact import StructuredArtifact

_SEMVER = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")


class AgentGovernanceError(ValueError):
    """Raised when runtime agent governance rules are violated."""


@dataclass(frozen=True)
class AgentContract:
    id: str
    version: str
    responsibility: str
    inputs: frozenset[str]
    outputs: frozenset[str]
    permissions: frozenset[str]
    validation: frozenset[str]
    failure_handling: frozenset[str]
    provenance_required: bool

    @classmethod
    def from_entry(cls, entry: dict[str, Any]) -> "AgentContract":
        version = entry["version"]
        if not _SEMVER.fullmatch(version):
            raise AgentGovernanceError(f"invalid agent contract version: {version}")
        return cls(
            id=entry["id"],
            version=version,
            responsibility=entry["responsibility"],
            inputs=frozenset(entry["inputs"]),
            outputs=frozenset(entry["outputs"]),
            permissions=frozenset(entry["permissions"]),
            validation=frozenset(entry["validation"]),
            failure_handling=frozenset(entry["failure_handling"]),
            provenance_required=entry["provenance_required"],
        )


class SchemaRegistry:
    """Registry of JSON Schemas addressable by stable schema IDs."""

    def __init__(self, entries: dict[str, Path]) -> None:
        self._schemas: dict[str, dict[str, Any]] = {}
        for schema_id, path in entries.items():
            schema = json.loads(path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            if schema.get("$id") != schema_id:
                raise AgentGovernanceError(
                    f"schema registry id does not match schema $id: {schema_id}"
                )
            self._schemas[schema_id] = schema

    def validator(self, schema_id: str) -> Draft202012Validator:
        try:
            schema = self._schemas[schema_id]
        except KeyError as exc:
            raise AgentGovernanceError(f"unregistered artifact schema: {schema_id}") from exc
        return Draft202012Validator(schema)


class AgentGovernance:
    """Deterministic runtime policy for registered agents and structured artifacts."""

    def __init__(self, contracts: dict[str, AgentContract], schemas: SchemaRegistry) -> None:
        self._contracts = contracts
        self._schemas = schemas

    @classmethod
    def from_registry(
        cls,
        registry_path: Path,
        contract_schema_path: Path,
        schemas: SchemaRegistry,
    ) -> "AgentGovernance":
        try:
            entries = load_registry(registry_path, contract_schema_path)
        except AgentRegistryError as exc:
            raise AgentGovernanceError(str(exc)) from exc
        contracts = {entry["id"]: AgentContract.from_entry(entry) for entry in entries}
        return cls(contracts, schemas)

    def contract_for(self, agent_id: str) -> AgentContract:
        try:
            return self._contracts[agent_id]
        except KeyError as exc:
            raise AgentGovernanceError(f"unregistered agent: {agent_id}") from exc

    def authorize_request(self, request: AgentRequest) -> AgentContract:
        contract = self.contract_for(request.agent_id)
        undeclared = set(request.requested_permissions) - contract.permissions
        if undeclared:
            raise AgentGovernanceError(
                f"agent {request.agent_id} requested undeclared permissions: "
                f"{sorted(undeclared)}"
            )
        for artifact in request.input_artifacts:
            self._validate_artifact(artifact)
        return contract

    def validate_result(self, contract: AgentContract, result: AgentResult) -> None:
        if result.agent_id != contract.id:
            raise AgentGovernanceError("agent result identity does not match contract")
        seen_ids: set[str] = set()
        for artifact in result.output_artifacts:
            self._validate_artifact(artifact)
            if artifact.artifact_id in seen_ids:
                raise AgentGovernanceError(
                    f"duplicate output artifact id: {artifact.artifact_id}"
                )
            seen_ids.add(artifact.artifact_id)
            if artifact.owner_agent_id != contract.id:
                raise AgentGovernanceError(
                    f"agent {contract.id} does not own output artifact {artifact.artifact_id}"
                )
            if contract.provenance_required and not artifact.provenance_ids:
                raise AgentGovernanceError(
                    f"agent {contract.id} requires provenance for output artifacts"
                )

    def _validate_artifact(self, artifact: StructuredArtifact) -> None:
        if not artifact.artifact_id.strip():
            raise AgentGovernanceError("artifact_id must not be empty")
        if not _SEMVER.fullmatch(artifact.version):
            raise AgentGovernanceError(f"invalid artifact version: {artifact.version}")
        validator = self._schemas.validator(artifact.schema_id)
        document = {
            "artifact_id": artifact.artifact_id,
            "schema_id": artifact.schema_id,
            "version": artifact.version,
            "owner_agent_id": artifact.owner_agent_id,
            "payload": artifact.payload,
            "provenance_ids": list(artifact.provenance_ids),
        }
        errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
        if errors:
            details = "; ".join(error.message for error in errors)
            raise AgentGovernanceError(
                f"artifact {artifact.artifact_id} failed schema validation: {details}"
            )
