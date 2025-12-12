#include "hashmap.hpp"
#include <benchmark/benchmark.h>
#include <nlohmann/json.hpp>
#include <fstream>
#include <string>
#include <vector>

using namespace dsa_lab;
using json = nlohmann::json;

struct Operation {
    std::string op;
    std::string key;
    std::string value;
};

struct Workload {
    std::string name;
    size_t size;
    std::vector<Operation> operations;
};

std::optional<Workload> load_workload(const std::string& name) {
    // Find workload directory relative to benchmark
    std::string workload_path = "../../workloads/map/" + name + ".json";

    std::ifstream file(workload_path);
    if (!file.is_open()) {
        // Try alternative path
        workload_path = "../../../workloads/map/" + name + ".json";
        file.open(workload_path);
        if (!file.is_open()) {
            return std::nullopt;
        }
    }

    json j;
    file >> j;

    Workload workload;
    workload.name = j["name"];
    workload.size = j["size"];

    for (const auto& op : j["operations"]) {
        Operation o;
        o.op = op["op"];
        o.key = op["key"];
        if (op.contains("value")) {
            o.value = op["value"];
        }
        workload.operations.push_back(o);
    }

    return workload;
}

static void BM_Insert(benchmark::State& state) {
    size_t n = state.range(0);
    std::vector<std::string> keys(n);
    std::vector<std::string> values(n);

    for (size_t i = 0; i < n; i++) {
        keys[i] = "key_" + std::to_string(i);
        values[i] = "value_" + std::to_string(i);
    }

    for (auto _ : state) {
        HashMap<std::string, std::string> map;
        for (size_t i = 0; i < n; i++) {
            map.insert(keys[i], values[i]);
        }
        benchmark::DoNotOptimize(map);
    }

    state.SetItemsProcessed(state.iterations() * n);
}
BENCHMARK(BM_Insert)->Range(100, 10000);

static void BM_Get(benchmark::State& state) {
    size_t n = state.range(0);
    std::vector<std::string> keys(n);

    HashMap<std::string, std::string> map;
    for (size_t i = 0; i < n; i++) {
        keys[i] = "key_" + std::to_string(i);
        map.insert(keys[i], "value_" + std::to_string(i));
    }

    for (auto _ : state) {
        for (const auto& key : keys) {
            benchmark::DoNotOptimize(map.get(key));
        }
    }

    state.SetItemsProcessed(state.iterations() * n);
}
BENCHMARK(BM_Get)->Range(100, 10000);

static void BM_MixedUniformMedium(benchmark::State& state) {
    auto workload = load_workload("mixed_uniform_medium");
    if (!workload) {
        state.SkipWithError("Workload not found");
        return;
    }

    for (auto _ : state) {
        HashMap<std::string, std::string> map;
        for (const auto& op : workload->operations) {
            if (op.op == "insert") {
                map.insert(op.key, op.value);
            } else if (op.op == "get") {
                benchmark::DoNotOptimize(map.get(op.key));
            } else if (op.op == "delete") {
                benchmark::DoNotOptimize(map.remove(op.key));
            }
        }
        benchmark::DoNotOptimize(map);
    }

    state.SetItemsProcessed(state.iterations() * workload->size);
}
BENCHMARK(BM_MixedUniformMedium);

static void BM_InsertHeavyUniformMedium(benchmark::State& state) {
    auto workload = load_workload("insert_heavy_uniform_medium");
    if (!workload) {
        state.SkipWithError("Workload not found");
        return;
    }

    for (auto _ : state) {
        HashMap<std::string, std::string> map;
        for (const auto& op : workload->operations) {
            if (op.op == "insert") {
                map.insert(op.key, op.value);
            }
        }
        benchmark::DoNotOptimize(map);
    }

    state.SetItemsProcessed(state.iterations() * workload->size);
}
BENCHMARK(BM_InsertHeavyUniformMedium);

static void BM_ReadHeavyUniformMedium(benchmark::State& state) {
    auto workload = load_workload("read_heavy_uniform_medium");
    if (!workload) {
        state.SkipWithError("Workload not found");
        return;
    }

    for (auto _ : state) {
        HashMap<std::string, std::string> map;
        for (const auto& op : workload->operations) {
            if (op.op == "insert") {
                map.insert(op.key, op.value);
            } else if (op.op == "get") {
                benchmark::DoNotOptimize(map.get(op.key));
            }
        }
        benchmark::DoNotOptimize(map);
    }

    state.SetItemsProcessed(state.iterations() * workload->size);
}
BENCHMARK(BM_ReadHeavyUniformMedium);
