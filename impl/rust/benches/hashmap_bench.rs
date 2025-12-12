//! Benchmarks for HashMap implementation

use criterion::{black_box, criterion_group, criterion_main, BenchmarkId, Criterion};
use dsa_lab::HashMap;
use serde::Deserialize;
use std::fs;
use std::path::Path;

#[derive(Debug, Deserialize)]
struct Operation {
    op: String,
    key: String,
    value: Option<String>,
}

#[derive(Debug, Deserialize)]
struct Workload {
    name: String,
    size: usize,
    operations: Vec<Operation>,
}

fn load_workload(name: &str) -> Option<Workload> {
    let workload_dir = Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .parent()
        .unwrap()
        .join("workloads")
        .join("map");

    let path = workload_dir.join(format!("{}.json", name));
    if !path.exists() {
        return None;
    }

    let content = fs::read_to_string(path).ok()?;
    serde_json::from_str(&content).ok()
}

fn bench_workload(c: &mut Criterion, workload_name: &str) {
    let workload = match load_workload(workload_name) {
        Some(w) => w,
        None => {
            eprintln!("Workload {} not found, skipping", workload_name);
            return;
        }
    };

    c.bench_with_input(
        BenchmarkId::new("hashmap", &workload.name),
        &workload,
        |b, workload| {
            b.iter(|| {
                let mut map: HashMap<String, String> = HashMap::new();
                for op in &workload.operations {
                    match op.op.as_str() {
                        "insert" => {
                            map.insert(
                                black_box(op.key.clone()),
                                black_box(op.value.clone().unwrap_or_default()),
                            );
                        }
                        "get" => {
                            black_box(map.get(&op.key));
                        }
                        "delete" => {
                            black_box(map.remove(&op.key));
                        }
                        _ => {}
                    }
                }
                map
            })
        },
    );
}

fn bench_insert_only(c: &mut Criterion) {
    let sizes = [100, 1000, 10000];

    let mut group = c.benchmark_group("insert");
    for size in sizes {
        group.bench_with_input(BenchmarkId::from_parameter(size), &size, |b, &size| {
            let keys: Vec<String> = (0..size).map(|i| format!("key_{}", i)).collect();
            let values: Vec<String> = (0..size).map(|i| format!("value_{}", i)).collect();

            b.iter(|| {
                let mut map: HashMap<String, String> = HashMap::new();
                for (key, value) in keys.iter().zip(values.iter()) {
                    map.insert(black_box(key.clone()), black_box(value.clone()));
                }
                map
            })
        });
    }
    group.finish();
}

fn bench_get_only(c: &mut Criterion) {
    let sizes = [100, 1000, 10000];

    let mut group = c.benchmark_group("get");
    for size in sizes {
        group.bench_with_input(BenchmarkId::from_parameter(size), &size, |b, &size| {
            let keys: Vec<String> = (0..size).map(|i| format!("key_{}", i)).collect();
            let values: Vec<String> = (0..size).map(|i| format!("value_{}", i)).collect();

            let mut map: HashMap<String, String> = HashMap::new();
            for (key, value) in keys.iter().zip(values.iter()) {
                map.insert(key.clone(), value.clone());
            }

            b.iter(|| {
                for key in &keys {
                    black_box(map.get(key));
                }
            })
        });
    }
    group.finish();
}

fn bench_mixed(c: &mut Criterion) {
    bench_workload(c, "mixed_uniform_medium");
}

fn bench_insert_heavy(c: &mut Criterion) {
    bench_workload(c, "insert_heavy_uniform_medium");
}

fn bench_read_heavy(c: &mut Criterion) {
    bench_workload(c, "read_heavy_uniform_medium");
}

criterion_group!(
    benches,
    bench_insert_only,
    bench_get_only,
    bench_mixed,
    bench_insert_heavy,
    bench_read_heavy,
);
criterion_main!(benches);
