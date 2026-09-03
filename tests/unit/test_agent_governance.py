import json
from pathlib import Path

import pytest
from sanatana_ai.agents.governance import (
    AgentContract,
    AgentGovernance,
    AgentGovernanceError,
    GovernedAgentExecutor,
    SchemaRegistry,
)
from sanatana_ai.contracts.agent import AgentRequest, AgentResult
from sanatana_ai.contracts.artifact import StructuredArtifact

SCHEMA_ID = "sanatanaai://schemas/test-artifact/v1"


class EchoExecutor:
    def __init__(self, result: AgentResult) -> None:
        self.result = result

    def execute(self, request: AgentRequest) -> AgentResult:
        return self.result


def make_schema_registry(tmp_path: Path) -> SchemaRegistry:
    schema_path = tmp_path / "artifact.schema.json"
    schema_path.write_text(
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$id": SCHEMA_ID,
                "type": "object",
                "required": [
                    "artifact_id",
                    "artifact_type",
                    "schema_id",
                    "version",
                    "owner_agent_id",
                    "payload",
                    "provenance_ids",
                ],
                "properties": {
                    "artifact_id": {"type": "string", "minLength": 1},
                    "artifact_type": {"type": "string", "minLength": 1},
                    "schema_id": {"const": SCHEMA_ID},
                    "version": {"const": "1.0.0"},
                    "owner_agent_id": {"type": "string", "minLength": 1},
                    "payload": {
                        "type": "object",
                        "required": ["value"],
                        "properties": {"value": {"type": "string"}},
                        "additionalProperties": False,
                    },
                    "provenance_ids": {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": False,
            }
        ),
        encoding="utf-8",
    )
    return SchemaRegistry({SCHEMA_ID: schema_path})


def make_contract(*, provenance_required: bool = True) -> AgentContract:
    return AgentContract(
        id="research.source",
        version="1.2.0",
        responsibility="discover sources",
        inputs=frozenset({"source_request"}),
        outputs=frozenset({"source_artifact"}),
        permissions=frozenset({"source.read", "source.write"}),
        validation=frozenset({"artifact_schema"}),
        failure_handling=frozenset({"retry_transient"}),
        provenance_required=provenance_required,
    )


def make_artifact(
    *,
    artifact_type: str = "source_artifact",
    owner_agent_id: str = "research.source",
    value: str = "ok",
    provenance_ids: tuple[str, ...] = ("prov-1",),
) -> StructuredArtifact:
    return StructuredArtifact(
        artifact_id="artifact-1",
        artifact_type=artifact_type,
        schema_id=SCHEMA_ID,
        version="1.0.0",
        owner_agent_id=owner_agent_id,
        payload={"value": value},
        provenance_ids=provenance_ids,
    )


def make_governance(tmp_path: Path) -> AgentGovernance:
    return AgentGovernance(
        {"research.source": make_contract()},
        make_schema_registry(tmp_path),
    )


def test_governance_loads_repository_registry() -> None:
    root = Path(__file__).parents[2]
    schemas = SchemaRegistry.from_registry(
        root / "agents/registry/artifact-schemas.json", root
    )
    governance = AgentGovernance.from_registry(
        root / "agents/registry/foundation.agents.json",
        root / "agents/schemas/agent-contract.schema.json",
        schemas,
    )

    assert governance.contract_for("orchestration.mission").version == "1.0.0"


def test_governance_rejects_unregistered_agent(tmp_path: Path) -> None:
    governance = make_governance(tmp_path)
    request = AgentRequest("mission-test", "task-a", "unknown.agent")

    with pytest.raises(AgentGovernanceError, match="unregistered agent"):
        governance.authorize_request(request)


def test_governance_rejects_undeclared_permission(tmp_path: Path) -> None:
    governance = make_governance(tmp_path)
    request = AgentRequest(
        "mission-test",
        "task-a",
        "research.source",
        requested_permissions=("network.admin",),
    )

    with pytest.raises(AgentGovernanceError, match="undeclared permissions"):
        governance.authorize_request(request)


def test_governance_accepts_declared_permission_and_valid_input(tmp_path: Path) -> None:
    governance = make_governance(tmp_path)
    request = AgentRequest(
        "mission-test",
        "task-a",
        "research.source",
        requested_permissions=("source.read",),
        input_artifacts=(make_artifact(artifact_type="source_request"),),
    )

    assert governance.authorize_request(request).id == "research.source"


def test_governance_rejects_undeclared_input_artifact_type(tmp_path: Path) -> None:
    governance = make_governance(tmp_path)
    artifact = make_artifact(artifact_type="unexpected")

    with pytest.raises(
        AgentGovernanceError, match="does not declare input artifact type"
    ):
        governance.authorize_request(
            AgentRequest(
                "mission-test", "task-a", "research.source", input_artifacts=(artifact,)
            )
        )


def test_governance_rejects_unregistered_artifact_schema(tmp_path: Path) -> None:
    governance = make_governance(tmp_path)
    artifact = StructuredArtifact(
        "artifact-1",
        "source_request",
        "sanatanaai://schemas/not-registered/v1",
        "1.0.0",
        "research.source",
        {"value": "ok"},
        ("prov-1",),
    )

    with pytest.raises(AgentGovernanceError, match="unregistered artifact schema"):
        governance.authorize_request(
            AgentRequest(
                "mission-test", "task-a", "research.source", input_artifacts=(artifact,)
            )
        )


def test_governed_executor_rejects_invalid_output_artifact(tmp_path: Path) -> None:
    governance = make_governance(tmp_path)
    invalid = make_artifact(value="not-invalid")
    invalid = StructuredArtifact(
        invalid.artifact_id,
        invalid.artifact_type,
        invalid.schema_id,
        invalid.version,
        invalid.owner_agent_id,
        {"wrong": "payload"},
        invalid.provenance_ids,
    )
    result = AgentResult(
        "mission-test",
        "task-a",
        "research.source",
        "completed",
        output_artifacts=(invalid,),
    )

    with pytest.raises(AgentGovernanceError, match="failed schema validation"):
        GovernedAgentExecutor(EchoExecutor(result), governance).execute(
            AgentRequest("mission-test", "task-a", "research.source")
        )


def test_governed_executor_rejects_undeclared_output_artifact_type(
    tmp_path: Path,
) -> None:
    governance = make_governance(tmp_path)
    artifact = make_artifact(artifact_type="unexpected")
    result = AgentResult(
        "mission-test",
        "task-a",
        "research.source",
        "completed",
        output_artifacts=(artifact,),
    )

    with pytest.raises(
        AgentGovernanceError, match="does not declare output artifact type"
    ):
        GovernedAgentExecutor(EchoExecutor(result), governance).execute(
            AgentRequest("mission-test", "task-a", "research.source")
        )


def test_governed_executor_rejects_output_owned_by_other_agent(tmp_path: Path) -> None:
    governance = make_governance(tmp_path)
    result = AgentResult(
        "mission-test",
        "task-a",
        "research.source",
        "completed",
        output_artifacts=(make_artifact(owner_agent_id="other.agent"),),
    )

    with pytest.raises(AgentGovernanceError, match="does not own output artifact"):
        GovernedAgentExecutor(EchoExecutor(result), governance).execute(
            AgentRequest("mission-test", "task-a", "research.source")
        )


def test_governed_executor_requires_provenance_when_contract_requires_it(
    tmp_path: Path,
) -> None:
    governance = make_governance(tmp_path)
    artifact = make_artifact(provenance_ids=())
    result = AgentResult(
        "mission-test",
        "task-a",
        "research.source",
        "completed",
        output_artifacts=(artifact,),
    )

    with pytest.raises(AgentGovernanceError, match="requires provenance"):
        GovernedAgentExecutor(EchoExecutor(result), governance).execute(
            AgentRequest("mission-test", "task-a", "research.source")
        )


def test_governed_executor_rejects_duplicate_output_artifact_ids(
    tmp_path: Path,
) -> None:
    governance = make_governance(tmp_path)
    artifact = make_artifact()
    result = AgentResult(
        "mission-test",
        "task-a",
        "research.source",
        "completed",
        output_artifacts=(artifact, artifact),
    )

    with pytest.raises(AgentGovernanceError, match="duplicate output artifact id"):
        GovernedAgentExecutor(EchoExecutor(result), governance).execute(
            AgentRequest("mission-test", "task-a", "research.source")
        )


def test_governed_executor_accepts_valid_result(tmp_path: Path) -> None:
    governance = make_governance(tmp_path)
    result = AgentResult(
        "mission-test",
        "task-a",
        "research.source",
        "completed",
        output_artifacts=(make_artifact(),),
    )

    assert (
        GovernedAgentExecutor(EchoExecutor(result), governance).execute(
            AgentRequest("mission-test", "task-a", "research.source")
        )
        == result
    )
