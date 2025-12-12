# Benchmarking Methodology

How benchmarks are designed, run, and interpreted in dsa-lab.

## Principles

1. **Reproducibility over speed**
   - Fixed seeds for all random data
   - Captured environment metadata
   - Deterministic workloads

2. **Scenarios over microbenchmarks**
   - Real operation mixes
   - Realistic key distributions
   - Representative data sizes

3. **Comparability across languages**
   - Same workloads
   - Same operation sequences
   - Equivalent build configurations

## Workload Design

### Operation Mixes

| Workload | Insert | Get | Delete | Use Case |
|----------|--------|-----|--------|----------|
| insert_heavy | 100% | 0% | 0% | Initial population |
| read_heavy | 5% | 95% | 0% | Cache, lookup tables |
| mixed | 20% | 80% | 0% | General purpose |
| delete_heavy | 20% | 60% | 20% | Session stores, TTL |

### Key Distributions

**Uniform**
- Each key equally likely
- Tests average-case performance
- Seed: deterministic PRNG

**Zipf**
- Power-law distribution (s=1.0)
- 20% of keys = 80% of accesses
- Tests hot-key scenarios

### Sizes

| Size | Operations | Purpose |
|------|------------|---------|
| small | 1,000 | Quick iteration, cache-hot |
| medium | 10,000 | Standard benchmark |
| large | 100,000 | Scale testing |

## Build Configuration

All benchmarks run with **release/optimized** builds:

### Rust
```toml
[profile.release]
opt-level = 3
lto = true
```

### C++
```cmake
-DCMAKE_BUILD_TYPE=Release
-O3 -DNDEBUG
```

### Go
```bash
go test -bench=. -benchmem
```
(Go compiler optimizes automatically)

### Python
```bash
pytest-benchmark
```
(Interpreted, measures real performance)

## Warm-up

Each benchmark framework handles warm-up:

- **Criterion (Rust)**: Automatic warm-up iterations
- **Google Benchmark (C++)**: Automatic warm-up
- **testing.B (Go)**: b.ResetTimer() after setup
- **pytest-benchmark (Python)**: Configurable warm-up rounds

## Measurement

### What We Measure

1. **Throughput**: Operations per second
2. **Latency**: Time per operation (mean, stddev)
3. **Memory**: Peak allocation (where supported)

### Statistical Treatment

- Multiple iterations (framework-determined)
- Report mean and standard deviation
- Outlier detection (framework-specific)

## Environment Capture

Every benchmark run captures:

```json
{
  "timestamp": "ISO8601",
  "system": {
    "os": "Linux",
    "os_release": "5.15.0",
    "hostname": "bench-machine"
  },
  "cpu": {
    "model": "AMD Ryzen 9 5900X",
    "cores": 12
  },
  "memory": {
    "total_gb": 64
  },
  "toolchains": {
    "rust": {"rustc": "1.75.0"},
    "cpp": {"g++": "13.1.0"},
    "go": {"go": "1.21.5"},
    "python": {"python": "3.11.5"}
  }
}
```

## Running Benchmarks

```bash
# Generate workloads first
just gen

# Run all benchmarks
just bench

# Run specific language
just bench-rust
just bench-cpp
just bench-go
just bench-python

# Generate report
just report
```

## Interpreting Results

### Good Indicators
- Low variance (< 5% of mean)
- Consistent across runs
- Expected scaling (O(1) for hash ops)

### Warning Signs
- High variance (> 20%)
- Bimodal distribution (resize events)
- Unexpected scaling (O(n) suggests probe chains)

### Comparing Languages

Direct comparison caveats:
- Different memory models
- Different string representations
- Different default hash functions

Fair comparisons:
- Same workload, same seed
- Same operation count
- Release builds only
