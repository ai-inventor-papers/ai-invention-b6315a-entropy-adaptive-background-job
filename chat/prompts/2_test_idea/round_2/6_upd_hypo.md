# upd_hypo — test_idea

> Phase: `invention_loop` · round 2 · `upd_hypo`
> Run: `run_a-GYNIuwcKDN` — Entropy-Adaptive Background Job Scheduling for Bursty Workloads
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `upd_hypo` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-24 11:46:24 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A hypothesis reviser (Step 3.6: UPD_HYPO in the invention loop)

You received the current hypothesis, all artifacts, and the paper draft.
Revise the hypothesis based on what the evidence supports.

Honest revision → focused research. Inflated confidence → wasted iteration.
</your_role>
</ai_inventor_context>

You are revising a research hypothesis based on empirical evidence gathered
during an iterative invention loop. Your role is internal reflection — honest
assessment of what the evidence supports.

SCOPE: Your ONLY output is the revised hypothesis text. You do NOT run code,
produce artifacts, fix bugs, or otherwise act on the evidence yourself — the
next iteration of the invention loop will spawn fresh artifacts based on your
revised hypothesis. Reflect on the evidence and rewrite the hypothesis;
nothing else.

PRINCIPLES:
- Ground every revision in specific artifacts and results
- Treat negative and null results as valuable contributions. If the original
  approach failed, the null result IS often the contribution — frame it as
  such (e.g. "X does not improve Y under conditions Z"). Only pivot to a
  different positive claim when the evidence actually supports one; never
  fabricate a positive narrative to mask a failed approach.
- Increase specificity as evidence accumulates
- Don't inflate confidence without strong evidence
- Preserve the core AII prompt unless evidence clearly contradicts it
- Revise hypothesis text only — never attempt to address feedback by running
  code, proposing fixes, or producing artifacts; the next loop iteration
  handles all artifact generation

<current_hypothesis>
The hypothesis as it stands. Revise it based on the evidence below.

kind: hypothesis
title: Entropy-Adaptive Background Job Scheduling
hypothesis: >-
  Background job scheduling improves when thresholds adapt dynamically based on CPU load entropy (unpredictability) rather
  than fixed absolute levels. High entropy (chaotic load) triggers conservative thresholds; low entropy (smooth load) allows
  permissive thresholds. Momentum-aware dispatch prioritizes scheduling when load is decreasing, avoiding spikes. The hypothesis
  requires empirical validation: (1) background job completion time variance reduced by ≥20% vs. fixed-55% threshold, (2)
  foreground p95 latency improved by ≥10%, (3) entropy-outcome correlation r>0.7, (4) superiority confirmed vs. ≥1 alternative
  approach, (5) candidate parameters (60s window, 8 bins, linear formula, α=0.2) validated via sensitivity analysis, (6) success
  measured on both synthetic and real workloads.
motivation: >-
  Current background job schedulers use fixed CPU load thresholds (e.g., 'schedule if CPU < 50%'), which fail under bursty
  workloads where load is unpredictable and volatile. Systems with bursty foreground traffic experience poor background job
  completion times and latency. The insight is that entropy (Shannon entropy of recent CPU load samples) quantifies how unpredictable
  the system is: high entropy means load is bursty and scheduling is risky; low entropy means load is smooth and scheduling
  is safe. By adapting the scheduling threshold to current entropy, and by preferring moments when load momentum is negative
  (decreasing), the scheduler can achieve both responsiveness to foreground traffic AND predictable background job completion.
assumptions:
- >-
  CPU load entropy computed from recent samples (60s windows) provides a reliable signal of near-term predictability.
- >-
  Load momentum (rate of change) is a better scheduling signal than absolute load level for bursty workloads.
- >-
  Background jobs can tolerate adaptive/variable scheduling windows without significant architectural changes.
- >-
  Entropy-based adaptation reduces scheduling latency variance compared to fixed-threshold approaches.
- >-
  Job completion time improves when entropy-driven thresholds replace fixed thresholds in the presence of bursty foreground
  loads.
investigation_approach: >-
  Implement a background job scheduler with three components: (1) Real-time entropy estimator that computes Shannon entropy
  of CPU load samples over a sliding window; (2) Adaptive threshold that scales the scheduling CPU limit based on entropy
  (high entropy → conservative threshold, low entropy → permissive threshold); (3) Momentum-aware dispatcher that, within
  a 'safe' entropy zone, prioritizes scheduling when load gradient is negative. Test on a synthetic workload generator that
  produces bursty foreground load patterns, and measure background job completion time, latency percentiles, and fairness
  versus baseline fixed-threshold scheduler.
success_criteria: >-
  The entropy-adaptive scheduler achieves: (a) 20%+ reduction in background job completion time variance compared to fixed-threshold
  scheduling under bursty loads; (b) 10%+ improvement in p95 foreground latency when background jobs are scheduled with entropy-aware
  thresholds; (c) Statistically significant correlation (r > 0.7) between estimated load entropy and actual scheduling safety
  (measured as foreground latency impact); (d) Confirmation that momentum-based dispatch reduces 'false positives' (scheduling
  at moments when load immediately spikes after apparent trough).
related_works:
- >-
  Mixture-of-Schedulers (2511.11628): Routes to expert scheduling policies based on workload pattern recognition, tested on
  mixed interactive+batch workloads. Differs from this work because it routes based on WORKLOAD TYPE (what's running), not
  load ENTROPY (how predictable the system is), and does not use momentum-based dispatch timing.
- >-
  PREACT (3673038.3673135): Predictive resource allocation for bursty workloads in data centers using QPS prediction and SLO
  profiling. Differs because it targets data center job scheduling (not single-machine background jobs) and uses QPS-based
  prediction rather than load entropy adaptation.
- >-
  DriftSched (2606.02982): Adaptive QoS-aware GPU inference scheduling responding to token generation drift. Differs because
  it targets GPU inference (not CPU background jobs), tracks token-level drift (not load entropy), and operates on a different
  hardware substrate.
- >-
  Load trend analysis papers (CPU load rate of change): Predict future load from trend features for resource provisioning.
  Differs because they use load trends for FORECASTING, not as a real-time scheduling dispatch signal, and do not adapt scheduling
  thresholds.
- >-
  Entropy-based scheduling in RL (2601.19624): Adapts exploration entropy in reinforcement learning based on environmental
  drift. Differs because it is about exploration policy tuning in learning, not CPU load-based job scheduling decisions.
inspiration: >-
  The hypothesis is inspired by three cross-domain sources: (1) Information theory (Shannon entropy as a measure of uncertainty/unpredictability);
  (2) Control systems (momentum/derivative as a control signal for decision timing, borrowed from PID controllers and inertial
  dynamics in physics); (3) Adaptive systems in ecology (niche theory — systems with high ecological entropy/variability warrant
  conservative resource allocation; low entropy warrants aggressive allocation).
terms:
- term: Load entropy
  definition: >-
    Shannon entropy computed from a distribution of recent CPU load samples, quantifying the unpredictability or burstiness
    of the system. High entropy indicates volatile, hard-to-predict load; low entropy indicates smooth, predictable load.
- term: Momentum (or load gradient)
  definition: >-
    The instantaneous rate of change of CPU load, estimated as the first-order time derivative. Negative momentum means CPU
    load is decreasing; positive momentum means it is increasing.
- term: Adaptive threshold
  definition: >-
    A scheduling CPU load limit (e.g., 'schedule if CPU < X%') that varies in real time based on current system entropy, rather
    than being fixed. High entropy → conservative (lower) threshold; low entropy → permissive (higher) threshold.
- term: Bursty workload
  definition: >-
    A workload with high variability in request arrival rate or service time, causing unpredictable spikes in CPU load even
    when mean load is moderate.
- term: Background job
  definition: >-
    A lower-priority task (e.g., garbage collection, index rebuilding, cache warming) that tolerates variable scheduling delays
    and should not degrade foreground response latency.
summary: >-
  Background job schedulers should adapt their CPU load thresholds dynamically based on measured load entropy (unpredictability),
  and dispatch jobs preferentially when load momentum is negative, improving both completion time predictability and foreground
  latency under bursty workloads.
_relation_rationale: >-
  Design refined to emphasize empirical validation scope; core entropy-based scheduling concept unchanged.
_confidence_delta: decreased
_key_changes:
- >-
  Added explicit empirical validation criteria: 20%+ variance reduction, 10%+ p95 latency, r>0.7 correlation, superiority
  vs. ≥1 alternative
- >-
  Clarified candidate design parameters (60s window, 8 bins, linear formula, α=0.2) require sensitivity analysis validation
- >-
  Added requirement for head-to-head comparison against alternative approaches to substantiate novelty
- >-
  Expanded validation scope: both synthetic AND real workloads required, not synthetic-only
- >-
  Softened absolute claims ('improves significantly' → 'improves') to reflect unvalidated status
relation_type: evolution
</current_hypothesis>

<all_artifacts>
Complete set of research artifacts across all iterations.

--- Item 1 ---
id: art_sTVyGK2NrtrJ
type: research
title: 'Entropy-Adaptive Background Job Scheduler: Complete Design Specification'
summary: >-
  This comprehensive research establishes all design parameters needed to implement and evaluate an entropy-adaptive background
  job scheduler. The system monitors CPU load unpredictability (entropy) and load trends (momentum) to dynamically adjust
  scheduling thresholds: in predictable periods, background jobs run freely; during chaotic/bursty periods, they are throttled
  to protect foreground tasks. Key findings: (1) Shannon entropy estimation from CPU load samples over 60-second windows with
  8 bins and Miller-Madow bias correction provides a robust signal; (2) Exponential weighted moving average (EWMA, α=0.2)
  tracks load momentum with 1-5 second window; (3) Linear threshold formula maps entropy [0, log₂(8)] to CPU limits [70%,
  25%], with update every 10-30 seconds; (4) Production baseline is fixed 55% CPU threshold; (5) Success metrics include 20%+
  variance reduction in job completion times, 10%+ p95 latency improvement for foreground tasks, entropy-outcome correlation
  r>0.7, and statistically significant improvement at n≥50 trials. The approach differs from prior work: Mixture-of-Schedulers
  routes based on workload type via ML (entropy-adaptive uses information theory for threshold adaptation); PREACT predicts
  QPS at datacenter scale (entropy-adaptive operates on single machine); DriftSched adapts GPU token budgets (entropy-adaptive
  uses CPU load distribution). This work is novel in combining information-theoretic entropy estimation with momentum-based
  dispatch timing for background job scheduling. Implementation overhead is <1% CPU, making it practical for production deployment.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_a-GYNIuwcKDN/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 2 ---
id: art_aWntWiTqo8og
type: experiment
in_dependencies:
- id: art_sTVyGK2NrtrJ
  label: design specification
title: Entropy-Adaptive Job Scheduler Experiment
summary: >-
  Implements and evaluates an entropy-adaptive background job scheduler that uses Shannon entropy of CPU load to dynamically
  adjust scheduling thresholds, protecting foreground task latency during bursty periods. Compares four scheduler variants
  (Baseline fixed-55%, Entropy-only, Momentum-only, Entropy-Adaptive) on 10 trials of synthetic workloads with Poisson arrivals
  and spike patterns. Measures completion time coefficient of variation (CV), foreground p95 latency, entropy-outcome correlation,
  false positive rate, and statistical significance via paired t-tests and Cohen's d effect sizes. Outputs: method_out.json
  with per-scheduler metrics and paired comparisons; full/mini/preview variants for analysis.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_a-GYNIuwcKDN/3_invention_loop/iter_2/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 3 ---
id: art_y3jAZErQa4Ew
type: evaluation
title: Statistical Analysis & Component Ablation
summary: >-
  Comprehensive evaluation of entropy-adaptive scheduling hypothesis using rigorous statistical methods. Computes primary
  metrics: completion time coefficient of variation (CV) reduction, foreground p95 latency improvement, entropy-outcome correlation,
  and false positive rate. Includes ablation analysis isolating entropy vs momentum contributions with Cohen's d effect sizes,
  sensitivity analysis across 27 parameter configurations (entropy window, bins, momentum α), and hypothesis tests with 95%
  confidence intervals. Results show 23.5% CV reduction (target ≥20%, p<0.001), 11.4% p95 latency improvement (target ≥10%,
  p<0.001), 73.1% false positive rate reduction, and strong parameter stability (score 0.906). Evaluated 4 schedulers (baseline,
  entropy_only, momentum_only, entropy_adaptive) over 40 trials with comprehensive ablation showing both entropy and momentum
  contribute meaningfully to performance gains. Statistical rigor ensures reproducibility and practical significance.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_a-GYNIuwcKDN/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

--- Item 4 ---
id: art_eizvgaZKW-hz
type: research
title: Real-world workload traces for entropy-adaptive scheduler validation
summary: >-
  This research comprehensively identifies, characterizes, and documents access paths for four major production workload trace
  datasets: Azure VM Traces (V1/V2 with 2-2.7M VMs, 30 days, 5-minute granularity), Alibaba Cluster Traces (2017/2018 with
  1.3k-4k machines, 24h-8 days), Google Cluster Traces (2011/2019 from 12.5k-machine Borg cells), and Wikipedia Request Traces.
  The research validates their suitability for testing entropy-adaptive scheduler designs by documenting dataset schemas,
  access methods, and known data quality issues. Critical finding: Real production traces exhibit strong temporal structure
  (diurnal patterns, inter-spike clustering, heavy-tailed burstiness) absent from synthetic Poisson+periodic baselines used
  in scheduler design. Prior research confirms self-similar traffic properties (Hurst exponent > 0.5) and co-location interference
  effects in real workloads. Entropy methodology is standardized (60-second windows, 8 percentile bins, Miller-Madow bias
  correction for small samples) but never applied comparatively to real vs synthetic baselines. The research establishes that
  a critical validation gap exists: no published work quantifies the entropy distribution divergence between production traces
  and synthetic models using identical methodology. This gap is load-bearing for scheduler generalization claims because entropy
  thresholds tuned on synthetic data may not match real workload ranges. Recommendations identify Alibaba 2018 as primary
  dataset (8-day duration, 4k machines, fine-grained metrics, confirmed heavy-tail patterns) with Azure V2 and Google 2011
  as complementary sources. Expected outcome is KS test divergence (p<0.05) with medium-to-large effect sizes (Cohen's d >
  0.5), validating that real workloads require distinct entropy calibration than synthetic models.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_a-GYNIuwcKDN/3_invention_loop/iter_2/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
</all_artifacts>

<new_artifacts_this_iteration>
These 3 artifacts were created THIS iteration.

id: art_aWntWiTqo8og
type: experiment
in_dependencies:
- id: art_sTVyGK2NrtrJ
  label: design specification
title: Entropy-Adaptive Job Scheduler Experiment
summary: >-
  Implements and evaluates an entropy-adaptive background job scheduler that uses Shannon entropy of CPU load to dynamically
  adjust scheduling thresholds, protecting foreground task latency during bursty periods. Compares four scheduler variants
  (Baseline fixed-55%, Entropy-only, Momentum-only, Entropy-Adaptive) on 10 trials of synthetic workloads with Poisson arrivals
  and spike patterns. Measures completion time coefficient of variation (CV), foreground p95 latency, entropy-outcome correlation,
  false positive rate, and statistical significance via paired t-tests and Cohen's d effect sizes. Outputs: method_out.json
  with per-scheduler metrics and paired comparisons; full/mini/preview variants for analysis.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_a-GYNIuwcKDN/3_invention_loop/iter_2/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

id: art_y3jAZErQa4Ew
type: evaluation
title: Statistical Analysis & Component Ablation
summary: >-
  Comprehensive evaluation of entropy-adaptive scheduling hypothesis using rigorous statistical methods. Computes primary
  metrics: completion time coefficient of variation (CV) reduction, foreground p95 latency improvement, entropy-outcome correlation,
  and false positive rate. Includes ablation analysis isolating entropy vs momentum contributions with Cohen's d effect sizes,
  sensitivity analysis across 27 parameter configurations (entropy window, bins, momentum α), and hypothesis tests with 95%
  confidence intervals. Results show 23.5% CV reduction (target ≥20%, p<0.001), 11.4% p95 latency improvement (target ≥10%,
  p<0.001), 73.1% false positive rate reduction, and strong parameter stability (score 0.906). Evaluated 4 schedulers (baseline,
  entropy_only, momentum_only, entropy_adaptive) over 40 trials with comprehensive ablation showing both entropy and momentum
  contribute meaningfully to performance gains. Statistical rigor ensures reproducibility and practical significance.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_a-GYNIuwcKDN/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

id: art_eizvgaZKW-hz
type: research
title: Real-world workload traces for entropy-adaptive scheduler validation
summary: >-
  This research comprehensively identifies, characterizes, and documents access paths for four major production workload trace
  datasets: Azure VM Traces (V1/V2 with 2-2.7M VMs, 30 days, 5-minute granularity), Alibaba Cluster Traces (2017/2018 with
  1.3k-4k machines, 24h-8 days), Google Cluster Traces (2011/2019 from 12.5k-machine Borg cells), and Wikipedia Request Traces.
  The research validates their suitability for testing entropy-adaptive scheduler designs by documenting dataset schemas,
  access methods, and known data quality issues. Critical finding: Real production traces exhibit strong temporal structure
  (diurnal patterns, inter-spike clustering, heavy-tailed burstiness) absent from synthetic Poisson+periodic baselines used
  in scheduler design. Prior research confirms self-similar traffic properties (Hurst exponent > 0.5) and co-location interference
  effects in real workloads. Entropy methodology is standardized (60-second windows, 8 percentile bins, Miller-Madow bias
  correction for small samples) but never applied comparatively to real vs synthetic baselines. The research establishes that
  a critical validation gap exists: no published work quantifies the entropy distribution divergence between production traces
  and synthetic models using identical methodology. This gap is load-bearing for scheduler generalization claims because entropy
  thresholds tuned on synthetic data may not match real workload ranges. Recommendations identify Alibaba 2018 as primary
  dataset (8-day duration, 4k machines, fine-grained metrics, confirmed heavy-tail patterns) with Azure V2 and Google 2011
  as complementary sources. Expected outcome is KS test divergence (p<0.05) with medium-to-large effect sizes (Cohen's d >
  0.5), validating that real workloads require distinct entropy calibration than synthetic models.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_a-GYNIuwcKDN/3_invention_loop/iter_2/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
</new_artifacts_this_iteration>

<current_paper>
The paper draft from this iteration — represents the current state of the research story.

# Entropy-Adaptive Background Job Scheduling for Bursty Workloads

## Introduction

### The Problem: Fixed Thresholds Fail Under Burstiness

Background job schedulers run lower-priority tasks (garbage collection, cache warming, index maintenance, data replication) that must not degrade foreground application latency. Current production systems use fixed CPU load thresholds: schedule background jobs only if CPU utilization is below a static limit, typically 50-60%. This rule is simple and predictable.

However, fixed thresholds have a critical flaw under bursty workloads. Consider a web service with unpredictable request spikes: the CPU might be at 40% for 30 seconds, then spike to 85% within milliseconds. A fixed 55% threshold will schedule background jobs during the calm period, but by the time they acquire CPU time, the foreground load has spiked and background activity now competes directly with user-facing work. The scheduler has no signal that the calm moment is temporary or likely to be disrupted.

This manifests as two coupled failures: background job completion times become highly variable (some finish quickly, others are delayed by minutes when foreground traffic spikes), and foreground latency percentiles (p95, p99) degrade noticeably when background jobs run, even under "safe" CPU levels. Industry evidence documents a consistent 10-20% p95 latency cost during background job execution, even with conservative thresholds.

### Why Prior Approaches Fall Short

**Workload type-based routing** classifies workloads as interactive, batch, or real-time and routes each to a specialist scheduler. This is effective when workload types are stable, but on a single machine running mixed workloads, type classification is expensive and does not directly address load *unpredictability*—two workloads of the same type can have vastly different entropy.

**Datacenter-scale QPS prediction** forecasts aggregate query rates across many machines to provision resources centrally. This approach works at the multi-tenant scale but not on a single machine where local CPU load is the control signal, and adds latency to dispatch decisions due to centralized coordination.

**GPU-specific adaptive scheduling** predicts token generation drift in language model inference and adapts GPU time budgets. This is domain-specific to GPU inference and does not generalize to CPU background jobs with heterogeneous execution times.

**Load trend prediction** uses historical load slopes to forecast near-term load, helping with resource provisioning. However, provision-time forecasting is fundamentally different from *dispatch-time* decision making: a scheduler needs to know now whether to start a background job, not predict load five minutes hence.

The gap is clear: no prior work uses *load entropy* (unpredictability) as a signal for real-time scheduling decisions on a single machine, nor combines entropy adaptation with momentum-based dispatch timing.

### Our Contribution

We propose **entropy-adaptive background job scheduling**, which makes three key innovations:

1. **Information-theoretic signal**: We quantify load unpredictability directly using Shannon entropy over CPU load samples, providing a principled measure of how "bursty" the system currently is. High entropy means the near future is unpredictable (conserve resources); low entropy means load is smooth (schedule freely).

2. **Adaptive thresholds**: Rather than a fixed 55% CPU limit, we dynamically adjust the threshold between 70% (smooth, low-entropy periods) and 25% (chaotic, high-entropy periods) by linearly interpolating based on entropy.

3. **Momentum-aware dispatch**: Within a "safe" entropy zone, we further prioritize scheduling moments when load gradient is negative (decreasing), avoiding the trap of scheduling just before a load spike.

**Empirical validation**: We have implemented and evaluated the complete system on synthetic workloads. Results show 23.5% reduction in background job completion time variance (p<0.001) and 11.4% improvement in p95 foreground latency (p<0.001). Ablation studies confirm both components contribute meaningfully. Sensitivity analysis validates design parameters.

[FIGURE:fig_system_arch]

### Summary of Contributions

- **Empirical demonstration**: First implementation showing entropy-adaptive scheduling achieves 23.5% completion time variance reduction and 11.4% p95 latency improvement over fixed-threshold baselines.

- **Rigorous component analysis**: Ablation studies and sensitivity analysis quantify entropy vs momentum contributions and validate parameter choices across 27 configurations.

- **Differentiation from related work**: Unlike type-based routing (MoS), entropy-adaptive measures system *unpredictability*. Unlike datacenter-scale prediction (PREACT), it operates at single-machine granularity with real-time dispatch. Unlike GPU-specific methods (DriftSched), it uses universally available CPU load.

- **Production-ready design**: Complete specification of entropy estimator, momentum tracker, adaptive threshold formula, and fallback mechanisms with <1% CPU overhead.

- **Roadmap for real-world validation**: Identification of production datasets (Azure, Alibaba, Google) and methodology for entropy distribution validation.

## Related Work

### Adaptive Scheduling

**Mixture-of-Schedulers (MoS)** learns to route workloads to specialist schedulers based on ML classification. It achieves 86.4% superiority on the Aurora benchmark. MoS operates on workload *type* (what is running), not load *entropy* (how unpredictable the system is). Two interactive workloads with the same type can have different entropy; MoS would treat both identically. Additionally, MoS requires training data and per-dispatch inference, whereas entropy-adaptive uses closed-form model-free calculation.

**PREACT** predicts query rate at datacenter scale to pre-allocate resources across machines. It works at the orchestration layer (placement, VM provisioning), whereas entropy-adaptive works at single-machine granularity (per-job CPU throttling). The approaches are complementary.

**DriftSched** adapts GPU inference scheduling to token generation drift. It is domain-specific to GPU inference and tracks signals inaccessible on CPU systems. Entropy-adaptive uses universally available CPU load data.

### Load Prediction and Control

**Workload forecasting** predicts future load to inform resource provisioning. Entropy-adaptive differs by making dispatch-time decisions based on current entropy, not forecasting. Forecasting minimizes provisioning waste; entropy adaptation minimizes dispatch regret.

**Feedback control for scheduling** applies control theory to enforce SLOs. Load momentum is a classical control signal. We adopt momentum for real-time dispatch prioritization, extending prior work focused on deadline enforcement to background job protection during bursty periods.

### Load Characterization

**Burstiness characterization** documents load spike patterns in data centers. This validates the motivation for entropy-based scheduling but proposes no specific dispatch policy.

**Dual-metric analysis** shows burstiness requires metrics beyond mean and variance. Entropy captures temporal structure, making it appropriate for bursty workload analysis.

## Methods: Technical Design

### Entropy Estimator

**Goal**: Quantify CPU load unpredictability.

**Approach**: Compute Shannon entropy H = -Σ p_i log₂(p_i) over recent CPU load samples, where p_i is the fraction of samples in bin i.

**Specification**:
- Sampling: 500ms intervals
- Window: 60 seconds (120 samples)
- Discretization: 8 percentile-based bins
- Bias correction: Miller-Madow (H_corrected = H_plugin + (K-1)/(2N))
- Normalization: Divide by log₂(8) to scale to [0, 1]

**Rationale**: Entropy directly measures unpredictability. Uniform distribution yields H=1.0 (maximum uncertainty); constant load yields H=0.

### Momentum Estimator

**Goal**: Identify load trends for dispatch timing.

**Approach**: EWMA of load gradient.

**Specification**:
- Formula: momentum_t = α × load_t + (1 - α) × momentum_{t-1}
- Update: every 1 second
- Smoothing: α = 0.2 (5-second memory)
- Thresholds: momentum < -5% (declining) or > +10% (spiking)

### Adaptive Thresholds

**Goal**: Map entropy to scheduling CPU limit.

**Formula**:
```
H_norm = H_corrected / log₂(8)
threshold(H_norm) = 70% - 45% × H_norm
```

- H_norm = 0 (smooth): threshold = 70%
- H_norm = 1 (chaotic): threshold = 25%
- H_norm = 0.5 (moderate): threshold = 47.5%

**Decision rule**: Schedule if current_cpu < threshold(H_norm) AND (entropy < 0.6 OR momentum < -5%).

## Experiments

### Setup

**Testbed**: Single Linux machine (8 cores, 32GB RAM).

**Foreground**: Synthetic interactive workload (Poisson arrivals 10-50 req/s, lognormal service time 5-50ms).

**Background**: CPU-bound jobs (matrix multiply, image processing, sorting) of variable size (10s-100s).

**Bursty pattern**: Periodic spikes to 2x load every 60 seconds for 10 seconds.

**Schedulers evaluated**:
1. Baseline (fixed 55%)
2. Entropy-only (entropy thresholds, no momentum)
3. Momentum-only (fixed 55%, momentum dispatch)
4. Entropy-Adaptive (full proposed method)

### Results

#### Primary Metrics

**Completion Time Variance Reduction**

Entropy-adaptive achieves 23.5% reduction in coefficient of variation (CV) of background job completion times (23.49% ± 10.4% confidence interval, p < 0.001), exceeding our ≥20% target. Baseline mean CV = 0.453; entropy-adaptive mean CV = 0.347.

[FIGURE:fig_cv_reduction]

**Foreground P95 Latency Improvement**

Entropy-adaptive achieves 11.4% improvement in p95 latency (11.40% ± 2.6% CI, p < 0.001), exceeding our ≥10% target. Baseline mean p95 = 152.3 ms; entropy-adaptive mean p95 = 134.9 ms.

[FIGURE:fig_p95_improvement]

**False Positive Rate Reduction**

Entropy-adaptive reduces false positive rate (scheduling followed by CPU spike within 5 seconds) by 73.1%. Baseline FPR = 26%; entropy-adaptive FPR = 7%.

[FIGURE:fig_false_positive]

**Statistical Significance**

Evaluation based on n=10 trials per scheduler (40 total trials). Effect sizes show large practical significance: entropy component contributes Cohen's d = -1.69 to CV reduction (very large effect); momentum contributes Cohen's d = -1.13 (large effect). Confidence intervals are non-overlapping between baseline and entropy-adaptive across all metrics.

#### Ablation Analysis

Ablation studies isolate the contribution of entropy versus momentum components:

- Baseline (fixed 55%): CV reduction = 0%, p95 improvement = 0%
- Entropy-only: CV reduction = 18.1%, p95 improvement = 7.1%
- Momentum-only: CV reduction = 11.5%, p95 improvement = 4.0%
- Entropy-Adaptive (full): CV reduction = 23.5%, p95 improvement = 11.4%

Both entropy and momentum make statistically significant contributions. Entropy reduces completion time variance by adapting to burstiness; momentum reduces false positives by avoiding dispatch just before spikes.

[FIGURE:fig_ablation]

#### Sensitivity Analysis

We tested 27 parameter configurations across three dimensions: entropy window size (30s, 60s, 120s), percentile bins (5, 8, 10), and momentum smoothing α (0.1, 0.2, 0.3).

Results show strong parameter stability with score 0.906. The default configuration (60s, 8 bins, α=0.2) achieves near-optimal performance with low variance. The optimal configuration identified (30s, 5 bins, α=0.3) provides marginal improvement (<0.2%) within measurement noise.

[FIGURE:fig_sensitivity]

### Comparison with Alternatives

Entropy-adaptive outperforms entropy-only (18.1% vs 23.5% CV reduction) and momentum-only (11.5% vs 23.5%) by combining both signals, demonstrating the value of each component.

## Discussion

### Strengths

1. **Entropy as scheduling signal**: Despite entropy-outcome correlation not reaching r > 0.7 target (actual r ≈ -0.09), the system achieved target improvements in completion time variance and p95 latency. This indicates entropy IS a useful signal for scheduling decisions, even if the direct correlation is weak. The weak correlation likely reflects that entropy estimates unpredictability over 60-second windows, but dispatch is a point-in-time decision; perfect instantaneous correlation shouldn't be expected.

2. **Component contribution**: Ablation studies validate both entropy (Cohen's d = -1.69) and momentum (Cohen's d = -1.13) contribute substantially to improvements. Their combination is more effective than either alone.

3. **Parameter robustness**: Across 27 parameter configurations, chosen design parameters are near-optimal with high stability score (0.906), increasing confidence in generalization beyond this specific workload.

4. **Practical efficiency**: Implementation overhead is <1% CPU. Negligible cost relative to benefit.

### Limitations

**Entropy-outcome correlation mismatch**: The hypothesis that entropy-outcome correlation would exceed r > 0.7 was not validated (actual r ≈ -0.09). This does not invalidate the overall approach since primary metrics (CV reduction, p95 improvement) were both achieved. The weak correlation likely reflects: (1) entropy is computed from 60-second windows but dispatch is a point-in-time decision; (2) entropy captures global system unpredictability, not per-workload latency sensitivity; (3) other factors beyond entropy influence instantaneous latency.

**Synthetic workloads only**: Evaluation uses controlled synthetic workloads with Poisson arrivals and periodic spikes (every 60s). Real production traffic has multi-scale burstiness (seconds, minutes, hours), diurnal patterns, and complex correlations. Results may not fully generalize to production systems.

**Real workload validation needed**: We have identified and characterized four major production datasets (Azure VM Traces, Alibaba Cluster Traces, Google Cluster Data, Wikipedia Request Traces). Preliminary analysis suggests real workloads exhibit different entropy distributions (expected range 0.4-1.0 bits vs 0.2-0.6 bits for synthetic), potentially requiring parameter re-tuning.

**Entropy cold-start**: During the first 60 seconds of operation, no entropy estimate exists. Recommended fallback: use base threshold (70%) until first window completes, then switch to adaptive mode.

**Work-conservation trade-off**: Entropy-adaptive may strategically leave CPU idle during high-entropy periods to protect foreground SLOs. This trades resource utilization for SLO assurance. Quantifying this trade-off requires production deployment data.

**Scope limitations**: Single-machine focus limits applicability to modern containerized/orchestrated deployments (Kubernetes, cloud functions) where per-machine scheduling is less relevant. Integration with orchestration-level decisions remains future work.

## Conclusion

Fixed-threshold background job scheduling is inadequate for bursty workloads. We have proposed and empirically validated entropy-adaptive scheduling, which measures load unpredictability (Shannon entropy) and load momentum to dynamically adjust CPU scheduling thresholds in real time. Evaluation on synthetic workloads demonstrates achievement of primary targets: 23.5% completion time variance reduction (p<0.001) and 11.4% p95 latency improvement (p<0.001). Ablation studies confirm both entropy and momentum components contribute meaningfully. Sensitivity analysis validates parameter choices.

The next critical step is validation on production workloads. We have identified access paths for Azure, Alibaba, and Google production traces and developed methodology for comparing entropy distributions between synthetic and real workloads. Real-world validation on these datasets will determine whether entropy thresholds tuned on synthetic data require recalibration for production systems.

**Future work**:
- Deploy entropy-adaptive on production systems to validate real-world performance and measure work-conservation trade-offs.
- Compare real workload entropy distributions against synthetic assumptions using Kolmogorov-Smirnov tests.
- Extend to multivariate entropy combining CPU, I/O, and memory signals.
- Integration with container orchestration platforms (Kubernetes, serverless).
- Adaptive parameter tuning per workload type or deployment profile.

## References

[1] B. Gregg, "Linux Load Averages: Solving the Mystery," Aug. 2017.

[2] Linux Kernel Organization, "CFS Scheduler Design," Linux Kernel Documentation.

[3] Z. Zhou et al., "Mixture-of-Schedulers: Adaptive Scheduling Agent as Learned Router," arXiv:2511.11628, 2025.

[4] Y. Liu et al., "DriftSched: Adaptive QoS-Aware Scheduling under Token Drift," arXiv:2606.02982, 2026.

[5] T. Kraska et al., "PREACT: Predictive Resource Allocation for Bursty Workloads," in Proc. ACM SIGMOD, 2018.

[6] S. Wang et al., "Tracking Drift: Entropy Scheduling for Non-Stationary RL," arXiv:2601.19624, 2026.

[7] J. Smith, "Non-linear Analysis of Bursty Workloads using Dual Metrics," Journal of Cloud Computing, 2019.

[8] M. Woodruff et al., "Measuring Burstiness in Data Center Applications," in Proc. USENIX ATC, 2019.

[9] HostMyCode, "Linux Process Priority and CPU Scheduling," 2026.

[10] ScoutAPM, "Restricting Process CPU Usage," blog post.

[11] S. Raschka, "Exponentially Weighted Moving Averages: Theory and Implementation," Towards Data Science, 2020.

[12] S. Nowozin, "Estimating Discrete Entropy, Part 2," 2014.

[13] R Package Developers, "Miller-Madow Entropy Estimator," entropy package documentation.

[14] Wikipedia, "Entropy Estimation."

[15] Wikipedia, "Work-Conserving Scheduler."

[16] Microsoft Azure, "Best Practices for Background Jobs."

[17] RosziGit, "Kubernetes CPU Throttling and CFS Mechanics," blog post.

[18] OneUptime, "Building Latency Percentile SLOs," Jan. 2026.

[19] LoadTester, "p95 vs p99 Latency Explained," blog post.

[20] A. Kaur et al., "A Survey of Workload Forecasting Methods in Cloud Computing," Journal of Cloud Computing, 2023.

[21] J. A. Stankovic, "Feedback Control Real-Time Scheduling," Real-Time Systems, vol. 8, pp. 99-125, 1995.

[22] A. Bodik et al., "Characterizing, Modeling, and Generating Workload Spikes," in Proc. ACM SOCC, 2010.

[23] Microsoft Research, "Azure Public Datasets," GitHub.

[24] Alibaba Open Source, "Open Cluster Trace Program," GitHub.

[25] Google, "Cluster Data Repository," GitHub.

[26] S. Leland et al., "The Changing Nature of Network Traffic," in Proc. ACM SIGCOMM, 1998.

[27] N. Schad et al., "Analyzing Alibaba's Co-located Datacenter Workloads," in Proc. ACM WOSC, 2018.

[28] M. Delorme et al., "Selecting an Effective Entropy Estimator for Short Sequences," Entropy, vol. 23, no. 5, 2021.

[29] Y. Richman et al., "Approximate Entropy and Sample Entropy: A Comprehensive Tutorial," Entropy, vol. 19, no. 6, 2017.

[30] Y. Yu et al., "BurstGPT: A Real-World Workload Dataset to Optimize LLM Serving Systems," arXiv:2401.17644, 2024.

[31] A. Pal et al., "Resource demands in telco data centers," Nature Scientific Data, 2024.

[32] S. Kumar et al., "Attention-based workload prediction and dynamic resource allocation," Nature Scientific Reports, 2026.

</current_paper>

<reviewer_feedback>
Feedback from the paper reviewer this iteration.

- [MAJOR] (evidence) Entropy-outcome correlation reaches only r≈-0.09, failing the stated r>0.7 target by a large margin. This is presented in the Discussion as a limitation that doesn't invalidate the approach because 'primary metrics were achieved.' However, this explanation is insufficient: if entropy doesn't correlate with the outcomes you're trying to optimize (latency), then entropy is not THE signal you claim it is. The weak correlation raises questions: (1) Are the improvements actually driven by entropy, or by the momentum component or the combination effect? (2) Is there a non-linear relationship that linear correlation misses? (3) Is entropy the wrong metric entirely, and the improvements come from 'just being adaptive' rather than adaptive-to-entropy? The ablation shows entropy contributes Cohen's d=-1.69, but this is from comparing entropy-only to baseline—it doesn't show entropy is better than alternative signals (variance, autocorrelation, etc.).
  Action: Investigate entropy-outcome correlation rigorously: (1) Plot scatter of entropy vs latency delta for all samples (n×10 trials); fit polynomial and non-linear models to check if r=-0.09 is an artifact of linear assumption. (2) Test alternative entropy metrics (sample entropy, approximate entropy, multiscale entropy) and report their correlations. (3) Compare entropy correlation to alternative signals: r(load_variance, latency_delta), r(autocorrelation, latency_delta), r(ARIMA_prediction_error, latency_delta). If entropy has the weakest correlation among candidates, acknowledge this and reframe contribution as 'we show entropy + momentum heuristic works empirically even if not theoretically motivated by strong signal correlation.' (4) If none of these improve correlation above r>0.4, consider whether the r>0.7 target was misguided, and propose an alternative theoretical framework (e.g., information-theoretic justification not based on direct latency correlation).
- [MAJOR] (evidence) Evaluation uses only synthetic workloads (Poisson arrivals, lognormal service times, periodic 2x spikes every 60s). Artifact 4 explicitly documents that real production workloads have significantly different entropy distributions (expected 0.4-1.0 bits vs synthetic 0.2-0.6 bits) and temporal structure (multi-scale burstiness, diurnal patterns, inter-spike clustering). The paper acknowledges this gap and defers validation to 'future work,' but this is inadequate for a top-tier venue contribution. Without real workload validation, the 23.5% CV reduction and 11.4% p95 improvement claims are not supported for production systems. Real workloads may have entropy distributions that fall outside the adaptive threshold range [25%, 70%], requiring parameter retuning that artifact 4 predicts ('potentially requiring parameter re-tuning'). This mismatch alone could cause the approach to underperform or fail on real data.
  Action: Run entropy-adaptive on at least one real production trace before resubmission. Artifact 4 identifies Alibaba 2018 as the primary candidate (8-day duration, 4k machines, confirmed heavy-tail patterns). Steps: (1) Extract CPU load time series from Alibaba 2018 for 3-5 representative machines. (2) Run entropy-adaptive and fixed-55% baseline on the same data. (3) Report CV and p95 latency for real traces. (4) Compare entropy distributions (histogram and KS test p-value) between real and synthetic data. If real data entropy is outside [0.2-0.6] or p_KS < 0.05, document the distribution mismatch and discuss whether parameters need retuning. Expected outcome: either (a) 23.5% improvement holds on real data, validating synthetic experiments, or (b) improvement degrades to 10-15%, revealing a critical gap between synthetic and real workloads that must be addressed in next iteration.
- [MAJOR] (novelty) The paper claims novelty over Mixture-of-Schedulers (MoS), PREACT, and DriftSched, but provides no experimental comparison. The Related Work section (Section 2) states MoS 'operates on workload type, not load entropy' and 'requires training and per-dispatch inference,' but then makes no empirical comparison. The claim that entropy-adaptive is superior to these approaches is unsubstantiated. A fair evaluation would: (1) implement MoS classifier on the synthetic workloads (classifying jobs as 'interactive' vs 'batch'), (2) implement PREACT's core idea (CPU load forecasting 5-10 seconds ahead to inform scheduling), (3) run all three adaptive strategies against fixed 55% baseline on identical workloads. Without head-to-head comparison, the paper cannot claim entropy is a better signal than type-based routing or forecasting. The ablation only shows entropy vs momentum vs combined—none of these are published baselines.
  Action: Add experimental comparison of entropy-adaptive against at least two published baselines: (1) Mixture-of-Schedulers: train a simple classifier (decision tree, logistic regression, or random forest) on job features (arrival time, service time, CPU usage) to predict whether the job is 'interactive' or 'batch.' Use this to classify foreground workload type and schedule background jobs conservatively when interactive traffic is detected. Measure CV and p95 on identical synthetic workloads. (2) Momentum-only: use fixed 55% threshold but apply entropy-adaptive's momentum-based dispatch prioritization (only schedule when momentum < -5%). This isolates momentum's contribution vs entropy's contribution. Report results in a table: baseline (fixed 55%), momentum-only, entropy-only, entropy-adaptive. Expected finding: entropy-adaptive beats all others by >10%, supporting the novelty claim. If MoS or momentum-only is competitive, the contribution is weakened—entropy would be one of several useful signals, not a breakthrough.
- [MAJOR] (evidence) Sample size n=10 trials per scheduler is small for systems papers at top venues. Standard practice in scheduling conferences (OSDI, SOSP) expects n≥50-100 trials to establish statistical significance for noisy system metrics like latency percentiles. The previous review (iteration 1) recommended n≥50 or preferably n≥100; the paper now reports n=10. With only 10 trials, 95% confidence intervals are wide (typically ±20-30% of point estimate), and claims of 23.5% ± 10.4% CV reduction are at the edge of detection noise. The paper reports p<0.001, but this should be verified: with n=10 per group and paired t-test, the t-statistic must exceed ~3.25 for p<0.001 (two-tailed, df=9). The effect size Cohen's d=-1.69 is very large and suggests a strong difference, but large effect sizes can appear with small samples due to random variation in endpoint selection.
  Action: Increase sample size to n≥50 trials per scheduler. At 10 minutes per trial, this is ~8.3 hours per scheduler × 4 schedulers = 33 hours total—feasible on a single machine over 1-2 days. Steps: (1) Run n=50 trials for each of the four schedulers (baseline, entropy-only, momentum-only, entropy-adaptive) on identical synthetic workload generator. (2) Report point estimates and 95% CIs for CV and p95 latency for each scheduler. (3) Compute statistical power: for the observed effect size and variance, n=50 achieves what power for detecting a 10% improvement? 15%? 20%? (4) Report p-values and Cohen's d with 95% CIs (not just point estimates). (5) Show convergence: plot point estimates and CI width as a function of n (n=10, 20, 30, 40, 50) to demonstrate that results stabilize. If the effect shrinks as n increases (e.g., 23.5% at n=10, drops to 15% at n=50), this reveals that the small-n result was inflated by chance.
- [MINOR] (methodology) Sensitivity analysis across 27 parameter configurations is mentioned and claims 'stability score 0.906,' but detailed results are not reported in the main paper. The paper only states 'the chosen configuration (60s, 8 bins, α=0.2) achieves near-optimal performance' and 'the optimal configuration identified (30s, 5 bins, α=0.3) provides marginal improvement (<0.2%).' This is opaque: What is the 'stability score'? How many of the 27 configurations beat the chosen baseline? Which dimension (window, bins, α) has the largest impact on CV/p95? Without seeing the heatmap or table, readers cannot assess parameter robustness or judge whether the chosen design is justified.
  Action: Report sensitivity analysis results in full. Create a 3D heatmap or table showing CV reduction and p95 improvement for all 27 configurations (window size × bin count × momentum α). Highlight the chosen configuration (60s, 8 bins, 0.2) and the empirically optimal (30s, 5 bins, 0.3). Define 'stability score' explicitly: is it coefficient of variation across configs, Gini coefficient of performance, or something else? Show which parameter (window, bins, α) is most influential via one-way sensitivity analysis (vary one parameter while holding others fixed). Report effect size (Δ in CV/p95) for each parameter level. Expected outcome: if 60s/8/0.2 is robust and close-to-optimal, the design choice is validated; if a different config is substantially better (e.g., >5% improvement), update the main design to use the empirically better parameters.
- [MINOR] (clarity) Key parameter thresholds are stated without empirical or theoretical justification: (1) momentum threshold -5% (decision rule: 'momentum < -5%') and +10% (mentioned as 'spiking') appear in the decision rule but are never validated by data. Why not -2% or -8%? (2) Entropy safe zone 0.6 mentioned in decision rule ('entropy < 0.6') but never discussed or justified in main text or methods. (3) False positive rate definition is casual: 'scheduling followed by CPU spike within 5 seconds'—what defines a spike? Is it any increase, or only >10% increase, or >1 standard deviation? Why 5 seconds? These vague thresholds reduce methodological rigor.
  Action: Empirically justify threshold parameters: (1) Momentum: plot false positive rate vs momentum threshold (-10%, -5%, -2%, 0%, +2%). Show that -5% minimizes FPR while not sacrificing background job throughput. (2) Entropy safe zone: plot foreground p95 latency degradation vs entropy safe zone threshold (0.3, 0.5, 0.6, 0.8, 1.0). Show that 0.6 minimizes the 'regret' (latency increase relative to baseline). (3) False positive rate: formally define 'spike' as 'current_cpu exceeds threshold(H_norm)' (not just any increase). Justify 5-second window by showing that this is the typical time for background job to acquire meaningful CPU and start degrading foreground latency. Run sensitivity: show FPR for 2s, 5s, 10s windows—is 5s optimal? Include these analyses in the revised paper or appendix.
- [MINOR] (clarity) Missing figures referenced in paper: [FIGURE:fig_system_arch], [FIGURE:fig_cv_reduction], [FIGURE:fig_p95_improvement], [FIGURE:fig_false_positive], [FIGURE:fig_ablation], [FIGURE:fig_sensitivity]. While the instructions state to assume figures show what captions describe, the actual figures are needed for a real submission. Scatter plot of entropy vs latency delta would be particularly important for understanding the weak correlation (r≈-0.09) issue. Without visuals, readers cannot quickly grasp system architecture, results, or parameter sensitivities.
  Action: Create all referenced figures: (1) [FIGURE:fig_system_arch]: block diagram of entropy estimator, momentum tracker, threshold calculator, dispatch logic. (2) [FIGURE:fig_cv_reduction]: bar chart showing baseline vs entropy-adaptive CV (with 95% CIs), possibly separated by entropy regime (low/medium/high). (3) [FIGURE:fig_p95_improvement]: time series plot of p95 latency over the experiment, showing baseline vs entropy-adaptive. (4) [FIGURE:fig_false_positive]: line plot of false positive rate vs entropy threshold or momentum threshold. (5) [FIGURE:fig_ablation]: grouped bar chart showing CV reduction for baseline (0%), entropy-only, momentum-only, entropy-adaptive. (6) [FIGURE:fig_sensitivity]: heatmap of CV reduction across the 27 parameter configurations. (7) Additional scatter plot: entropy vs latency delta for all samples, with r and trend line, to visualize the weak correlation issue.
- [MINOR] (scope) The paper focuses exclusively on single-machine background job scheduling. Modern production systems use container orchestration (Kubernetes, serverless functions, cloud instances) where per-machine scheduling is less relevant and orchestration-level decisions dominate. The paper acknowledges this limitation in the Conclusion ('Single-machine focus limits applicability to modern containerized/orchestrated deployments') but does not propose a path to practical deployment. For a 2025 submission, limiting scope to single-machine scheduling significantly reduces impact—it addresses a problem that is less urgent in the era of Kubernetes.
  Action: Outline a path to practical deployment in modern systems. Discuss: (1) Kubernetes integration: How would entropy-adaptive work in kubelet (per-node entropy computation and signaling to scheduler)? Would it throttle background pods locally or inform pod placement decisions? (2) Serverless platforms: AWS Lambda, Google Cloud Functions often run background cleanup/replication tasks; could entropy-adaptive improve their scheduling? (3) Hybrid approach: Entropy-adaptive could complement orchestration-level decisions (Kubernetes scheduler places pod on node; entropy-adaptive fine-tunes CPU sharing on that node). Provide a minimal design sketch for at least one of these integration points. This broadens the applicability beyond legacy systems and positions entropy-adaptive in the modern infrastructure landscape.
- [MINOR] (evidence) Work-conservation trade-off is acknowledged but not quantified. The paper states 'entropy-adaptive may strategically leave CPU idle during high-entropy periods to protect foreground SLOs' and defers analysis to 'deployment data.' In cloud environments, CPU idling directly increases operating costs (paying for idle resources). The trade-off between SLO protection (latency improvement) and resource efficiency (CPU utilization) is load-bearing for practical deployment decisions, but is left unanalyzed.
  Action: Quantify the work-conservation trade-off: (1) Measure CPU utilization (% of time CPU is idle vs running background jobs) for baseline (fixed 55%) vs entropy-adaptive across all synthetic trials. (2) Model the cost: Cost = (p95_latency - target_latency) × C_latency + (idle_cpu_fraction) × C_energy. Use realistic cloud values (e.g., C_latency = $100 per 1ms p95 SLO violation, C_energy = $0.01 per idle CPU-hour). (3) Compute cost for both schedulers and show whether entropy-adaptive's latency improvement justifies the idle CPU cost. Expected finding: entropy-adaptive may idle 5-10% of CPU to gain 11.4% latency improvement; trade-off is favorable if latency violations are costly. If idling is >20%, discuss strategies to reduce it (e.g., selective idling only during extreme high-entropy periods, or background job prioritization to keep something running while protecting SLOs).
</reviewer_feedback>



<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for the field's landscape, prior work, crowded lanes, and the novelty bar — consult it while revising so the updated hypothesis stays genuinely novel and well-positioned.

- **aii-handbook-auto-computational-linguistics** — Field handbook for computational linguistics as a SCIENCE of language — grammaticality and minimal pairs (BLiMP), surprisal versus reading times, linguistic structure in LMs, annotator disagreement an
- **aii-handbook-auto-mechanistic-interpretability** — Field handbook for mechanistic interpretability of neural networks — circuit discovery, activation and attribution patching, sparse autoencoders, transcoders, attribution graphs, steering vectors, pro
- **aii-handbook-auto-multi-agent-llm-systems** — Field handbook for multi-agent LLM systems (MAS) — orchestration topology, multi-agent debate, mixture-of-agents, verifier and critic agents, inter-agent protocols (MCP/A2A), failure attribution and s
- **aii-handbook-auto-neurosymbolic** — Field handbook for neuro-symbolic AI — text-to-logic autoformalization (NL to FOL), LLM-plus-solver and prover pipelines (Prolog, ASP, SMT), probabilistic-differentiable NeSy (DeepProbLog, Scallop), r
</available_domain_handbooks>

<task>
IMPORTANT: Your ONLY output is the revised hypothesis text. Do NOT run code, produce artifacts,
fix bugs, or attempt to address the evidence yourself — the next iteration of the invention loop
will generate fresh artifacts based on your revised hypothesis. Reflect and rewrite; nothing else.

Do NOT generate a completely new hypothesis. Take the current hypothesis and REVISE it
to incorporate new evidence. Keep the core idea — refine, narrow, or strengthen it.

1. Does the evidence support the hypothesis? Narrow or broaden scope as needed.
2. Which claims now have strong evidence? Which are still unsupported?
3. Should the hypothesis become more specific based on what we've learned?
4. If reviewer feedback is provided, address the critiques directly.

STABILITY IS OK: If progress is good and evidence supports the current direction, keep the
hypothesis similar or identical. Only make substantive changes when evidence clearly calls for
them — e.g., contradictory results, fundamental reviewer critiques, or findings that refine scope.

You must also classify two kinds of edges in the research trace:

(A) The H↔H edge — how does this revised hypothesis relate to the previous one?
    Set `relation_type` (Moulines's structuralist typology) to one of:
    - "evolution": refining specialised claims, same conceptual frame
    - "embedding": previous hypothesis is now a special case of a broader frame
    - "replacement": rejecting the previous frame entirely (Kuhnian shift)
    Set `relation_rationale` to a brief justification (≤120 chars).

(B) The A↔A edges — for each artifact created THIS iteration, classify each of its
    `in_dependencies` (predecessor → dependent) using MultiCite's citation-function
    typology (Lauscher et al., NAACL 2022) — emit one entry in `artifact_relations`
    per (predecessor, dependent) pair. Predecessors are ALWAYS artifacts from EARLIER
    iterations — artifacts within one iteration run in parallel and cannot depend on
    each other, so never emit a relation between two same-iteration artifacts (it
    will be dropped):
    - "background": predecessor is treated as background context
    - "motivation": predecessor motivated this artifact's research
    - "uses": this artifact uses the predecessor's data, method, or output
    - "extends": this artifact extends the predecessor
    - "similarities": this artifact's results agree with the predecessor's
    - "differences": this artifact's results disagree with the predecessor's
    Each `relation_rationale` must be ≤120 characters.

Output the COMPLETE revised hypothesis (with the H↔H relation fields) AND the full
list of A↔A `artifact_relations` for this iteration's new artifacts.
</task><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_a-GYNIuwcKDN/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ArtifactRelation": {
      "description": "One typed A\u2194A edge between a dependent artifact and one of its in_dependencies.\n\nMultiCite citation-function typology (Lauscher et al., NAACL 2022),\nreduced to 6 plain-English types.",
      "properties": {
        "from_id": {
          "description": "ID of the predecessor artifact (the one being depended on)",
          "title": "From Id",
          "type": "string"
        },
        "to_id": {
          "description": "ID of the dependent artifact (the new artifact this iteration)",
          "title": "To Id",
          "type": "string"
        },
        "relation_type": {
          "description": "MultiCite citation-function type for the predecessor\u2192dependent edge: 'background' \u2014 predecessor is treated as background context; 'motivation' \u2014 predecessor motivated this artifact's research; 'uses' \u2014 this artifact uses the predecessor's data, method, or output; 'extends' \u2014 this artifact extends the predecessor; 'similarities' \u2014 this artifact's results agree with the predecessor's; 'differences' \u2014 this artifact's results disagree with the predecessor's.",
          "enum": [
            "background",
            "motivation",
            "uses",
            "extends",
            "similarities",
            "differences"
          ],
          "title": "Relation Type",
          "type": "string"
        },
        "relation_rationale": {
          "description": "Brief rationale for this relation type (one short line, max 120 characters).",
          "maxLength": 120,
          "title": "Relation Rationale",
          "type": "string"
        }
      },
      "required": [
        "from_id",
        "to_id",
        "relation_type",
        "relation_rationale"
      ],
      "title": "ArtifactRelation",
      "type": "object"
    }
  },
  "description": "Revised hypothesis after reviewing iteration results.\n\nOutput matches the hypothesis dict structure so it can replace the\noriginal hypothesis in subsequent iterations.",
  "properties": {
    "title": {
      "description": "Revised hypothesis title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); may be unchanged if still accurate.",
      "title": "Title",
      "type": "string"
    },
    "hypothesis": {
      "description": "Revised hypothesis statement \u2014 what we now believe based on evidence",
      "title": "Hypothesis",
      "type": "string"
    },
    "relation_rationale": {
      "description": "Brief rationale for the H\u2194H revision type (one short line, max 120 characters).",
      "maxLength": 120,
      "title": "Relation Rationale",
      "type": "string"
    },
    "confidence_delta": {
      "description": "How confidence changed: 'increased', 'decreased', or 'unchanged'",
      "title": "Confidence Delta",
      "type": "string"
    },
    "key_changes": {
      "description": "Bullet list of specific changes made to the hypothesis",
      "items": {
        "type": "string"
      },
      "title": "Key Changes",
      "type": "array"
    },
    "relation_type": {
      "description": "Moulines's structuralist typology of this hypothesis revision: 'evolution' \u2014 refining specialised claims while keeping the same conceptual frame; 'embedding' \u2014 the previous hypothesis is now a special case of a broader frame; 'replacement' \u2014 rejecting the previous frame entirely (incommensurable, Kuhnian revolution).",
      "enum": [
        "evolution",
        "embedding",
        "replacement"
      ],
      "title": "Relation Type",
      "type": "string"
    },
    "artifact_relations": {
      "description": "Typed A\u2194A edges for this iteration's new artifacts. Emit one entry per (predecessor \u2192 dependent) edge for every in_dependency on each artifact produced this iteration.",
      "items": {
        "$ref": "#/$defs/ArtifactRelation"
      },
      "title": "Artifact Relations",
      "type": "array"
    }
  },
  "required": [
    "title",
    "hypothesis",
    "relation_rationale",
    "confidence_delta",
    "key_changes",
    "relation_type"
  ],
  "title": "RevisedHypothesis",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-08-24 11:46:24 UTC

```
Find a better heuristic for scheduling background jobs on a machine with bursty CPU load.
```

### [3] SYSTEM-USER prompt · 2026-08-24 11:47:48 UTC

```
<validation-feedback>
Attempt 1 failed validation.

Schema validation found 1 problem — fix ALL of them at once:
  - at `relation_rationale`: 'Same core concept (entropy+momentum adaptive scheduling), but narrowed to synthetic-only validation, acknowledged r>0.7 target failure, and shifted from theoretical optimality to empirical pragmatism.' is too long (at most 120 characters, got 200)
Every required field must be present and every field type must match the schema.

Produce `.terminal_claude_agent_struct_out.json` again so it contains corrected JSON that matches the schema. Do not invent new fields.
</validation-feedback>
```
