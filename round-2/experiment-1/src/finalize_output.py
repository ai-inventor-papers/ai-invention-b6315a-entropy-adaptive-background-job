#!/usr/bin/env python3
"""Finalize output: wait for method_out.json, validate, generate variants."""

import json
import time
import sys
from pathlib import Path

def wait_for_output(timeout_sec=2400, check_interval=10):
    """Wait for method_out.json to be created."""
    start = time.time()
    while time.time() - start < timeout_sec:
        if Path("method_out.json").exists():
            print("✓ method_out.json found")
            return True
        time.sleep(check_interval)
    print("✗ Timeout waiting for method_out.json")
    return False

def validate_output():
    """Validate JSON structure."""
    try:
        data = json.loads(Path("method_out.json").read_text())
        required_keys = {'schedulers', 'comparisons', 'success_criteria', 'total_trials'}
        if not required_keys.issubset(data.keys()):
            print(f"✗ Missing keys: {required_keys - data.keys()}")
            return False
        print("✓ JSON structure valid")
        return True
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        return False

def generate_variants():
    """Generate full/mini/preview variants using aii-json skill."""
    print("Generating full/mini/preview variants...")
    import subprocess
    skill_dir = Path("/ai-inventor/.claude/skills/aii-json")
    script = skill_dir / "scripts" / "aii_json_format_mini_preview.py"

    if script.exists():
        result = subprocess.run(
            [sys.executable, str(script), "--input", "method_out.json"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print(f"Warning: {result.stderr}")
            # Fallback: create minimal variants manually
            return create_minimal_variants()
    return create_minimal_variants()

def create_minimal_variants():
    """Create minimal full/mini/preview if skill unavailable."""
    data = json.loads(Path("method_out.json").read_text())

    # Full is just a copy
    Path("full_method_out.json").write_text(json.dumps(data, indent=2))

    # Mini with reduced data
    mini_data = {**data, "total_trials": min(3, data.get("total_trials", 0))}
    Path("mini_method_out.json").write_text(json.dumps(mini_data, indent=2))

    # Preview with truncated strings
    preview_data = json.loads(json.dumps(data))  # Deep copy
    # Truncate all strings to 200 chars
    def truncate(obj):
        if isinstance(obj, str):
            return obj[:200] + ("..." if len(obj) > 200 else "")
        elif isinstance(obj, dict):
            return {k: truncate(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [truncate(item) for item in obj]
        return obj

    preview_data = truncate(preview_data)
    Path("preview_method_out.json").write_text(json.dumps(preview_data, indent=2))

    print("✓ Generated full_method_out.json")
    print("✓ Generated mini_method_out.json")
    print("✓ Generated preview_method_out.json")
    return True

if __name__ == "__main__":
    if not wait_for_output():
        sys.exit(1)
    if not validate_output():
        sys.exit(1)
    if not generate_variants():
        sys.exit(1)

    print("\n✓ All outputs ready")
    sys.exit(0)
