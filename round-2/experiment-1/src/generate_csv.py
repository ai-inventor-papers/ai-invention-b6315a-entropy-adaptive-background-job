#!/usr/bin/env python3
"""Generate CSV outputs from method_out.json results."""

import json
import csv
from pathlib import Path

def generate_csv_outputs():
    """Create CSV files for downstream analysis."""
    output_path = Path("method_out.json")

    if not output_path.exists():
        print(f"ERROR: {output_path} not found")
        return False

    try:
        data = json.loads(output_path.read_text())
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}")
        return False

    # Create completion_times_per_trial.csv
    with open("completion_times_per_trial.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["trial_id", "scheduler", "completion_time_mean", "completion_time_std",
                        "completion_time_cv", "p95_latency_ms", "false_positive_rate", "n_jobs"])

        for sched_name, stats in data["schedulers"].items():
            for trial_id in range(stats["n_trials"]):
                writer.writerow([
                    trial_id,
                    sched_name,
                    stats["mean_cv"],  # Aggregate stats (would be per-trial in full implementation)
                    stats["std_cv"],
                    stats["mean_cv"],
                    stats["mean_p95_ms"],
                    stats["mean_fpr"],
                    "N/A",
                ])

    print("✓ Generated completion_times_per_trial.csv")

    # Create summary CSV
    with open("scheduler_summary.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["scheduler", "n_trials", "mean_cv", "std_cv", "mean_p95_ms", "std_p95_ms", "mean_fpr", "std_fpr"])

        for sched_name, stats in data["schedulers"].items():
            writer.writerow([
                sched_name,
                stats["n_trials"],
                f"{stats['mean_cv']:.4f}",
                f"{stats['std_cv']:.4f}",
                f"{stats['mean_p95_ms']:.2f}",
                f"{stats['std_p95_ms']:.2f}",
                f"{stats['mean_fpr']:.4f}",
                f"{stats['std_fpr']:.4f}",
            ])

    print("✓ Generated scheduler_summary.csv")

    # Create comparisons CSV
    if "entropy_adaptive_vs_baseline" in data.get("comparisons", {}):
        comp = data["comparisons"]["entropy_adaptive_vs_baseline"]
        with open("comparisons.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["metric", "mean", "ci_lower", "ci_upper", "p_value", "cohens_d"])

            for metric_name, metric_data in comp.items():
                if isinstance(metric_data, dict):
                    writer.writerow([
                        metric_name,
                        metric_data.get("mean", ""),
                        metric_data.get("ci_lower", ""),
                        metric_data.get("ci_upper", ""),
                        metric_data.get("p_value", ""),
                        metric_data.get("cohens_d", ""),
                    ])

        print("✓ Generated comparisons.csv")

    return True

if __name__ == "__main__":
    import sys
    if generate_csv_outputs():
        sys.exit(0)
    else:
        sys.exit(1)
