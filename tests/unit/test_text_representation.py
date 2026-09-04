from __future__ import annotations

from dataclasses import replace

import pytest

from sanatana_ai.text_representation import (
    PassageRecord,
    TextRepresentation,
    TextRepresentationRegistry,
)


def make_representation() -> TextRepresentation:
    return TextRepresentation(
        id="repr-001",
        source_id="source-001",
        representation_type="original",
        language="sa",
        text="धर्मस्य तत्त्वं निहितं गुहायाम्",
    )


def make_passage() -> PassageRecord:
    return PassageRecord(
        id="passage-001",
        representation_id="repr-001",
        source_id="source-001",
        locator="adhyaya:1:verse:1",
        text="धर्मस्य तत्त्वं निहितं गुहायाम्",
        language="sa",
    )


def test_representation_registry_is_idempotent() -> None:
    registry = TextRepresentationRegistry()
    representation = make_representation()
    assert registry.register_representation(representation) == representation
    assert registry.register_representation(representation) == representation


def test_conflicting_representation_id_fails_closed() -> None:
    registry = TextRepresentationRegistry()
    representation = make_representation()
    registry.register_representation(representation)
    with pytest.raises(ValueError, match="representation ID"):
        registry.register_representation(replace(representation, language="hi"))


def test_passage_requires_known_representation() -> None:
    registry = TextRepresentationRegistry()
    with pytest.raises(ValueError, match="unknown representation"):
        registry.register_passage(make_passage())


def test_passage_must_match_representation_source_and_language() -> None:
    registry = TextRepresentationRegistry()
    registry.register_representation(make_representation())
    with pytest.raises(ValueError, match="source"):
        registry.register_passage(replace(make_passage(), source_id="source-002"))
    with pytest.raises(ValueError, match="language"):
        registry.register_passage(replace(make_passage(), language="hi"))


def test_passage_identity_is_idempotent_and_conflicts_fail_closed() -> None:
    registry = TextRepresentationRegistry()
    registry.register_representation(make_representation())
    passage = make_passage()
    assert registry.register_passage(passage) == passage
    assert registry.register_passage(passage) == passage
    with pytest.raises(ValueError, match="passage ID"):
        registry.register_passage(replace(passage, text="different"))
