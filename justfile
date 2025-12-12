# dsa-lab justfile
# https://github.com/casey/just

set shell := ["bash", "-cu"]

# Default recipe
default:
    @just --list

# Project root
root := justfile_directory()

# =============================================================================
# BOOTSTRAP
# =============================================================================

# Set up development environment
bootstrap:
    @echo "==> Setting up Python virtual environment..."
    python3 -m venv {{root}}/tools/.venv
    {{root}}/tools/.venv/bin/pip install --upgrade pip
    {{root}}/tools/.venv/bin/pip install -r {{root}}/tools/requirements.txt
    @echo "==> Checking Rust toolchain..."
    rustc --version || echo "WARNING: Rust not installed"
    @echo "==> Checking C++ toolchain..."
    cmake --version || echo "WARNING: CMake not installed"
    g++ --version || echo "WARNING: g++ not installed"
    @echo "==> Checking Go toolchain..."
    go version || echo "WARNING: Go not installed"
    @echo "==> Bootstrap complete!"

# =============================================================================
# WORKLOAD GENERATION
# =============================================================================

# Generate all workloads
gen:
    @echo "==> Generating workloads..."
    {{root}}/tools/.venv/bin/python {{root}}/tools/gen_workloads.py
    @echo "==> Workloads generated in workloads/"

# =============================================================================
# FORMATTING
# =============================================================================

# Format all code
fmt: fmt-rust fmt-cpp fmt-go fmt-python

# Format Rust code
fmt-rust:
    @echo "==> Formatting Rust..."
    cd {{root}}/impl/rust && cargo fmt

# Format C++ code
fmt-cpp:
    @echo "==> Formatting C++..."
    find {{root}}/impl/cpp/src {{root}}/impl/cpp/tests {{root}}/impl/cpp/bench -name '*.cpp' -o -name '*.hpp' | xargs -r clang-format -i || echo "clang-format not available"

# Format Go code
fmt-go:
    @echo "==> Formatting Go..."
    cd {{root}}/impl/go && go fmt ./...

# Format Python code
fmt-python:
    @echo "==> Formatting Python..."
    {{root}}/tools/.venv/bin/python -m black {{root}}/impl/python {{root}}/tools || echo "black not available"

# =============================================================================
# TESTING
# =============================================================================

# Run all tests
test: test-rust test-cpp test-go test-python

# Run Rust tests
test-rust:
    @echo "==> Running Rust tests..."
    cd {{root}}/impl/rust && cargo test

# Run C++ tests
test-cpp:
    #!/usr/bin/env bash
    set -eu
    echo "==> Building and running C++ tests..."
    if ! command -v cmake &>/dev/null; then echo "SKIP: cmake not installed"; exit 0; fi
    if ! command -v ninja &>/dev/null; then echo "SKIP: ninja not installed"; exit 0; fi
    cmake -S {{root}}/impl/cpp -B {{root}}/impl/cpp/build -G Ninja -DCMAKE_BUILD_TYPE=Release
    cmake --build {{root}}/impl/cpp/build --target dsa_tests
    {{root}}/impl/cpp/build/dsa_tests

# Run Go tests
test-go:
    @echo "==> Running Go tests..."
    cd {{root}}/impl/go && go test ./...

# Run Python tests
test-python:
    @echo "==> Running Python tests..."
    cd {{root}}/impl/python && {{root}}/tools/.venv/bin/pytest tests/ -v

# =============================================================================
# BENCHMARKING
# =============================================================================

# Run all benchmarks
bench: bench-rust bench-cpp bench-go bench-python

# Run Rust benchmarks
bench-rust:
    @echo "==> Running Rust benchmarks..."
    cd {{root}}/impl/rust && cargo bench -- --save-baseline main 2>/dev/null || cargo bench
    @mkdir -p {{root}}/reports/raw
    @cp -r {{root}}/impl/rust/target/criterion {{root}}/reports/raw/rust_criterion 2>/dev/null || true

# Run C++ benchmarks
bench-cpp:
    #!/usr/bin/env bash
    set -eu
    echo "==> Building and running C++ benchmarks..."
    if ! command -v cmake &>/dev/null; then echo "SKIP: cmake not installed"; exit 0; fi
    if ! command -v ninja &>/dev/null; then echo "SKIP: ninja not installed"; exit 0; fi
    cmake -S {{root}}/impl/cpp -B {{root}}/impl/cpp/build -G Ninja -DCMAKE_BUILD_TYPE=Release
    cmake --build {{root}}/impl/cpp/build --target dsa_bench
    mkdir -p {{root}}/reports/raw
    {{root}}/impl/cpp/build/dsa_bench --benchmark_format=json > {{root}}/reports/raw/cpp_bench.json

# Run Go benchmarks
bench-go:
    @echo "==> Running Go benchmarks..."
    @mkdir -p {{root}}/reports/raw
    cd {{root}}/impl/go && go test -bench=. -benchmem ./... | tee {{root}}/reports/raw/go_bench.txt

# Run Python benchmarks
bench-python:
    @echo "==> Running Python benchmarks..."
    @mkdir -p {{root}}/reports/raw
    cd {{root}}/impl/python && {{root}}/tools/.venv/bin/pytest bench/ -v --benchmark-json={{root}}/reports/raw/python_bench.json

# =============================================================================
# REPORTING
# =============================================================================

# Generate benchmark report
report:
    @echo "==> Generating benchmark report..."
    {{root}}/tools/.venv/bin/python {{root}}/tools/report.py
    @echo "==> Report written to reports/latest.md"

# Capture environment info
env-capture:
    @echo "==> Capturing environment..."
    {{root}}/tools/.venv/bin/python {{root}}/tools/env_capture.py

# =============================================================================
# CI
# =============================================================================

# Run CI checks (format check + tests)
ci: ci-fmt test

# Check formatting (non-destructive)
ci-fmt:
    #!/usr/bin/env bash
    set -eu
    echo "==> Checking Rust formatting..."
    cd {{root}}/impl/rust && cargo fmt --check
    echo "==> Checking Go formatting..."
    cd {{root}}/impl/go && test -z "$(gofmt -l .)"
    echo "==> Formatting checks passed!"

# =============================================================================
# CLEAN
# =============================================================================

# Clean all build artifacts
clean:
    @echo "==> Cleaning Rust..."
    cd {{root}}/impl/rust && cargo clean
    @echo "==> Cleaning C++..."
    rm -rf {{root}}/impl/cpp/build
    @echo "==> Cleaning Go..."
    cd {{root}}/impl/go && go clean
    @echo "==> Cleaning Python..."
    find {{root}}/impl/python -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    find {{root}}/impl/python -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
    @echo "==> Clean complete!"
