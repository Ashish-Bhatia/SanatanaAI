    older = Checkpoint("cp-old", "mission-test", "task-a", "running", base)
    newer = Checkpoint(
        "cp-new", "mission-test", "task-a", "completed", base + timedelta(seconds=1)
    )
    store.save(newer)
    store.save(older)
    assert store.latest("mission-test", "task-a") == newer


def test_sqlite_rejects_naive_checkpoint_timestamp() -> None:
    store = SQLiteCheckpointStore(sqlite3.connect(":memory:"))
    checkpoint = Checkpoint(
        "cp-1",
        "mission-test",
        "task-a",
        "running",
        datetime.fromisoformat("2026-01-01"),
    )
    with pytest.raises(ValueError, match="timezone-aware"):
        store.save(checkpoint)


def test_sqlite_rejects_corrupt_checkpoint_row() -> None:
    connection = sqlite3.connect(":memory:")
    store = SQLiteCheckpointStore(connection)
    connection.execute(
        "INSERT INTO checkpoints VALUES (?, ?, ?, ?, ?)",
        ("cp-corrupt", "mission-test", "task-a", "running", "not-a-timestamp"),
    )
    with pytest.raises(ValueError, match="created_at is corrupt"):