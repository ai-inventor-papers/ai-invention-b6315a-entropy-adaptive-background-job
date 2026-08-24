# gen_full_paper — report_results

> Phase: `gen_paper_repo` · `gen_full_paper`
> Run: `run_a-GYNIuwcKDN` — Entropy-Adaptive Background Job Scheduling for Bursty Workloads
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_full_paper` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-24 12:02:52 UTC

````
<research_methodology>
Write like an experienced academic. Reviewers judge both the science and the writing.

- Claims must be proportional to evidence. Choose verbs carefully — "demonstrate," "observe," and "hypothesize" mean different things.
- Every result needs: what was measured, on what data, the numbers, and what they mean.
- Methodology must be specific enough to reproduce. Related work must be organized by theme, not a literature dump.
- State limitations honestly. Avoid both overclaiming and excessive hedging.
</research_methodology>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_a-GYNIuwcKDN/4_gen_paper_repo/_4_assemble_paper/paper/workspace`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_a-GYNIuwcKDN/4_gen_paper_repo/_4_assemble_paper/paper/workspace/`:
GOOD: `/ai-inventor/aii_data/runs/run_a-GYNIuwcKDN/4_gen_paper_repo/_4_assemble_paper/paper/workspace/file.py`, `/ai-inventor/aii_data/runs/run_a-GYNIuwcKDN/4_gen_paper_repo/_4_assemble_paper/paper/workspace/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>

<task>
Create a publication-ready top-conference LaTeX paper with BibTeX from <paper_text> and <available_figures>, compile to PDF.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<paper_text>
title: Entropy-Adaptive Background Job Scheduling for Bursty Workloads
abstract: >-
  Background job scheduling on machines with bursty foreground workloads presents a fundamental tension: rigid CPU thresholds
  protect foreground latency but degrade background job throughput, while permissive scheduling improves throughput at the
  cost of foreground SLO violations. This paper proposes entropy-adaptive scheduling, which adapts CPU thresholds dynamically
  based on measured load unpredictability rather than absolute load level. By quantifying system burstiness using Shannon
  entropy of CPU load samples and timing dispatch decisions to avoid load spikes using load momentum, we enable schedulers
  to be conservative during unpredictable periods and permissive during smooth periods. Empirical evaluation on synthetic
  workloads with controlled burstiness demonstrates a 23.5% reduction in background job completion time variance (target:
  ≥20%, p<0.001), an 11.4% improvement in p95 foreground latency (target: ≥10%, p<0.001), and a 73.1% reduction in false positive
  scheduling decisions. Ablation studies confirm that both entropy and momentum components contribute significantly to these
  gains (Cohen's d > 1.1 for both). Implementation overhead is negligible (<1% CPU), making deployment practical in production
  systems. We identify directions for real-world validation using production traces from Azure, Alibaba, and Google datacenters.
paper_text: |
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
summary: >-
  This paper presents entropy-adaptive background job scheduling, which dynamically adjusts CPU scheduling thresholds based
  on measured load unpredictability (Shannon entropy) and load momentum. Empirical evaluation on synthetic bursty workloads
  demonstrates: (1) 23.5% reduction in background job completion time variance vs fixed-55% baseline (p<0.001), exceeding
  the ≥20% target; (2) 11.4% improvement in foreground p95 latency (p<0.001), exceeding the ≥10% target; (3) 73.1% reduction
  in false positive scheduling decisions; (4) Ablation studies confirm both entropy (Cohen's d=-1.69) and momentum (Cohen's
  d=-1.13) components contribute significantly; (5) Sensitivity analysis across 27 parameter configurations validates that
  chosen parameters (60s window, 8 bins, α=0.2) are near-optimal with high stability (score=0.906). The work addresses a fundamental
  limitation of fixed-threshold scheduling under bursty loads by grounding dispatch decisions in load unpredictability rather
  than absolute load level. While entropy-outcome correlation did not reach the r>0.7 target (actual r≈-0.09), the achievement
  of primary performance metrics indicates entropy remains a useful scheduling signal. Future work includes real-world validation
  on production traces (Azure, Alibaba, Google) and integration with container orchestration platforms.
</paper_text>

<available_figures>
--- Item 1 ---
id: fig_system_arch
figure_type: concept
title: System Architecture Overview
caption: >-
  End-to-end entropy-adaptive scheduling pipeline: CPU load samples feed into entropy estimator (60-second window, 8 percentile
  bins, Miller-Madow correction) to produce normalized entropy H_norm ∈ [0,1]. In parallel, load momentum tracker uses EWMA
  (α=0.2) to estimate load gradient. Adaptive threshold calculator maps H_norm to scheduling CPU limit (70%-45%×H_norm), and
  dispatch logic makes scheduling decisions based on current CPU utilization, entropy threshold, and momentum signal.
image_gen_detailed_description: >-
  Horizontal flow diagram, left to right. Components: (1) CPU Load Samples box (gray) with /proc/stat input arrow, (2) Entropy
  Estimator box (blue) showing '60s window, 8 bins, Miller-Madow', (3) Normalized Entropy arrow to [0,1] scale, (4) Momentum
  Tracker box (green) showing 'EWMA α=0.2', (5) Adaptive Threshold Calculator (orange) with formula '70%-45%×H_norm', (6)
  Dispatch Logic (red) showing decision rule with three inputs (CPU, threshold, entropy, momentum), (7) Output: Schedule vs
  Hold decision. All boxes connected with arrows showing data flow. Use sans-serif font, light background, white boxes with
  colored borders matching box colors. Include small annotations (units, ranges) on data flows.
aspect_ratio: '21:9'
summary: >-
  Architecture showing entropy estimation, momentum tracking, threshold adaptation, and dispatch logic.
figure_path: figures/fig_system_arch_v0.jpg

--- Item 2 ---
id: fig_cv_reduction
figure_type: data
title: Completion Time Variance Reduction
caption: >-
  Coefficient of variation (CV) of background job completion times across four scheduler variants. Baseline (fixed 55%) serves
  as reference (CV = 0.453). Entropy-only reduces CV to 0.371 (18.1% reduction). Momentum-only reduces CV to 0.401 (11.5%
  reduction). Entropy-Adaptive (full proposed method) reduces CV to 0.347 (23.5% reduction, p<0.001). Error bars show 95%
  confidence intervals. The target threshold of ≥20% reduction is marked with a horizontal dashed line.
image_gen_detailed_description: >-
  Bar chart showing CV reduction. X-axis: Scheduler (Baseline, Entropy-only, Momentum-only, Entropy-Adaptive). Y-axis: CV
  value, range 0.30-0.50. Values and CIs: Baseline 0.453 ±0.020, Entropy-only 0.371 ±0.035, Momentum-only 0.401 ±0.028, Entropy-Adaptive
  0.347 ±0.032. Gray bars for Baseline, blue for Entropy-only, green for Momentum-only, red for Entropy-Adaptive. Error bars
  show CI width. Horizontal dashed line at 0.362 (20% reduction from baseline). Y-axis label 'Completion Time CV', X-axis
  label 'Scheduler'. Legend in corner. Title above.
aspect_ratio: '16:9'
summary: Shows 23.5% CV reduction for entropy-adaptive vs baseline, exceeding 20% target.
figure_path: figures/fig_cv_reduction_v0.pdf

--- Item 3 ---
id: fig_p95_improvement
figure_type: data
title: Foreground P95 Latency Improvement
caption: >-
  95th percentile (p95) latency of foreground interactive tasks (milliseconds) across four scheduler variants. Baseline (fixed
  55%) has mean p95 = 152.3 ms. Entropy-only reduces p95 to 141.5 ms (7.1% improvement). Momentum-only reduces p95 to 146.2
  ms (4.0% improvement). Entropy-Adaptive reduces p95 to 134.9 ms (11.4% improvement, p<0.001). Error bars show 95% confidence
  intervals. The target threshold of ≥10% improvement is marked with a horizontal dashed line.
image_gen_detailed_description: >-
  Bar chart showing p95 latency. X-axis: Scheduler (Baseline, Entropy-only, Momentum-only, Entropy-Adaptive). Y-axis: P95
  Latency (ms), range 120-165. Values and CIs: Baseline 152.3 ±3.2, Entropy-only 141.5 ±2.8, Momentum-only 146.2 ±3.1, Entropy-Adaptive
  134.9 ±2.4. Gray bars for Baseline, blue for Entropy-only, green for Momentum-only, red for Entropy-Adaptive. Error bars
  show CI width. Horizontal dashed line at 137.1 (10% improvement from baseline). Y-axis label 'P95 Latency (ms)', X-axis
  label 'Scheduler'. Legend in corner.
aspect_ratio: '16:9'
summary: >-
  Shows 11.4% p95 latency improvement for entropy-adaptive vs baseline, exceeding 10% target.
figure_path: figures/fig_p95_improvement_v0.pdf

--- Item 4 ---
id: fig_ablation
figure_type: data
title: 'Ablation Study: Component Contributions'
caption: >-
  Ablation analysis showing the contribution of entropy and momentum components. Left panel: CV reduction (%). Right panel:
  P95 latency improvement (%). Baseline = 0% (reference). Entropy-only = 18.1% CV / 7.1% p95. Momentum-only = 11.5% CV / 4.0%
  p95. Entropy-Adaptive (full) = 23.5% CV / 11.4% p95. Effect sizes: Entropy Cohen's d = -1.69 (very large). Momentum Cohen's
  d = -1.13 (large). Both components make statistically significant contributions, and their interaction yields superadditive
  improvement (23.5% > 18.1% + 11.5% would be if purely additive).
image_gen_detailed_description: >-
  Two-panel side-by-side bar chart. Left panel: CV Reduction (%). Right panel: P95 Improvement (%). X-axis for both: Baseline,
  Entropy-only, Momentum-only, Entropy-Adaptive. Left panel Y-axis: CV Reduction (%), range 0-30. Right panel Y-axis: P95
  Improvement (%), range 0-15. Left values: Baseline 0, Entropy-only 18.1, Momentum-only 11.5, Entropy-Adaptive 23.5. Right
  values: Baseline 0, Entropy-only 7.1, Momentum-only 4.0, Entropy-Adaptive 11.4. Gray for Baseline, blue for Entropy-only,
  green for Momentum-only, red for Entropy-Adaptive (consistent across both panels). Title above panels: 'Ablation Analysis'.
  Legend showing component colors.
aspect_ratio: '16:9'
summary: >-
  Ablation showing entropy (d=-1.69) and momentum (d=-1.13) both contribute to improvements.
figure_path: figures/fig_ablation_v0.pdf

--- Item 5 ---
id: fig_sensitivity
figure_type: data
title: Parameter Sensitivity Analysis
caption: >-
  Sensitivity analysis across 27 parameter configurations: entropy window (30s, 60s, 120s), percentile bins (5, 8, 10), momentum
  α (0.1, 0.2, 0.3). Heatmap shows mean CV achieved across configurations. Default configuration (60s, 8 bins, α=0.2) highlighted
  with black border, achieves CV=0.347. Optimal configuration (30s, 5 bins, α=0.3) shown in corner, achieves CV=0.346 (marginal
  0.16% improvement within measurement noise). Parameter stability score = 0.906 indicates robustness. Color scale: lighter
  = higher CV (worse), darker = lower CV (better).
image_gen_detailed_description: >-
  3D heatmap rendered as grid of small cells. X-axis: α values (0.1, 0.2, 0.3), 3 columns. Y-axis: window size (30s, 60s,
  120s), 3 rows. Z-axis (color intensity): mean CV across bin counts 5/8/10. Color scale from light (CV=0.35) to dark (CV=0.40).
  Cell at window=60s, α=0.2 has black border (default config, CV=0.347). Cell at window=30s, α=0.3 labeled as optimal (CV=0.346).
  Cells annotated with rounded CV values. Title: 'Parameter Sensitivity (Entropy Window vs Momentum α, mean across bin counts)'.
  Colorbar on right showing CV scale 0.34-0.41.
aspect_ratio: '16:9'
summary: >-
  Parameter stability score 0.906; chosen parameters near-optimal with low variance.
figure_path: figures/fig_sensitivity_v0.pdf

--- Item 6 ---
id: fig_false_positive
figure_type: data
title: False Positive Rate Reduction
caption: >-
  False positive rate (FPR) — scheduling decisions followed by CPU spike >15% within 5 seconds. Baseline (fixed 55%) has FPR
  = 26.0%. Entropy-only reduces FPR to 21.5% (17.3% reduction). Momentum-only reduces FPR to 11.5% (55.8% reduction). Entropy-Adaptive
  reduces FPR to 7.0% (73.1% reduction). Entropy-adaptive's superior performance shows momentum component effectively avoids
  dispatch decisions that precede load spikes. Lower FPR correlates with fewer background jobs being disrupted by unexpected
  foreground load increases.
image_gen_detailed_description: >-
  Bar chart showing false positive rate. X-axis: Scheduler (Baseline, Entropy-only, Momentum-only, Entropy-Adaptive). Y-axis:
  False Positive Rate (%), range 0-30. Values: Baseline 26.0, Entropy-only 21.5, Momentum-only 11.5, Entropy-Adaptive 7.0.
  Gray for Baseline, blue for Entropy-only, green for Momentum-only, red for Entropy-Adaptive. No error bars (single-value
  metrics). Y-axis label 'FPR (%)', X-axis label 'Scheduler'. Title above: 'False Positive Rate'. Annotation showing 73.1%
  reduction from Baseline to Entropy-Adaptive.
aspect_ratio: '16:9'
summary: >-
  Entropy-adaptive reduces FPR by 73.1%, showing momentum effectively avoids pre-spike dispatch.
figure_path: figures/fig_false_positive_v0.pdf
</available_figures>

<figure_requirements>
CRITICAL: Include ALL figures from <available_figures>. No exceptions.

- Every figure MUST use \includegraphics{figures/<the filename from its own `figure_path` above>} — INCLUDING the extension it actually has. Data figures are delivered as `.pdf` (vector, so their axis labels stay sharp) and concept figures as `.jpg`. Writing `.jpg` for a `.pdf` figure names a file that is not in figures/ and the build fails on it
- Do NOT skip, convert to tables, or describe without inserting
- Each needs: \begin{figure}[placement], \includegraphics, \caption, \label, \end{figure} — one placement for every figure, see FLOAT PLACEMENT below. Constrain every \includegraphics with `width=\linewidth,height=0.85\textheight,keepaspectratio`. The height is a LAST RESORT, not the usual limit: it exists so a very tall figure cannot overrun the page, and at 0.4 it bound almost everything instead — a 1:1 confusion matrix printed at 50.9% and its 11 pt axis labels reached the page at 5.6 pt, below what any venue accepts. At 0.85 every ratio the paper prompt prescribes (21:9, 16:9, 4:3, 1:1) is limited by WIDTH, prints at 93% and keeps its text above 10 pt. Use exactly these option keys — `max height=` is NOT valid LaTeX
- Use the `caption` field from each figure for \caption{...} — do NOT invent new captions
- Place figures where their [FIGURE:fig_id] markers appear in paper_text
- VERIFICATION: paper.tex MUST have exact same number of \includegraphics as <available_figures>
- Do NOT generate new figure images (no matplotlib, no PIL, no image generation). Use ONLY the pre-generated figures from <available_figures>. They were already created by a previous pipeline step.

FLOAT PLACEMENT: every figure gets \begin{figure}[!htbp]. Measured, not chosen:
the document the aii-paper-to-latex skill sets up is ONE column, so `figure*` is
exactly as wide as `figure` (469.76pt either way) and gains nothing; and any
placement asking for a page TOP — `[!t]`, `[!tbp]` — floated the hero diagram above
the paper's own title on page 1, while `[!htbp]` did not. `[!htbp]` also gives LaTeX
four options, so a float can never be deferred to the end of the document, which one
option alone risks. Where the hero ENDS UP is decided by its [FIGURE:] marker in
paper_text, which is already placed near the end of the Introduction — preserve it.
</figure_requirements>

<artifact_links>
The paper_text contains \footnote{Code: \url{...}} references linking to artifact source code
on GitHub. Include \usepackage{hyperref} and \usepackage{url}.
Preserve these exactly as-is — do not remove, rewrite, or convert them to plain text.
The URLs will not resolve yet (the repo is deployed after compilation) — do NOT try to verify or fix them.
</artifact_links>

<headings>
NEVER use inline math (``$...$``) inside ``\section{...}`` / ``\subsection{...}`` / ``\subsubsection{...}`` arguments — hyperref's bookmark builder errors out (``Token not allowed in a PDF string``) and the PDF outline breaks. If a section heading needs a math-looking term, use the text equivalent (``d star`` not ``$d^*$``, ``alpha-equivalent`` not ``$\alpha$-equivalent``) or wrap it in ``\texorpdfstring{$math$}{plain}``. Inline math inside body paragraphs is fine.
</headings>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-to-latex, aii-semscholar-bib.
TODO 2. Review <paper_text> and <available_figures>. Copy all figure images into ./figures/ in your workspace. Count figures — MUST include every one. Plan placements per section. Build `./references.bib` via aii_semscholar_bib__fetch — collect DOIs/ArXiv IDs from <paper_text> and batch-fetch all BibTeX in one call. Do NOT fabricate entries.
TODO 3. Create `./paper.tex` per aii-paper-to-latex skill's setup, write ALL sections, insert ALL figures from <available_figures>, include `./references.bib` via \bibliography. Compile to PDF per skill's process. Fix errors.
TODO 4. CRITICAL VERIFICATION: Run `grep -c 'includegraphics' paper.tex`, confirm count equals figures in <available_figures>. If not, add missing figures. Verify `./paper.pdf` was created.
TODO 5. VISUAL REVIEW: Write Python script to convert EVERY page of paper.pdf to PNG at 150 DPI (use pdf2image or pymupdf). Then read ALL page screenshots — each page image costs ~1,600 tokens so a 15-page paper is only ~24K tokens. You MUST read every page. The ONLY exception is if all page images would not fit in your remaining context — in that case, read as many as fit and state which pages you are skipping and why. Check every page for layout issues, overlapping figures, cut-off text, bad spacing, formatting problems. Fix issues and recompile.
TODO 6. FINAL READ: Check page count (`pdfinfo paper.pdf` or pymupdf). Read entire paper.pdf — check for missing sections, unclear explanations, inconsistencies, typos. Fix and recompile. The ONLY exception is if all pages would not fit in your remaining context — in that case, read as many pages as fit and state which pages you are skipping and why.
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "FullPaperExpectedFiles": {
      "description": "All expected output files from full paper generation.",
      "properties": {
        "paper_tex_path": {
          "description": "Path to LaTeX source file. Example: 'paper.tex'",
          "title": "Paper Tex Path",
          "type": "string"
        },
        "paper_pdf_path": {
          "description": "Path to compiled PDF. Example: 'paper.pdf'",
          "title": "Paper Pdf Path",
          "type": "string"
        },
        "references_bib_path": {
          "description": "Path to BibTeX bibliography file. Example: 'references.bib'",
          "title": "References Bib Path",
          "type": "string"
        },
        "figure_paths": {
          "description": "Paths to all figure image files. Example: ['figures/fig1_v0.jpg', 'figures/fig2_v0.jpg']",
          "items": {
            "type": "string"
          },
          "title": "Figure Paths",
          "type": "array"
        }
      },
      "required": [
        "paper_tex_path",
        "paper_pdf_path",
        "references_bib_path",
        "figure_paths"
      ],
      "title": "FullPaperExpectedFiles",
      "type": "object"
    }
  },
  "description": "Full paper \u2014 structured output from paper generation.",
  "properties": {
    "title": {
      "description": "Paper title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance. Aim for about 4-8 words (~40 characters).",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "description": "Brief summary of the generated paper: sections written, figures included, compilation status",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/FullPaperExpectedFiles",
      "description": "All output files you created. Must include paper.tex, paper.pdf, references.bib, and paths to all figure files."
    }
  },
  "required": [
    "title",
    "summary",
    "out_expected_files"
  ],
  "title": "FullPaper",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-08-24 12:02:52 UTC

```
Find a better heuristic for scheduling background jobs on a machine with bursty CPU load.
```

### [3] SKILL-INPUT — aii-paper-to-latex · 2026-08-24 12:03:00 UTC

The agent loaded the **aii-paper-to-latex** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-paper-to-latex
description: "Assembles and compiles a LaTeX paper into paper.pdf: documentclass and package preamble, figure floats that includegraphics pre-generated vector .pdf and .jpg files, float-placement and width rules, and the required pdflatex, bibtex, pdflatex, pdflatex run sequence. Use whenever pre-written text and pre-generated figures must become a compiled PDF, and whenever a build misbehaves — citations printing as question marks, figures drifting to the end or above the title, shrunken axis labels, undefined references. Triggers: latex, tex, pdflatex, bibtex, natbib, includegraphics, figure float, htbp, compile or build the paper, paper.tex, paper.pdf. NOT for: writing the paper's text or deciding its structure (use aii-paper-writing), creating the figure images (aii-data-fig-gen, aii-concept-fig-gen), or fetching bibliography entries (use aii-semscholar-bib); NOT for reshaping a PDF that already exists — merging, splitting, form filling, table extraction (use anthropic-pdf)."
---

## LaTeX Paper Assembly

Assembles a research paper from paper text, pre-generated figures (vector `.pdf` for data figures, `.jpg` for concept figures) and a bibliography into a compiled PDF.

### Document Setup

```latex
\documentclass[11pt,letterpaper]{article}
\usepackage{graphicx, geometry, amsmath, hyperref, natbib, booktabs, xcolor, listings}
\geometry{margin=1in}
\hypersetup{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=black}
```

### Figure Inclusion

CRITICAL: Include ALL figures. Every figure MUST appear in the paper.

```latex
\begin{figure}[!htbp]
  \centering
  \includegraphics[width=0.92\textwidth,keepaspectratio]{figures/filename.pdf}
  \caption{Descriptive caption.}
  \label{fig:label}
\end{figure}
```

Rules:
- ALWAYS `[!htbp]` — all four options, so a float can never be deferred to the end of the
  document, which `[t]` or `[h]` alone risks. Do not ask for a page TOP: `[!t]` and
  `[!tbp]` both floated a figure ABOVE the paper's own title on page 1, where `[!htbp]`
  on the same document did not. Where a figure lands is decided by where it is declared
  in the text
- Use `figure`, never `figure*`. This document class is ONE column, so `figure*` is exactly
  as wide as `figure` (469.76pt either way) and gains nothing, while restricting the float
  to a page top
- ALWAYS constrain with `width` and `keepaspectratio`. Add `height` only as a
  LAST RESORT against a very tall figure overrunning the page, and keep it
  generous — `0.85\textheight`. A tight height cap binds on ordinary figures
  and LaTeX then shrinks the TEXT with them: at `0.4\textheight` a square
  figure printed at 50.9%, putting 11 pt axis labels on the page at 5.6 pt.
  The figure generator measures legibility at the figure's OWN size, so it
  cannot see this happen
- Every figure needs `\caption`, `\label`, and a `\ref` in the text
- Do NOT convert figures to tables or describe them without inserting the image
- Do NOT skip any figures

### Compilation Process

Run each command separately (do NOT chain with `&&` — pdflatex often exits non-zero on warnings, which would skip bibtex and leave citations as `??`):

```bash
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
```

All four commands are required. Skipping bibtex causes `??` in all citations.
Fix any errors between runs. Verify `./paper.pdf` was created.

### Output Files

- `./paper.tex` — LaTeX source
- `./references.bib` — bibliography file
- `./paper.pdf` — compiled PDF
- `./figures/` — all figure images (pre-generated, copied into workspace). Data
  figures are `.pdf` (vector — LaTeX renders their text at page resolution, which
  is what keeps axis labels sharp in print); concept figures are `.jpg`. Use each
  file's OWN extension in `\includegraphics`; there is no conversion step.
````

### [4] SKILL-INPUT — aii-semscholar-bib · 2026-08-24 12:03:02 UTC

The agent loaded the **aii-semscholar-bib** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-semscholar-bib
description: "Fetches real BibTeX entries in one batch from Semantic Scholar by DOI, ArXiv ID or title via aii_semscholar_bib__fetch, normalises citation keys to AuthorYYYY, injects DOIs, and writes the result into references.bib, with a mandatory web-search fallback for anything not found. ALWAYS use whenever a bibliography, reference list or .bib file is being built or extended, and whenever a citation needs a verified entry instead of an invented one — never hand-write BibTeX first. Triggers: bibliography, references.bib, bibtex, citation key, DOI, arXiv id, Semantic Scholar, reference list, cite these papers, natbib entries. NOT for: writing the text around the citations (use aii-paper-writing), running bibtex and compiling (use aii-paper-to-latex), judging whether cited work supports the claims (use amg-paper-verification), or open-ended literature search and PDF mining (use aii-web-tools)."
---

## Tool: `aii_semscholar_bib__fetch`

Batch-fetch BibTeX entries from Semantic Scholar. Pass all references in a single call — the tool handles batching internally.

### How it works

1. **DOI/ArXiv refs** → batched into POST /paper/batch calls (up to 500 per API call, auto-chunked)
2. **Title-only refs** → individual GET /paper/search/match (1s delay between)
3. **Post-process** → fix entry type, fix citation key (AuthorYYYY), inject DOI

The ability server runs a single worker (`max_threads: 1`). Multiple concurrent tool calls are queued — each runs independently (no cross-request aggregation). Batching happens within each request.

### Input format

```json
{
  "references": [
    {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
    {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
    {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
  ]
}
```

Each reference object can have:
- `doi` — DOI string (ArXiv DOIs like `10.48550/arXiv.XXXX.XXXXX` auto-convert to ArXiv IDs)
- `arxiv` — ArXiv ID (e.g. `"2305.14325"`)
- `title` — Paper title (used for search/match when no DOI/ArXiv)
- `author` — First author last name (for cleaner citation key)
- `year` — Publication year (int, for citation key)

At least one of `doi`, `arxiv`, or `title` is required per reference.

### Output format

```json
{
  "success": true,
  "bib_text": "@inproceedings{Vaswani2017, ...}\n\n@article{Wei2022, ...}",
  "total": 3,
  "found": 3,
  "failed_count": 0,
  "entries": [{"citation_key": "Vaswani2017", "bibtex": "...", "title": "...", "doi": "...", "arxiv": ""}],
  "failed": []
}
```

### Workflow

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Call `aii_semscholar_bib__fetch` with the full list in **one call**
3. Save `bib_text` from the response to your `references.bib` file
4. Check `failed` — for any missed papers, follow the **fallback procedure** below

### Fallback for failed references (MANDATORY)

NEVER fabricate BibTeX. For each failed reference:
1. **WebSearch** for `"Title" author year` (try `site:arxiv.org` too)
2. **WebFetch** the paper page → extract title, authors, year, venue, DOI/ArXiv ID
3. If DOI/ArXiv found → retry `aii_semscholar_bib__fetch` with it
4. Last resort: write BibTeX by hand using **only verified info from the actual paper page**

---

### CLI (for manual use / debugging)

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-semscholar-bib" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_semscholar_bib__fetch.py --refs '[
  {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
  {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
  {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
]'
```

`--json, -j` — output raw JSON instead of .bib text

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````
