# Hash Map Contract

This document defines the interface contract and invariants for all hash map implementations in dsa-lab.

## Interface

All implementations MUST provide the following operations:

### Core Operations

```
insert(key: string, value: string) -> Option<string>
```
- Insert a key-value pair into the map
- Returns the previous value if the key existed, None otherwise
- Time complexity: O(1) amortized

```
get(key: string) -> Option<string>
```
- Retrieve the value associated with a key
- Returns None if the key does not exist
- Time complexity: O(1) average

```
remove(key: string) -> Option<string>
```
- Remove a key-value pair from the map
- Returns the removed value if the key existed, None otherwise
- Time complexity: O(1) average

```
contains(key: string) -> bool
```
- Check if a key exists in the map
- Time complexity: O(1) average

```
len() -> usize
```
- Return the number of key-value pairs in the map
- Time complexity: O(1)

```
is_empty() -> bool
```
- Return true if the map contains no elements
- Time complexity: O(1)

```
clear()
```
- Remove all key-value pairs from the map
- Time complexity: O(n)

## Invariants

All implementations MUST maintain these invariants:

1. **Uniqueness**: Each key appears at most once in the map
2. **Consistency**: `get(k)` returns `v` if and only if `insert(k, v)` was the last operation on key `k` (and no `remove(k)` followed)
3. **Size accuracy**: `len()` always returns the exact number of key-value pairs
4. **Empty consistency**: `is_empty()` returns `true` iff `len() == 0`

## Implementation Requirements

### Hash Function
- Use a deterministic hash function
- For string keys, use a well-distributed hash (FNV-1a, xxHash, or language default)

### Collision Resolution
- **Primary**: Open addressing with linear probing
- **Alternative**: Chaining (document if used)

### Load Factor
- Default maximum load factor: 0.75
- Resize by 2x when load factor exceeded

### Memory
- Implementations should not leak memory
- Clear should free/reuse internal storage

## Testing Requirements

Each implementation must pass:

1. **Unit tests**: Edge cases (empty map, single element, etc.)
2. **Oracle tests**: Compare behavior against language's standard map
3. **Stress tests**: Large numbers of operations without crashes

## Semantic Equivalence

All implementations must produce identical observable behavior:

```
Given the same sequence of operations,
all implementations must return the same results
(accounting for iteration order being undefined)
```

Note: Iteration order is NOT guaranteed to be consistent across implementations.

## Error Handling

- Out of memory: Implementation-specific (crash or return error)
- Invalid input: Undefined behavior (callers must validate)

## Thread Safety

- Base implementations are NOT thread-safe
- Thread-safe variants may be provided separately (with `_sync` suffix)
