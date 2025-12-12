"""Unit tests for HashMap implementation."""

import pytest
from dsa_lab import HashMap


class TestHashMapBasic:
    """Basic HashMap tests."""

    def test_new_map_is_empty(self) -> None:
        m = HashMap()
        assert len(m) == 0
        assert not m

    def test_insert_and_get(self) -> None:
        m = HashMap()
        result = m.insert("key1", "value1")
        assert result is None
        assert m.get("key1") == "value1"
        assert len(m) == 1

    def test_insert_overwrite(self) -> None:
        m = HashMap()
        m.insert("key", "value1")
        old = m.insert("key", "value2")
        assert old == "value1"
        assert m.get("key") == "value2"
        assert len(m) == 1

    def test_remove(self) -> None:
        m = HashMap()
        m.insert("key", "value")
        removed = m.remove("key")
        assert removed == "value"
        assert m.get("key") is None
        assert len(m) == 0

    def test_remove_non_existent(self) -> None:
        m = HashMap()
        removed = m.remove("nonexistent")
        assert removed is None

    def test_contains(self) -> None:
        m = HashMap()
        m.insert("key", "value")
        assert m.contains("key")
        assert not m.contains("other")
        assert "key" in m
        assert "other" not in m

    def test_clear(self) -> None:
        m = HashMap()
        m.insert("key1", "value1")
        m.insert("key2", "value2")
        m.clear()
        assert len(m) == 0
        assert m.get("key1") is None


class TestHashMapResize:
    """Tests for HashMap resizing."""

    def test_resize(self) -> None:
        m = HashMap(capacity=4)
        for i in range(100):
            m.insert(f"key{i}", f"value{i}")

        assert len(m) == 100
        for i in range(100):
            assert m.get(f"key{i}") == f"value{i}"

    def test_tombstone_reuse(self) -> None:
        m = HashMap()
        m.insert("key1", "value1")
        m.insert("key2", "value2")
        m.remove("key1")
        m.insert("key3", "value3")

        assert len(m) == 2
        assert m.contains("key2")
        assert m.contains("key3")
        assert not m.contains("key1")


class TestHashMapPythonic:
    """Tests for Pythonic interface."""

    def test_bracket_get(self) -> None:
        m = HashMap()
        m.insert("key", "value")
        assert m["key"] == "value"

    def test_bracket_get_missing(self) -> None:
        m = HashMap()
        with pytest.raises(KeyError):
            _ = m["nonexistent"]

    def test_bracket_set(self) -> None:
        m = HashMap()
        m["key"] = "value"
        assert m.get("key") == "value"

    def test_del(self) -> None:
        m = HashMap()
        m.insert("key", "value")
        del m["key"]
        assert m.get("key") is None

    def test_del_missing(self) -> None:
        m = HashMap()
        with pytest.raises(KeyError):
            del m["nonexistent"]

    def test_iter(self) -> None:
        m = HashMap()
        m.insert("a", "1")
        m.insert("b", "2")
        m.insert("c", "3")

        keys = list(m)
        assert len(keys) == 3
        assert set(keys) == {"a", "b", "c"}

    def test_keys(self) -> None:
        m = HashMap()
        m.insert("a", "1")
        m.insert("b", "2")
        assert set(m.keys()) == {"a", "b"}

    def test_values(self) -> None:
        m = HashMap()
        m.insert("a", "1")
        m.insert("b", "2")
        assert set(m.values()) == {"1", "2"}

    def test_items(self) -> None:
        m = HashMap()
        m.insert("a", "1")
        m.insert("b", "2")
        assert set(m.items()) == {("a", "1"), ("b", "2")}
