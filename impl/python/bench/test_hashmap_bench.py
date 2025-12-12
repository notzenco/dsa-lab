"""Benchmarks for HashMap implementation."""

import json
from pathlib import Path
from typing import Optional
import pytest

from dsa_lab import HashMap


def load_workload(name: str) -> Optional[dict]:
    """Load a workload file."""
    paths = [
        Path(__file__).parent.parent.parent.parent
        / "workloads"
        / "map"
        / f"{name}.json",
        Path(__file__).parent.parent.parent.parent.parent
        / "workloads"
        / "map"
        / f"{name}.json",
    ]

    for path in paths:
        if path.exists():
            with open(path) as f:
                return json.load(f)
    return None


class TestInsertBenchmarks:
    """Insert operation benchmarks."""

    @pytest.mark.parametrize("size", [100, 1000, 10000])
    def test_insert(self, benchmark, size: int) -> None:
        keys = [f"key_{i}" for i in range(size)]
        values = [f"value_{i}" for i in range(size)]

        def run():
            m = HashMap()
            for key, value in zip(keys, values):
                m.insert(key, value)
            return m

        result = benchmark(run)
        assert len(result) == size


class TestGetBenchmarks:
    """Get operation benchmarks."""

    @pytest.mark.parametrize("size", [100, 1000, 10000])
    def test_get(self, benchmark, size: int) -> None:
        keys = [f"key_{i}" for i in range(size)]
        m = HashMap()
        for i, key in enumerate(keys):
            m.insert(key, f"value_{i}")

        def run():
            for key in keys:
                m.get(key)

        benchmark(run)


class TestWorkloadBenchmarks:
    """Workload-based benchmarks."""

    def test_mixed_uniform_medium(self, benchmark) -> None:
        workload = load_workload("mixed_uniform_medium")
        if workload is None:
            pytest.skip("Workload not found")

        operations = workload["operations"]

        def run():
            m = HashMap()
            for op in operations:
                if op["op"] == "insert":
                    m.insert(op["key"], op.get("value", ""))
                elif op["op"] == "get":
                    m.get(op["key"])
                elif op["op"] == "delete":
                    m.remove(op["key"])
            return m

        benchmark(run)

    def test_insert_heavy_uniform_medium(self, benchmark) -> None:
        workload = load_workload("insert_heavy_uniform_medium")
        if workload is None:
            pytest.skip("Workload not found")

        operations = workload["operations"]

        def run():
            m = HashMap()
            for op in operations:
                if op["op"] == "insert":
                    m.insert(op["key"], op.get("value", ""))
            return m

        benchmark(run)

    def test_read_heavy_uniform_medium(self, benchmark) -> None:
        workload = load_workload("read_heavy_uniform_medium")
        if workload is None:
            pytest.skip("Workload not found")

        operations = workload["operations"]

        def run():
            m = HashMap()
            for op in operations:
                if op["op"] == "insert":
                    m.insert(op["key"], op.get("value", ""))
                elif op["op"] == "get":
                    m.get(op["key"])
            return m

        benchmark(run)
