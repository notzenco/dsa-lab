# Decision Guide

When to use which hash map implementation and key design decisions.

## Language Selection

| Use Case | Recommended | Rationale |
|----------|-------------|-----------|
| Maximum performance | Rust, C++ | Zero-cost abstractions, no GC |
| Quick prototyping | Python | Rapid iteration, easy debugging |
| Concurrent workloads | Go | Built-in concurrency primitives |
| Memory-constrained | Rust, C++ | Fine-grained control |
| Learning/education | Python | Clear, readable implementations |

## Open Addressing vs Chaining

### Open Addressing (Linear Probing)
**Chosen as default implementation**

Pros:
- Better cache locality
- Lower memory overhead (no node allocations)
- Simpler memory management

Cons:
- Clustering can degrade performance
- Deletion requires tombstones
- Performance degrades sharply at high load factors

Best for:
- Read-heavy workloads
- Known maximum size
- Cache-sensitive applications

### Chaining
**Alternative implementation**

Pros:
- Stable performance at high load factors
- Simple deletion (no tombstones)
- Can exceed load factor of 1.0

Cons:
- Poor cache locality
- Memory allocation per entry
- Pointer chasing overhead

Best for:
- Write-heavy workloads
- Unknown or highly variable size
- When deletion is frequent

## Load Factor Tuning

| Load Factor | Trade-off |
|-------------|-----------|
| 0.5 | Fast lookups, high memory usage |
| 0.75 | **Default** - balanced |
| 0.9 | Memory efficient, slower at capacity |

## Key Distribution Considerations

### Uniform Keys
- Standard case
- All hash buckets equally likely
- Predictable performance

### Zipf (Skewed) Keys
- Real-world access patterns (hot keys)
- Benefits from caching
- May cause clustering in open addressing

## Anti-Patterns to Avoid

1. **Premature optimization**
   - Start with language standard library
   - Profile before implementing custom

2. **Wrong collision resolution for workload**
   - Don't use linear probing for delete-heavy workloads
   - Don't use chaining for cache-sensitive code

3. **Ignoring load factor**
   - Always resize before hitting maximum
   - Don't let load factor exceed 0.9

4. **Poor hash functions**
   - Don't use simple modulo for string keys
   - Don't use identity hash for sequential integers

5. **Forgetting tombstones**
   - Open addressing requires tombstones for deletion
   - Not cleaning tombstones causes probe chain growth

## Benchmark Interpretation

### What to measure
- Throughput (ops/sec)
- Latency (p50, p95, p99)
- Memory usage

### What to watch for
- Variance indicates instability
- Bimodal distributions suggest resizing impact
- Memory growth without size growth = leak

### Common pitfalls
- Microbenchmarks don't reflect real workloads
- Warm-up effects (first iteration slower)
- JIT compilation effects (Go, Python)
