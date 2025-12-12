# dsa-lab

A product-grade monorepo for multi-language Data Structures & Algorithms implementations with reproducible benchmarks.

## Quick Start

```bash
# Install just (https://github.com/casey/just)
cargo install just

# Bootstrap the environment
just bootstrap

# Generate workloads
just gen

# Run all tests
just test

# Run benchmarks
just bench

# Generate report
just report
```

## Supported Languages

| Language | Build System | Test Framework | Benchmark Framework |
|----------|--------------|----------------|---------------------|
| Rust     | Cargo        | built-in       | Criterion           |
| C++      | CMake/Ninja  | Google Test    | Google Benchmark    |
| Go       | Go Modules   | testing        | testing.B           |
| Python   | pyproject    | pytest         | pytest-benchmark    |

## Repository Structure

```
dsa-lab/
  README.md              # This file
  LICENSE                # MIT License
  .gitignore             # Git ignore patterns
  .editorconfig          # Editor configuration
  justfile               # Task runner commands

  tools/                 # Build/test tooling
    requirements.txt     # Python dependencies
    gen_workloads.py     # Workload generator
    report.py            # Benchmark report generator
    env_capture.py       # Environment metadata capture

  docs/                  # Documentation
    CONTRACT.md          # Interface contracts and invariants
    DECISION_GUIDE.md    # When to use what
    BENCH_METHOD.md      # Benchmarking methodology
    DATASETS.md          # Dataset specifications
    STYLE.md             # Code style guidelines

  workloads/             # Generated test workloads
    map/                 # Hash map workloads

  reports/               # Benchmark reports
    latest.md            # Most recent benchmark results
    history/             # Historical reports

  impl/                  # Implementations
    rust/                # Rust implementation
    cpp/                 # C++ implementation
    go/                  # Go implementation
    python/              # Python implementation

  .github/workflows/     # CI/CD
    ci.yml               # Continuous integration
    bench.yml            # Benchmark workflow
```

## MVP: Hash Map

The initial implementation focuses on a hash map with open addressing (linear probing).

### Workload Types

- **insert-heavy**: 100% insert operations
- **read-heavy**: 95% get / 5% insert
- **mixed**: 80% get / 20% insert
- **delete-heavy**: 60% get / 20% insert / 20% delete

### Key Distributions

- Uniform random
- Zipf (skewed access patterns)

## Development

```bash
# Format all code
just fmt

# Run CI checks locally
just ci

# Run specific language tests
just test-rust
just test-cpp
just test-go
just test-python

# Run specific language benchmarks
just bench-rust
just bench-cpp
just bench-go
just bench-python
```

## Requirements

- Rust 1.70+
- CMake 3.20+ with Ninja
- Go 1.21+
- Python 3.10+
- just (task runner)

## License

MIT License - see [LICENSE](LICENSE) for details.
