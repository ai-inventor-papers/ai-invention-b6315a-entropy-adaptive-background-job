#!/usr/bin/env python3
"""Validate and format method_out.json output."""

import json
import sys
from pathlib import Path

def validate_output():
    """Validate the method output against expected schema."""
    output_path = Path("method_out.json")

    if not output_path.exists():
        print(f"ERROR: {output_path} not found")
        return False

    try:
        data = json.loads(output_path.read_text())
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {output_path}: {e}")
        return False

    # Check required top-level keys
    required_keys = {'schedulers', 'comparisons', 'success_criteria', 'total_trials'}
    if not required_keys.issubset(data.keys()):
        print(f"ERROR: Missing keys: {required_keys - data.keys()}")
        return False

    # Check schedulers
    scheduler_names = {'Baseline', 'Entropy-Only', 'Momentum-Only', 'Entropy-Adaptive'}
    if not scheduler_names.issubset(data['schedulers'].keys()):
        print(f"ERROR: Missing schedulers: {scheduler_names - data['schedulers'].keys()}")
        return False

    for sched_name, stats in data['schedulers'].items():
        required_stats = {'n_trials', 'mean_cv', 'std_cv', 'mean_p95_ms', 'std_p95_ms', 'mean_fpr', 'std_fpr'}
        if not required_stats.issubset(stats.keys()):
            print(f"ERROR: {sched_name} missing stats: {required_stats - stats.keys()}")
            return False

    # Check success criteria
    required_criteria = {'cv_reduction_ge_20pct', 'p95_improvement_ge_10pct', 'entropy_outcome_r_gt_0_7',
                         'sample_size_ge_50'}
    if not required_criteria.issubset(data['success_criteria'].keys()):
        print(f"ERROR: Missing success criteria: {required_criteria - data['success_criteria'].keys()}")
        return False

    print("✓ Output validation PASSED")
    return True

if __name__ == "__main__":
    if validate_output():
        sys.exit(0)
    else:
        sys.exit(1)
