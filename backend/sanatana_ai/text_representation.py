from __future__ import annotations

from dataclasses import dataclass

REPRESENTATION_TYPES = frozenset({"original", "transliteration", "translation"})
SCHEMA_VERSION = "1.0"


@dataclass(frozen=True)
class TextRepresentation:
    id: str
    source_id: str
    representation_type: str
    language: str
    text: str
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError("unsupported text representation schema version")
        if not all((self.id, self.source_id, self.language, self.text)):
            raise ValueError("text representation identity, source, language, and text are required")
        if self.representation_type not in REPRESENTATION_TYPES:
            raise ValueError("invalid text representation type")


@dataclass(frozen=True)
class PassageRecord:
    id: str
    representation_id: str
    source_id: str
    locator: str
    text: str
    language: str
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError("unsupported passage schema version")
        if not all((self.id, self.representation_id, self.source_id, self.locator, self.text, self.language)):
            raise ValueError("passage identity, representation, source, locator, language, and text are required")


class TextRepresentationRegistry:
    """Storage-neutral registry enforcing representation and passage identity boundaries."""

    def __init__(self) -> None:
        self._representations: dict[str, TextRepresentation] = {}
        self._passages: dict[str, PassageRecord] = {}

    def register_representation(self, representation: TextRepresentation) -> TextRepresentation:
        existing = self._representations.get(representation.id)
        if existing is not None and existing != representation:
            raise ValueError("representation ID already exists with different content")
        self._representations[representation.id] = representation
        return representation

    def register_passage(self, passage: PassageRecord) -> PassageRecord:
        representation = self._representations.get(passage.representation_id)
        if representation is None:
            raise ValueError("passage references an unknown representation")
        if representation.source_id != passage.source_id:
            raise ValueError("passage source does not match representation source")
        if representation.language != passage.language:
            raise ValueError("passage language does not match representation language")
        existing = self._passages.get(passage.id)
        if existing is not None and existing != passage:
            raise ValueError("passage ID already exists with different content")
        self._passages[passage.id] = passage
        return passage

    def get_representation(self, representation_id: str) -> TextRepresentation:
        try:
            return self._representations[representation_id]
        except KeyError as exc:
            raise KeyError(f"unknown representation: {representation_id}") from exc

    def get_passage(self, passage_id: str) -> PassageRecord:
        try:
            return self._passages[passage_id]
        except KeyError as exc:
            raise KeyError(f"unknown passage: {passage_id}") from exc

    def passages_for_representation(self, representation_id: str) -> tuple[PassageRecord, ...]:
        self.get_representation(representation_id)
        return tuple(item for item in self._passages.values() if item.representation_id == representation_id)
