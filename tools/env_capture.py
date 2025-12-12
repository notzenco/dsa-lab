#!/usr/bin/env python3
"""
Environment Capture Script for dsa-lab

Captures system and toolchain information for reproducible benchmarks.
"""

import json
import os
import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


def run_command(cmd: list[str]) -> Optional[str]:
    """Run a command and return its output, or None on failure."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    return None


def get_cpu_info() -> Dict[str, Any]:
    """Get CPU information."""
    info = {
        "processor": platform.processor() or "unknown",
        "architecture": platform.machine(),
    }

    # Try to get more detailed info on Linux
    if platform.system() == "Linux":
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if line.startswith("model name"):
                        info["model"] = line.split(":")[1].strip()
                        break
        except (IOError, IndexError):
            pass

        # Get CPU count
        try:
            info["cores"] = os.cpu_count()
        except:
            pass

    return info


def get_memory_info() -> Dict[str, Any]:
    """Get memory information."""
    info = {}

    if platform.system() == "Linux":
        try:
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemTotal"):
                        kb = int(line.split()[1])
                        info["total_gb"] = round(kb / 1024 / 1024, 2)
                        break
        except (IOError, ValueError):
            pass

    return info


def get_rust_info() -> Dict[str, Any]:
    """Get Rust toolchain information."""
    info = {}

    rustc_version = run_command(["rustc", "--version"])
    if rustc_version:
        info["rustc"] = rustc_version

    cargo_version = run_command(["cargo", "--version"])
    if cargo_version:
        info["cargo"] = cargo_version

    return info


def get_cpp_info() -> Dict[str, Any]:
    """Get C++ toolchain information."""
    info = {}

    # Try g++ first
    gpp_version = run_command(["g++", "--version"])
    if gpp_version:
        info["g++"] = gpp_version.split("\n")[0]

    # Try clang++
    clangpp_version = run_command(["clang++", "--version"])
    if clangpp_version:
        info["clang++"] = clangpp_version.split("\n")[0]

    cmake_version = run_command(["cmake", "--version"])
    if cmake_version:
        info["cmake"] = cmake_version.split("\n")[0]

    ninja_version = run_command(["ninja", "--version"])
    if ninja_version:
        info["ninja"] = ninja_version

    return info


def get_go_info() -> Dict[str, Any]:
    """Get Go toolchain information."""
    info = {}

    go_version = run_command(["go", "version"])
    if go_version:
        info["go"] = go_version

    return info


def get_python_info() -> Dict[str, Any]:
    """Get Python information."""
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
    }


def capture_environment() -> Dict[str, Any]:
    """Capture full environment information."""
    return {
        "timestamp": datetime.now().isoformat(),
        "system": {
            "os": platform.system(),
            "os_release": platform.release(),
            "os_version": platform.version(),
            "hostname": platform.node(),
        },
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "toolchains": {
            "rust": get_rust_info(),
            "cpp": get_cpp_info(),
            "go": get_go_info(),
            "python": get_python_info(),
        },
    }


def flatten_env(env: Dict[str, Any], prefix: str = "") -> Dict[str, str]:
    """Flatten nested dict for simple key-value display."""
    flat = {}
    for key, value in env.items():
        full_key = f"{prefix}{key}" if prefix else key
        if isinstance(value, dict):
            flat.update(flatten_env(value, f"{full_key}."))
        else:
            flat[full_key] = str(value)
    return flat


def main():
    """Capture and output environment information."""
    root = Path(__file__).parent.parent
    raw_dir = root / "reports" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    env = capture_environment()

    # Write full JSON
    json_file = raw_dir / "env.json"
    with open(json_file, "w") as f:
        json.dump(env, f, indent=2)

    print(f"Environment captured to {json_file}")
    print()

    # Print summary
    print("=== Environment Summary ===")
    print()

    flat = flatten_env(env)
    for key, value in sorted(flat.items()):
        if key != "timestamp":
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
