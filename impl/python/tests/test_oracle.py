"""Oracle tests comparing HashMap against built-in dict."""

import random
from dsa_lab import HashMap


class TestOracleComparison:
    """Compare HashMap against Python's built-in dict."""

    def test_insert_get(self) -> None:
        our_map = HashMap()
        std_map: dict[str, str] = {}

        for i in range(1000):
            key = f"key_{i}"
            value = f"value_{i}"
            our_map.insert(key, value)
            std_map[key] = value

        assert len(our_map) == len(std_map)

        for i in range(1000):
            key = f"key_{i}"
            assert our_map.get(key) == std_map.get(key)

        # Non-existent key
        assert our_map.get("nonexistent") == std_map.get("nonexistent")

    def test_overwrite(self) -> None:
        our_map = HashMap()
        std_map: dict[str, str] = {}

        # Insert initial values
        for i in range(100):
            key = f"key_{i}"
            value = f"value_{i}"
            our_map.insert(key, value)
            std_map[key] = value

        # Overwrite
        for i in range(100):
            key = f"key_{i}"
            new_value = f"new_value_{i}"
            our_map.insert(key, new_value)
            std_map[key] = new_value

        assert len(our_map) == len(std_map)
        for i in range(100):
            key = f"key_{i}"
            assert our_map.get(key) == std_map[key]

    def test_remove(self) -> None:
        our_map = HashMap()
        std_map: dict[str, str] = {}

        # Insert
        for i in range(100):
            key = f"key_{i}"
            value = f"value_{i}"
            our_map.insert(key, value)
            std_map[key] = value

        # Remove even keys
        for i in range(0, 100, 2):
            key = f"key_{i}"
            our_map.remove(key)
            del std_map[key]

        assert len(our_map) == len(std_map)

        for i in range(100):
            key = f"key_{i}"
            assert our_map.get(key) == std_map.get(key)
            assert our_map.contains(key) == (key in std_map)

    def test_mixed_operations(self) -> None:
        rng = random.Random(42)
        our_map = HashMap()
        std_map: dict[str, str] = {}

        for _ in range(10000):
            op = rng.randint(0, 2)
            key = f"key_{rng.randint(0, 99)}"
            value = f"value_{rng.randint(0, 999)}"

            if op == 0:  # Insert
                our_map.insert(key, value)
                std_map[key] = value
            elif op == 1:  # Get
                assert our_map.get(key) == std_map.get(key)
            else:  # Remove
                our_result = our_map.remove(key)
                std_result = std_map.pop(key, None)
                assert our_result == std_result

        assert len(our_map) == len(std_map)
