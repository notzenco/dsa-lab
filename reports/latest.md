# dsa-lab Benchmark Report

**Generated:** 2025-12-12 23:32:09

## Environment

| Property | Value |
|----------|-------|
| timestamp | 2025-12-12T22:47:31.014034 |
| system | {'os': 'Linux', 'os_release': '6.6.87.2-microsoft-standard-WSL2', 'os_version': '#1 SMP PREEMPT_DYNAMIC Thu Jun  5 18:30:46 UTC 2025', 'hostname': 'desktop'} |
| cpu | {'processor': 'unknown', 'architecture': 'x86_64', 'model': 'Intel(R) Core(TM) i7-10700K CPU @ 3.80GHz', 'cores': 16} |
| memory | {'total_gb': 15.58} |
| toolchains | {'rust': {'rustc': 'rustc 1.91.1 (ed61e7d7e 2025-11-07)', 'cargo': 'cargo 1.91.1 (ea2d97820 2025-10-10)'}, 'cpp': {'g++': 'g++ (Debian 14.3.0-10) 14.3.0', 'clang++': 'Debian clang version 19.1.7 (3+b2)'}, 'go': {'go': 'go version go1.24.4 linux/amd64'}, 'python': {'python': '3.13.7', 'implementation': 'CPython'}} |

## Results Summary

### Hash Map Operations

| Benchmark | Rust | C++ | Go | Python |
|-----------|------|-----|-------|--------|
| BM_Get/100 | - | 2.29 us | - | - |
| BM_Get/10000 | - | 382.64 us | - | - |
| BM_Get/4096 | - | 129.31 us | - | - |
| BM_Get/512 | - | 14.40 us | - | - |
| BM_Insert/100 | - | 12.37 us | - | - |
| BM_Insert/10000 | - | 1.91 ms | - | - |
| BM_Insert/4096 | - | 864.26 us | - | - |
| BM_Insert/512 | - | 82.23 us | - | - |
| BM_InsertHeavyUniformMedium | - | 0.00 ns | - | - |
| BM_MixedUniformMedium | - | 0.00 ns | - | - |
| BM_ReadHeavyUniformMedium | - | 0.00 ns | - | - |
| BenchmarkInsertHeavyUniformMedium | - | - | 1.32 ms | - |
| BenchmarkMixedUniformMedium | - | - | 605.16 us | - |
| BenchmarkReadHeavyUniformMedium | - | - | 449.40 us | - |
| test_get[10000] | - | - | - | 5.09 ms |
| test_get[1000] | - | - | - | 452.49 us |
| test_get[100] | - | - | - | 35.88 us |
| test_insert[10000] | - | - | - | 21.43 ms |
| test_insert[1000] | - | - | - | 2.23 ms |
| test_insert[100] | - | - | - | 208.41 us |
| test_insert_heavy_uniform_medium | - | - | - | 22.19 ms |
| test_mixed_uniform_medium | - | - | - | 9.76 ms |
| test_read_heavy_uniform_medium | - | - | - | 6.48 ms |

## C++ (Google Benchmark)

| Benchmark | Mean Time |
|-----------|-----------|
| BM_Get/100 | 2.29 us |
| BM_Get/10000 | 382.64 us |
| BM_Get/4096 | 129.31 us |
| BM_Get/512 | 14.40 us |
| BM_Insert/100 | 12.37 us |
| BM_Insert/10000 | 1.91 ms |
| BM_Insert/4096 | 864.26 us |
| BM_Insert/512 | 82.23 us |
| BM_InsertHeavyUniformMedium | 0.00 ns |
| BM_MixedUniformMedium | 0.00 ns |
| BM_ReadHeavyUniformMedium | 0.00 ns |

## Go (testing.B)

| Benchmark | Mean Time |
|-----------|-----------|
| BenchmarkInsertHeavyUniformMedium | 1.32 ms |
| BenchmarkMixedUniformMedium | 605.16 us |
| BenchmarkReadHeavyUniformMedium | 449.40 us |

## Python (pytest-benchmark)

| Benchmark | Mean Time |
|-----------|-----------|
| test_get[10000] | 5.09 ms |
| test_get[1000] | 452.49 us |
| test_get[100] | 35.88 us |
| test_insert[10000] | 21.43 ms |
| test_insert[1000] | 2.23 ms |
| test_insert[100] | 208.41 us |
| test_insert_heavy_uniform_medium | 22.19 ms |
| test_mixed_uniform_medium | 9.76 ms |
| test_read_heavy_uniform_medium | 6.48 ms |

## Notes

- All benchmarks run with release/optimized builds
- Times are mean values across multiple iterations
- Lower is better
- Results may vary based on system load and hardware
