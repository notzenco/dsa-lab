#!/usr/bin/env python3
"""
Benchmark Report Generator for dsa-lab

Merges benchmark results from all languages into a unified Markdown report.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


def parse_criterion_results(criterion_dir: Path) -> Dict[str, Any]:
    """Parse Rust Criterion benchmark results."""
    results = {}

    if not criterion_dir.exists():
        return results

    for bench_dir in criterion_dir.iterdir():
        if not bench_dir.is_dir() or bench_dir.name.startswith("."):
            continue

        # Look for estimates.json
        estimates_file = bench_dir / "new" / "estimates.json"
        if estimates_file.exists():
            with open(estimates_file) as f:
                data = json.load(f)

            mean_ns = data.get("mean", {}).get("point_estimate", 0)
            results[bench_dir.name] = {
                "mean_ns": mean_ns,
                "mean_us": mean_ns / 1000,
                "mean_ms": mean_ns / 1_000_000,
            }

    return results


def parse_google_bench_results(json_file: Path) -> Dict[str, Any]:
    """Parse Google Benchmark JSON output."""
    results = {}

    if not json_file.exists():
        return results

    with open(json_file) as f:
        data = json.load(f)

    for bench in data.get("benchmarks", []):
        name = bench.get("name", "unknown")
        time_ns = bench.get("real_time", 0)
        time_unit = bench.get("time_unit", "ns")

        # Normalize to nanoseconds
        if time_unit == "us":
            time_ns *= 1000
        elif time_unit == "ms":
            time_ns *= 1_000_000

        results[name] = {
            "mean_ns": time_ns,
            "mean_us": time_ns / 1000,
            "mean_ms": time_ns / 1_000_000,
        }

    return results


def parse_go_bench_results(txt_file: Path) -> Dict[str, Any]:
    """Parse Go benchmark text output."""
    results = {}

    if not txt_file.exists():
        return results

    with open(txt_file) as f:
        for line in f:
            # Match: BenchmarkName-8    1000000    1234 ns/op    456 B/op    7 allocs/op
            match = re.match(
                r"(Benchmark\w+)[-\d]*\s+\d+\s+([\d.]+)\s+(ns|us|ms)/op",
                line
            )
            if match:
                name = match.group(1)
                time_val = float(match.group(2))
                unit = match.group(3)

                # Normalize to nanoseconds
                if unit == "us":
                    time_val *= 1000
                elif unit == "ms":
                    time_val *= 1_000_000

                results[name] = {
                    "mean_ns": time_val,
                    "mean_us": time_val / 1000,
                    "mean_ms": time_val / 1_000_000,
                }

    return results


def parse_pytest_bench_results(json_file: Path) -> Dict[str, Any]:
    """Parse pytest-benchmark JSON output."""
    results = {}

    if not json_file.exists():
        return results

    with open(json_file) as f:
        data = json.load(f)

    for bench in data.get("benchmarks", []):
        name = bench.get("name", "unknown")
        stats = bench.get("stats", {})
        mean_s = stats.get("mean", 0)

        results[name] = {
            "mean_ns": mean_s * 1_000_000_000,
            "mean_us": mean_s * 1_000_000,
            "mean_ms": mean_s * 1000,
        }

    return results


def format_time(ns: float) -> str:
    """Format time in appropriate units."""
    if ns < 1000:
        return f"{ns:.2f} ns"
    elif ns < 1_000_000:
        return f"{ns/1000:.2f} us"
    elif ns < 1_000_000_000:
        return f"{ns/1_000_000:.2f} ms"
    else:
        return f"{ns/1_000_000_000:.2f} s"


def load_env_info(env_file: Path) -> Dict[str, str]:
    """Load environment info from JSON file."""
    if not env_file.exists():
        return {}

    with open(env_file) as f:
        return json.load(f)


def generate_report(root: Path) -> str:
    """Generate the full benchmark report."""
    raw_dir = root / "reports" / "raw"

    # Parse results from each language
    rust_results = parse_criterion_results(raw_dir / "rust_criterion")
    cpp_results = parse_google_bench_results(raw_dir / "cpp_bench.json")
    go_results = parse_go_bench_results(raw_dir / "go_bench.txt")
    python_results = parse_pytest_bench_results(raw_dir / "python_bench.json")

    # Load environment info
    env_info = load_env_info(raw_dir / "env.json")

    # Build report
    lines = [
        "# dsa-lab Benchmark Report",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]

    # Environment section
    if env_info:
        lines.extend([
            "## Environment",
            "",
            "| Property | Value |",
            "|----------|-------|",
        ])
        for key, value in env_info.items():
            lines.append(f"| {key} | {value} |")
        lines.append("")

    # Results summary
    lines.extend([
        "## Results Summary",
        "",
        "### Hash Map Operations",
        "",
    ])

    # Build comparison table
    all_benchmarks = set()
    all_benchmarks.update(rust_results.keys())
    all_benchmarks.update(cpp_results.keys())
    all_benchmarks.update(go_results.keys())
    all_benchmarks.update(python_results.keys())

    if all_benchmarks:
        lines.extend([
            "| Benchmark | Rust | C++ | Go | Python |",
            "|-----------|------|-----|-------|--------|",
        ])

        for bench in sorted(all_benchmarks):
            rust_time = format_time(rust_results.get(bench, {}).get("mean_ns", 0)) if bench in rust_results else "-"
            cpp_time = format_time(cpp_results.get(bench, {}).get("mean_ns", 0)) if bench in cpp_results else "-"
            go_time = format_time(go_results.get(bench, {}).get("mean_ns", 0)) if bench in go_results else "-"
            python_time = format_time(python_results.get(bench, {}).get("mean_ns", 0)) if bench in python_results else "-"

            lines.append(f"| {bench} | {rust_time} | {cpp_time} | {go_time} | {python_time} |")

        lines.append("")
    else:
        lines.extend([
            "*No benchmark results found. Run `just bench` to generate results.*",
            "",
        ])

    # Detailed sections per language
    if rust_results:
        lines.extend([
            "## Rust (Criterion)",
            "",
            "| Benchmark | Mean Time |",
            "|-----------|-----------|",
        ])
        for name, data in sorted(rust_results.items()):
            lines.append(f"| {name} | {format_time(data['mean_ns'])} |")
        lines.append("")

    if cpp_results:
        lines.extend([
            "## C++ (Google Benchmark)",
            "",
            "| Benchmark | Mean Time |",
            "|-----------|-----------|",
        ])
        for name, data in sorted(cpp_results.items()):
            lines.append(f"| {name} | {format_time(data['mean_ns'])} |")
        lines.append("")

    if go_results:
        lines.extend([
            "## Go (testing.B)",
            "",
            "| Benchmark | Mean Time |",
            "|-----------|-----------|",
        ])
        for name, data in sorted(go_results.items()):
            lines.append(f"| {name} | {format_time(data['mean_ns'])} |")
        lines.append("")

    if python_results:
        lines.extend([
            "## Python (pytest-benchmark)",
            "",
            "| Benchmark | Mean Time |",
            "|-----------|-----------|",
        ])
        for name, data in sorted(python_results.items()):
            lines.append(f"| {name} | {format_time(data['mean_ns'])} |")
        lines.append("")

    # Notes
    lines.extend([
        "## Notes",
        "",
        "- All benchmarks run with release/optimized builds",
        "- Times are mean values across multiple iterations",
        "- Lower is better",
        "- Results may vary based on system load and hardware",
        "",
    ])

    return "\n".join(lines)


def main():
    """Generate and write the benchmark report."""
    root = Path(__file__).parent.parent
    reports_dir = root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Also create raw directory if it doesn't exist
    (reports_dir / "raw").mkdir(parents=True, exist_ok=True)

    report = generate_report(root)

    # Write latest report
    latest_file = reports_dir / "latest.md"
    with open(latest_file, "w") as f:
        f.write(report)

    print(f"Report written to {latest_file}")

    # Optionally archive to history
    history_dir = reports_dir / "history"
    history_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    history_file = history_dir / f"report_{timestamp}.md"
    with open(history_file, "w") as f:
        f.write(report)

    print(f"Archived to {history_file}")


if __name__ == "__main__":
    main()
