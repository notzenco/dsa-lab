cmake_minimum_required(VERSION 3.20)
project(dsa_lab_cpp VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Compiler warnings
add_compile_options(-Wall -Wextra -Wpedantic)

# Release optimizations
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    add_compile_options(-O3 -DNDEBUG)
endif()

# Include directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src)

# Main library
add_library(dsa_lab
    src/hashmap.cpp
)

# Fetch dependencies
include(FetchContent)

# Google Test
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG v1.14.0
)
FetchContent_MakeAvailable(googletest)

# Google Benchmark
FetchContent_Declare(
    benchmark
    GIT_REPOSITORY https://github.com/google/benchmark.git
    GIT_TAG v1.8.3
)
set(BENCHMARK_ENABLE_TESTING OFF CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(benchmark)

# nlohmann/json for workload parsing
FetchContent_Declare(
    json
    GIT_REPOSITORY https://github.com/nlohmann/json.git
    GIT_TAG v3.11.3
)
FetchContent_MakeAvailable(json)

# Tests executable
add_executable(dsa_tests
    tests/hashmap_test.cpp
    tests/oracle_test.cpp
)
target_link_libraries(dsa_tests
    dsa_lab
    GTest::gtest_main
)

# Benchmark executable
add_executable(dsa_bench
    bench/hashmap_bench.cpp
)
target_link_libraries(dsa_bench
    dsa_lab
    benchmark::benchmark
    benchmark::benchmark_main
    nlohmann_json::nlohmann_json
)

# Enable testing
enable_testing()
add_test(NAME dsa_tests COMMAND dsa_tests)
