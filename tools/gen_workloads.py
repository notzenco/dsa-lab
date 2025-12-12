#!/usr/bin/env python3
"""
Workload Generator for dsa-lab

Generates deterministic workload files for benchmarking hash map implementations.
All workloads use fixed seeds for reproducibility.
"""

import json
import random
import math
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Fixed seeds for reproducibility
SEEDS = {
    "insert_heavy_uniform": 42,
    "insert_heavy_zipf": 43,
    "read_heavy_uniform": 44,
    "read_heavy_zipf": 45,
    "mixed_uniform": 46,
    "mixed_zipf": 47,
    "delete_heavy_uniform": 48,
    "delete_heavy_zipf": 49,
}

# Workload sizes
SIZES = {
    "small": 1_000,
    "medium": 10_000,
    "large": 100_000,
}

# Operation types
OP_INSERT = "insert"
OP_GET = "get"
OP_DELETE = "delete"


def zipf_distribution(n: int, s: float = 1.0, seed: int = 0) -> List[int]:
    """
    Generate n samples from a Zipf distribution.

    Args:
        n: Number of samples
        s: Zipf exponent (higher = more skewed)
        seed: Random seed

    Returns:
        List of integers following Zipf distribution
    """
    rng = random.Random(seed)

    # Precompute harmonic numbers for normalization
    max_k = 10000  # Maximum key value
    harmonics = [0.0]
    for k in range(1, max_k + 1):
        harmonics.append(harmonics[-1] + 1.0 / (k ** s))

    total = harmonics[-1]
    samples = []

    for _ in range(n):
        u = rng.random() * total
        # Binary search for the key
        lo, hi = 1, max_k
        while lo < hi:
            mid = (lo + hi) // 2
            if harmonics[mid] < u:
                lo = mid + 1
            else:
                hi = mid
        samples.append(lo)

    return samples


def generate_keys(n: int, distribution: str, seed: int) -> List[str]:
    """Generate n keys with the specified distribution."""
    rng = random.Random(seed)

    if distribution == "uniform":
        # Uniform random keys
        return [f"key_{rng.randint(0, n * 10)}" for _ in range(n)]
    elif distribution == "zipf":
        # Zipf-distributed keys (some keys appear much more frequently)
        indices = zipf_distribution(n, s=1.0, seed=seed)
        return [f"key_{i}" for i in indices]
    else:
        raise ValueError(f"Unknown distribution: {distribution}")


def generate_values(n: int, seed: int) -> List[str]:
    """Generate n random values."""
    rng = random.Random(seed)
    return [f"value_{rng.randint(0, 1_000_000)}" for _ in range(n)]


def generate_workload(
    name: str,
    size: int,
    distribution: str,
    op_weights: Dict[str, float],
    seed: int,
) -> Dict[str, Any]:
    """
    Generate a workload specification.

    Args:
        name: Workload name
        size: Number of operations
        distribution: Key distribution ("uniform" or "zipf")
        op_weights: Dict of operation type to weight (must sum to 1.0)
        seed: Random seed

    Returns:
        Workload specification dict
    """
    rng = random.Random(seed)

    # Normalize weights
    total_weight = sum(op_weights.values())
    normalized = {k: v / total_weight for k, v in op_weights.items()}

    # Pre-generate keys and values
    keys = generate_keys(size, distribution, seed)
    values = generate_values(size, seed + 1000)

    operations = []
    inserted_keys = set()

    for i in range(size):
        # Select operation based on weights
        r = rng.random()
        cumulative = 0.0
        op_type = OP_INSERT

        for op, weight in normalized.items():
            cumulative += weight
            if r < cumulative:
                op_type = op
                break

        key = keys[i]

        if op_type == OP_INSERT:
            operations.append({
                "op": OP_INSERT,
                "key": key,
                "value": values[i],
            })
            inserted_keys.add(key)
        elif op_type == OP_GET:
            # For gets, prefer keys we've inserted
            if inserted_keys and rng.random() < 0.8:
                key = rng.choice(list(inserted_keys))
            operations.append({
                "op": OP_GET,
                "key": key,
            })
        elif op_type == OP_DELETE:
            # For deletes, prefer keys we've inserted
            if inserted_keys and rng.random() < 0.8:
                key = rng.choice(list(inserted_keys))
                inserted_keys.discard(key)
            operations.append({
                "op": OP_DELETE,
                "key": key,
            })

    return {
        "name": name,
        "description": f"{name} workload with {distribution} key distribution",
        "size": size,
        "distribution": distribution,
        "operation_weights": op_weights,
        "seed": seed,
        "operations": operations,
    }


def main():
    """Generate all workloads."""
    root = Path(__file__).parent.parent
    workloads_dir = root / "workloads" / "map"
    workloads_dir.mkdir(parents=True, exist_ok=True)

    # Workload configurations
    workload_configs = [
        # Insert-heavy: 100% inserts
        ("insert_heavy", {OP_INSERT: 1.0, OP_GET: 0.0, OP_DELETE: 0.0}),
        # Read-heavy: 95% gets, 5% inserts
        ("read_heavy", {OP_INSERT: 0.05, OP_GET: 0.95, OP_DELETE: 0.0}),
        # Mixed: 80% gets, 20% inserts
        ("mixed", {OP_INSERT: 0.20, OP_GET: 0.80, OP_DELETE: 0.0}),
        # Delete-heavy: 60% gets, 20% inserts, 20% deletes
        ("delete_heavy", {OP_INSERT: 0.20, OP_GET: 0.60, OP_DELETE: 0.20}),
    ]

    distributions = ["uniform", "zipf"]

    generated = []

    for size_name, size in SIZES.items():
        for workload_name, op_weights in workload_configs:
            for dist in distributions:
                name = f"{workload_name}_{dist}_{size_name}"
                seed_key = f"{workload_name}_{dist}"
                seed = SEEDS.get(seed_key, hash(seed_key) % 10000)

                print(f"Generating {name}...")

                workload = generate_workload(
                    name=name,
                    size=size,
                    distribution=dist,
                    op_weights=op_weights,
                    seed=seed + SIZES[size_name],  # Vary seed by size
                )

                filename = f"{name}.json"
                filepath = workloads_dir / filename

                with open(filepath, "w") as f:
                    json.dump(workload, f, indent=2)

                generated.append(filename)

    # Write manifest
    manifest = {
        "workloads": generated,
        "sizes": SIZES,
        "distributions": distributions,
        "seeds": SEEDS,
    }

    with open(workloads_dir / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nGenerated {len(generated)} workloads in {workloads_dir}")
    print("Manifest written to manifest.json")


if __name__ == "__main__":
    main()
