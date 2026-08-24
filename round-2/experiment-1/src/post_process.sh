#!/bin/bash
# Post-processing script for experiment results

set -e

echo "Waiting for method_out.json..."
timeout 3000 bash -c 'until [ -f method_out.json ]; do sleep 10; done'

echo "✓ Output file created"

# Validate
echo "Validating output..."
source .venv/bin/activate
python validate_output.py

# Generate CSVs
echo "Generating CSV outputs..."
python generate_csv.py

# Display summary
echo "=== EXPERIMENT SUMMARY ==="
python3 -c "
import json
with open('method_out.json') as f:
    data = json.load(f)
print(f\"Total trials: {data['total_trials']}\")
for sched, stats in data['schedulers'].items():
    print(f\"{sched}: CV={stats['mean_cv']:.3f}±{stats['std_cv']:.3f}, P95={stats['mean_p95_ms']:.1f}±{stats['std_p95_ms']:.1f}ms\")
print(f\"\\nSuccess criteria:\")
for criterion, met in data['success_criteria'].items():
    print(f\"  {'✓' if met else '✗'} {criterion}\")
"

echo "✓ Post-processing complete"
