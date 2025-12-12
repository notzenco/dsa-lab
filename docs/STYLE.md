# Code Style Guidelines

Style conventions for each language in dsa-lab.

## General Principles

1. **Clarity over cleverness**: Code should be readable
2. **Consistency**: Follow language idioms
3. **Minimal comments**: Self-documenting code preferred
4. **Test coverage**: All public APIs must have tests

## Rust

### Formatting
```bash
cargo fmt
```

### Style Guide
- Follow [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- Use `rustfmt` defaults
- Prefer `Result` over `Option` for operations that can fail

### Naming
```rust
// Types: PascalCase
struct HashMap<K, V> { ... }

// Functions/methods: snake_case
fn insert(&mut self, key: K, value: V) -> Option<V>

// Constants: SCREAMING_SNAKE_CASE
const DEFAULT_CAPACITY: usize = 16;
```

### Documentation
```rust
/// Insert a key-value pair into the map.
///
/// Returns the previous value if the key existed.
pub fn insert(&mut self, key: K, value: V) -> Option<V>
```

## C++

### Formatting
```bash
clang-format -i src/*.cpp
```

### Style Guide
- Google C++ Style Guide (modified)
- C++17 minimum
- Prefer `std::optional` over pointer returns

### Naming
```cpp
// Types: PascalCase
class HashMap { ... };

// Functions/methods: snake_case
auto insert(std::string key, std::string value) -> std::optional<std::string>;

// Constants: kPascalCase
constexpr size_t kDefaultCapacity = 16;

// Member variables: trailing underscore
size_t size_;
```

### Headers
```cpp
#pragma once  // Preferred over include guards

#include <string>
#include <optional>
```

## Go

### Formatting
```bash
go fmt ./...
```

### Style Guide
- Follow [Effective Go](https://go.dev/doc/effective_go)
- Use `gofmt` (enforced)
- Exported names start with uppercase

### Naming
```go
// Types: PascalCase (exported)
type HashMap struct { ... }

// Functions/methods: PascalCase (exported) or camelCase (unexported)
func (m *HashMap) Insert(key, value string) (string, bool)

// Constants: PascalCase or camelCase
const DefaultCapacity = 16
```

### Error Handling
```go
// Return error as last value
func (m *HashMap) Get(key string) (string, bool)
```

## Python

### Formatting
```bash
black .
```

### Style Guide
- PEP 8
- Type hints required for public APIs
- Docstrings for public functions

### Naming
```python
# Classes: PascalCase
class HashMap:
    ...

# Functions/methods: snake_case
def insert(self, key: str, value: str) -> Optional[str]:
    ...

# Constants: SCREAMING_SNAKE_CASE
DEFAULT_CAPACITY = 16
```

### Type Hints
```python
from typing import Optional, Dict

def insert(self, key: str, value: str) -> Optional[str]:
    """Insert a key-value pair.

    Args:
        key: The key to insert
        value: The value to associate

    Returns:
        The previous value if key existed, None otherwise
    """
```

## Build Flags

### Debug Build
For development and debugging:

| Language | Flags |
|----------|-------|
| Rust | `cargo build` (default) |
| C++ | `-DCMAKE_BUILD_TYPE=Debug` |
| Go | Default (includes race detector with `-race`) |
| Python | N/A |

### Release Build
For benchmarking and production:

| Language | Flags |
|----------|-------|
| Rust | `cargo build --release` |
| C++ | `-DCMAKE_BUILD_TYPE=Release -O3 -DNDEBUG` |
| Go | Default (optimized) |
| Python | N/A |

## Warnings

All languages should compile with warnings enabled:

### Rust
```toml
# Cargo.toml
[lints.rust]
warnings = "deny"
```

### C++
```cmake
add_compile_options(-Wall -Wextra -Wpedantic)
```

### Go
```bash
go vet ./...
```

### Python
```bash
# Use mypy for type checking
mypy --strict src/
```

## Pre-commit Checks

Before committing:

1. Format code: `just fmt`
2. Run tests: `just test`
3. Check lints: `just ci-fmt`
