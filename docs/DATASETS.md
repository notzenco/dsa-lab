# Dataset Specifications

This document describes the workload datasets used for benchmarking.

## Workload Schema

All workloads are stored as JSON files with the following schema:

```json
{
  "name": "string",
  "description": "string",
  "size": "integer",
  "distribution": "uniform | zipf",
  "operation_weights": {
    "insert": "float (0-1)",
    "get": "float (0-1)",
    "delete": "float (0-1)"
  },
  "seed": "integer",
  "operations": [
    {
      "op": "insert | get | delete",
      "key": "string",
      "value": "string (only for insert)"
    }
  ]
}
```

## Generated Workloads

### By Operation Mix

#### insert_heavy
- 100% insert operations
- Use case: Initial table population
- Expected behavior: Continuous growth, periodic resizes

#### read_heavy
- 95% get, 5% insert
- Use case: Cache lookups, configuration stores
- Expected behavior: Mostly hits after warm-up

#### mixed
- 80% get, 20% insert
- Use case: General-purpose map usage
- Expected behavior: Balanced read/write

#### delete_heavy
- 60% get, 20% insert, 20% delete
- Use case: Session stores, LRU caches
- Expected behavior: Size fluctuation, tombstone accumulation

### By Distribution

#### Uniform
- Keys selected uniformly at random
- Range: 0 to 10 * workload_size
- Tests: Average-case performance

#### Zipf
- Keys follow Zipf distribution (s=1.0)
- Hot keys: Top 20% keys = 80% of operations
- Tests: Real-world access patterns, caching effects

### By Size

| Name | Operations | File Size (approx) |
|------|------------|-------------------|
| small | 1,000 | ~50 KB |
| medium | 10,000 | ~500 KB |
| large | 100,000 | ~5 MB |

## Seed Values

Fixed seeds ensure reproducibility:

| Workload | Seed Base |
|----------|-----------|
| insert_heavy_uniform | 42 |
| insert_heavy_zipf | 43 |
| read_heavy_uniform | 44 |
| read_heavy_zipf | 45 |
| mixed_uniform | 46 |
| mixed_zipf | 47 |
| delete_heavy_uniform | 48 |
| delete_heavy_zipf | 49 |

Actual seed = base + size (1000, 10000, or 100000)

## File Naming Convention

```
{workload_type}_{distribution}_{size}.json
```

Examples:
- `insert_heavy_uniform_small.json`
- `read_heavy_zipf_large.json`
- `mixed_uniform_medium.json`

## Manifest File

`workloads/map/manifest.json` lists all generated workloads:

```json
{
  "workloads": ["file1.json", "file2.json", ...],
  "sizes": {"small": 1000, "medium": 10000, "large": 100000},
  "distributions": ["uniform", "zipf"],
  "seeds": {...}
}
```

## Regenerating Workloads

```bash
# Generate all workloads
just gen

# Or run directly
python tools/gen_workloads.py
```

## Adding Custom Workloads

1. Edit `tools/gen_workloads.py`
2. Add new configuration to `workload_configs`
3. Add seed to `SEEDS` dict
4. Run `just gen`

## Validation

Workloads can be validated by:

1. **Schema validation**: JSON structure matches expected format
2. **Operation counts**: Total operations match `size` field
3. **Seed reproducibility**: Same seed produces identical workload
