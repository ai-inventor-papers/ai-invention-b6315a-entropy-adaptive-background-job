# gen_plan_research_1 — test_idea

> Phase: `invention_loop` · round 1 · `gen_plan`
> Run: `run_a-GYNIuwcKDN` — Entropy-Adaptive Background Job Scheduling for Bursty Workloads
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_plan_research_1` (terminal_claude_agent, claude-haiku-4-5)

### [1] CONFIG · 2026-08-24 10:51:28 UTC

```
model: claude-haiku-4-5 | effort: low | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_a-GYNIuwcKDN/3_invention_loop/iter_1/gen_plan/gen_plan_research_1
```

### [2] SYSTEM-USER prompt · 2026-08-24 10:51:36 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A plan generator (Step 3.2: GEN_PLAN in the invention loop)

You received the hypothesis, an artifact direction to elaborate, and dependency artifacts relevant to the plan.
Your job: elaborate this direction into a detailed, actionable plan for the executor agent.

Specific, actionable plan → valuable artifact. Vague plan → wasted execution.
</your_role>
</ai_inventor_context>

<artifact_type_info>
You are expanding an artifact direction of type: RESEARCH

RESEARCH
Web research to answer key questions — like a researcher making decisions.
Runtime: LLM Agent, no code execution.
Tools: the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text).
Capabilities: Find, synthesize, and compare information across sources; survey SOTA and best practices.
Deps: REQUIRED none | OPTIONAL other RESEARCH to build on prior findings
</artifact_type_info>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **SPEND BUDGET**: at most $10 USD of OpenRouter API calls for this artifact. Nothing outside your own code enforces this — the key you are given has no per-artifact cap — so it holds only if you track cumulative cost after every call and stop when you approach it. Budget the work up front: estimate the per-call cost and the number of calls BEFORE starting a sweep, not after it overruns. Exceeding it spends real money that the run cannot recover.
</software_constraints>
</available_resources>

<time_budget>

The research executor has 3h total (including writing code, debugging, testing, and fixing errors).

</time_budget>

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape. Two modes: general (default, broad web) and scholarly (peer-reviewed papers + citations) — pass mode=scholarly for prior-art, related-work, and citation lookups.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<plan_guidelines>
You are expanding an artifact direction from the strategy into a detailed plan.
The artifact direction specifies what to do at a high level (type, objective, approach, dependencies).
Your job is to make it concrete and actionable as a detailed plan.
Use web research to look up technical details, verify feasibility, and find reference materials
that will make your plan more concrete and actionable for the executor.

GOOD PLANS:
- Make each component SPECIFIC and actionable (not vague platitudes)
- Consider both success AND failure scenarios
- Build on the approach in the artifact direction
- Add concrete details the executor needs

BAD PLANS:
- Vague hand-waving ("do research on X")
- Ignoring the approach in the artifact direction
- Missing critical details the executor needs
</plan_guidelines>

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

<hypothesis>
kind: hypothesis
title: Entropy-Adaptive Background Job Scheduling
hypothesis: >-
  Background job scheduling performance improves significantly when the scheduling threshold adapts dynamically based on measured
  CPU load entropy (unpredictability), and dispatch decisions prioritize negative load momentum (decreasing trend) over absolute
  load level.
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
</hypothesis>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for the methods, proper baselines, and evaluation this field demands.

- **aii-handbook-auto-computational-linguistics** — Field handbook for computational linguistics as a SCIENCE of language — grammaticality and minimal pairs (BLiMP), surprisal versus reading times, linguistic structure in LMs, annotator disagreement an
- **aii-handbook-auto-mechanistic-interpretability** — Field handbook for mechanistic interpretability of neural networks — circuit discovery, activation and attribution patching, sparse autoencoders, transcoders, attribution graphs, steering vectors, pro
- **aii-handbook-auto-multi-agent-llm-systems** — Field handbook for multi-agent LLM systems (MAS) — orchestration topology, multi-agent debate, mixture-of-agents, verifier and critic agents, inter-agent protocols (MCP/A2A), failure attribution and s
- **aii-handbook-auto-neurosymbolic** — Field handbook for neuro-symbolic AI — text-to-logic autoformalization (NL to FOL), LLM-plus-solver and prover pipelines (Prolog, ASP, SMT), probabilistic-differentiable NeSy (DeepProbLog, Scallop), r
</available_domain_handbooks>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: research_iter1_dir1
type: research
objective: >-
  Establish design parameters for the entropy-adaptive scheduler through literature review and metric specification
approach: >-
  Survey peer-reviewed work in adaptive CPU schedulers, entropy-based resource allocation, load prediction, and momentum-based
  timing. Design the Shannon entropy estimator (specify window duration, discretization strategy for CPU load, data source).
  Design the load momentum estimator (derivative estimation method, smoothing). Specify the adaptive threshold formula mapping
  entropy → scheduling CPU limit (e.g., high entropy = conservative limit, low entropy = permissive limit). Define success
  metrics precisely: completion time variance reduction %, p95 latency delta %, entropy-safety correlation coefficient r,
  false positive rate (scheduling when load spikes immediately after apparent trough). Specify fixed-threshold baseline scheduler
  design (what threshold value to use for comparison). Document design rationale and parameter choices.
depends_on: []
</artifact_direction>



<instructions>
YOUR ROLE: Write a detailed PLAN for the artifact. A separate executor agent runs the actual artifact later.

You are a PLANNER, not an executor. Your output is a plan that tells the executor what to do and how.
Do NOT execute the artifact itself — a separate agent handles that. Your job is to plan it so well that the executor can follow your plan step by step.

You CAN and SHOULD: search the web, read papers, and explore library docs to make your plan concrete.
You CANNOT run shell commands or scripts — code execution is disabled. Research via web tools only.

Do NOT do the executor's job: don't download datasets, don't implement code, don't run experiments, don't write proofs, don't compute evaluations.

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

RESEARCH executor scope:
  Output: research_out.json with {answer, sources, follow_up_questions} + research_report.md
  DOES: Web research — search, read, synthesize information from papers/docs/APIs into a structured report
  DOES NOT: Run code, download files, execute scripts, compute anything — no shell/Python access
  Use for literature surveys, API documentation, technical specifications — pure information gathering
</artifact_executor_scope>

<artifact_planning_rules>
RESEARCH: Plan early — findings guide dataset selection, experiment design, and methodology.
</artifact_planning_rules>

<compute_profiles>
Choose the compute profile this artifact needs for execution.
Available profiles for research artifacts:
  - cpu_light: 4 vCPUs, 16GB RAM — proofs, research, lightweight tasks (fallback: memory-optimized CPUs first (cpu3m → cpu5m), then GPU hosts last-ditch)

Set runpod_compute_profile to one of these exact tier names.
</compute_profiles>
GOOD PLANS: specific, actionable, consider failure scenarios, build on the suggested approach.
BAD PLANS: vague hand-waving, ignoring the suggested approach, missing critical executor details.
</instructions><user_data>
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
  "description": "Plan for a RESEARCH artifact.",
  "properties": {
    "title": {
      "description": "Plan title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters).",
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Brief summary",
      "title": "Summary",
      "type": "string"
    },
    "runpod_compute_profile": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": "cpu_light",
      "description": "Compute tier for execution \u2014 pick from the available profiles list (e.g., 'gpu', 'cpu_heavy', 'cpu_light'). Only used in RunPod mode.",
      "title": "Runpod Compute Profile"
    },
    "question": {
      "default": "",
      "description": "The specific research question to investigate",
      "title": "Question",
      "type": "string"
    },
    "research_plan": {
      "description": "Step-by-step plan for web research to gather this research",
      "title": "Research Plan",
      "type": "string"
    },
    "explanation": {
      "description": "Why this research matters and what question it answers",
      "title": "Explanation",
      "type": "string"
    }
  },
  "required": [
    "title",
    "research_plan",
    "explanation"
  ],
  "title": "ResearchPlan",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-08-24 10:51:36 UTC

```
Find a better heuristic for scheduling background jobs on a machine with bursty CPU load.
```

### [4] ASSISTANT · 2026-08-24 10:51:49 UTC

```
I'll develop a detailed research plan for the entropy-adaptive background job scheduler investigation. Let me start by searching for relevant literature and concrete design parameters.
```

### [5] TOOL CALL — Skill · 2026-08-24 10:51:49 UTC

```
aii-web-tools
```

### [6] TOOL RESULT — Skill · 2026-08-24 10:51:49 UTC

```
{"success": true, "commandName": "aii-web-tools"}
```

### [7] TOOL CALL — Skill · 2026-08-24 10:51:49 UTC

```
aii-web-tools
```

### [8] TOOL RESULT — Skill · 2026-08-24 10:51:49 UTC

```
{"success": true, "commandName": "aii-web-tools"}
```

### [9] TOOL CALL — Skill · 2026-08-24 10:51:49 UTC

```
aii-web-tools
```

### [10] TOOL RESULT — Skill · 2026-08-24 10:51:49 UTC

```
{"success": true, "commandName": "aii-web-tools"}
```

### [11] ASSISTANT · 2026-08-24 10:51:59 UTC

```
Let me search for more specific information on load monitoring and background scheduling approaches:
```

### [12] TOOL CALL — Skill · 2026-08-24 10:51:59 UTC

```
aii-web-tools
```

### [13] TOOL RESULT — Skill · 2026-08-24 10:51:59 UTC

```
{"success": true, "commandName": "aii-web-tools"}
```

### [14] SYSTEM-USER prompt · 2026-08-24 10:51:59 UTC

```
(Re-invocation of /aii-web-tools — the skill instructions were previously loaded; the arguments or dynamic output below are new.)
```

### [15] TOOL CALL — Skill · 2026-08-24 10:51:59 UTC

```
aii-web-tools
```

### [16] TOOL RESULT — Skill · 2026-08-24 10:51:59 UTC

```
{"success": true, "commandName": "aii-web-tools"}
```

### [17] TOOL CALL — Skill · 2026-08-24 10:51:59 UTC

```
aii-web-tools
```

### [18] TOOL RESULT — Skill · 2026-08-24 10:51:59 UTC

```
{"success": true, "commandName": "aii-web-tools"}
```

### [19] ASSISTANT · 2026-08-24 10:52:45 UTC

```
Based on the hypothesis and artifact direction, I'll now create a comprehensive research plan for the entropy-adaptive scheduler design. Let me write the detailed plan to guide the executor:
```

### [20] TOOL CALL — Write · 2026-08-24 10:52:45 UTC

````
File: /tmp/claude-0/-ai-inventor-aii-data-runs-run-a-GYNIuwcKDN-3-invention-loop-iter-1-gen-plan-gen-plan-research-1/scratchpad/research_plan.md

# Research Plan: Entropy-Adaptive Background Job Scheduling

## Overview
This research establishes concrete design parameters for an entropy-adaptive background job scheduler that improves performance under bursty CPU loads by adapting scheduling thresholds to measured load entropy and prioritizing negative load momentum.

---

## Phase 1: Adaptive Scheduling & Entropy-Based Approaches Literature Survey

**Objective:** Identify how existing systems adapt scheduling decisions and whether entropy or information-theoretic measures have been applied to CPU scheduling.

**Research Questions:**
1. How do modern OS schedulers (Linux CFS, BFQ, Windows scheduler) currently adapt to workload characteristics?
2. What adaptive scheduling techniques exist in data center and cloud scheduling literature?
3. Have information-theoretic concepts (Shannon entropy, mutual information) been applied to resource allocation?
4. What does the literature say about entropy as a predictability signal?

**Key Search Topics:**
- "Adaptive CPU scheduler" + workload classification
- "Entropy resource allocation" + "scheduling" + "prediction"
- "Load prediction scheduling" + "bursty workloads"
- "Mixture of experts scheduling" (the 2511.11628 paper mentioned in hypothesis)
- "Predictive scheduling" + "data center" + "QoS"
- "Load forecasting" + "kernel scheduler"

**Success Indicators:**
- Identify ≥3 papers on adaptive scheduling approaches and their mechanisms
- Find evidence of entropy/information-theoretic approaches in resource allocation
- Document how existing systems measure "load predictability"
- Identify gaps between fixed-threshold and adaptive approaches

---

## Phase 2: Load Monitoring & Entropy Estimation Design

**Objective:** Specify concrete parameters for the Shannon entropy estimator: window size, load sampling rate, discretization strategy, and data source.

**Research Questions:**
1. How is CPU load typically measured and sampled in monitoring systems? (1-sec, 5-sec, 60-sec intervals?)
2. What load averaging algorithms are standard? (Linux load average, EWMA, others?)
3. What are typical window sizes for load-based decisions? (10s, 60s, 300s?)
4. How should CPU load be discretized for entropy calculation? (Percentile buckets? Fixed ranges?)
5. What entropy estimation methods handle short windows with limited samples?
6. How much variance exists in load entropy measurements over 60s windows?

**Key Search Topics:**
- "Linux load average" calculation and history
- "CPU load monitoring" + "sampling frequency" + "monitoring systems"
- "Entropy estimation" + "limited samples" + "bias correction"
- "Load distribution" analysis in web servers / data centers
- "Burstiness metric" + "workload characterization"
- "Window size" + "load prediction" + "resource scheduling"

**Concrete Design Decisions Needed:**
- Window duration: Candidate values from literature (e.g., 10s, 30s, 60s, 120s)
- Sampling frequency: How often to sample load (e.g., every 100ms, 1s, 5s)
- Discretization: Number of entropy bins (e.g., 5-10 bins for 0-100% load range)
- Data source: proc/stat, /proc/loadavg, or custom instrumentation?
- Entropy formula: Standard Shannon entropy H = -Σ p_i * log(p_i)
- Bias correction: Plugin estimator, Miller-Madow, or Linsker?

**Success Indicators:**
- Identify standard load monitoring practices
- Find papers on entropy estimation with finite samples
- Specify window size based on OS load averaging practices
- Document discretization approach with justification

---

## Phase 3: Load Momentum / Trend Analysis

**Objective:** Specify concrete method for computing load gradient/momentum and smoothing strategy.

**Research Questions:**
1. How do existing systems compute load trends? (Simple difference? Polynomial fit? EWMA?)
2. What smoothing techniques reduce noise in load gradient estimates?
3. How much lag/delay is acceptable in momentum estimation?
4. How are load trends used in existing resource allocation decisions?
5. What is typical load derivative magnitude for bursty workloads?

**Key Search Topics:**
- "Load trend" + "prediction" + "forecasting"
- "First-order derivative" + "noisy signals" + "CPU load"
- "Rate of change" + "resource scheduling"
- "EWMA" + "trend smoothing"
- "Savitzky-Golay filter" + "load" (if smoothing discussion exists)
- "PID controller" + "resource allocation" (for inspiration from control systems)
- "Momentum" + "scheduling" in RL / control literature

**Concrete Design Decisions Needed:**
- Momentum window: How far back to look (e.g., last 2-5 load samples)
- Derivative method: Simple difference, linear regression over window, or EWMA?
- Smoothing: Alpha parameter for EWMA or window size for regression?
- Negative momentum threshold: What counts as "decreasing trend"? (e.g., >1% decrease?)
- Detection delay: How recent must momentum be to be useful?

**Success Indicators:**
- Specify derivative estimation method with noise tolerance analysis
- Document typical load gradient magnitudes for bursty workloads
- Identify smoothing parameter ranges from literature
- Define threshold for "negative momentum" scheduling opportunity

---

## Phase 4: Adaptive Threshold Formula

**Objective:** Design the specific mathematical function mapping entropy → scheduling CPU limit.

**Research Questions:**
1. What functional forms are used for adaptive thresholding in other domains? (Sigmoid? Linear? Logarithmic?)
2. How do scheduling thresholds vary in practice? (What range: 30%-80%?)
3. What is the relationship between load entropy and scheduling risk tolerance?
4. How aggressive should the adaptation be? (Large swings vs. conservative changes?)

**Key Search Topics:**
- "Adaptive threshold" + "resource allocation"
- "Control system" + "setpoint adaptation"
- "Scheduling threshold" + "QoS"
- "Risk-aware scheduling"
- "Entropy vs. safety" tradeoffs

**Concrete Design Decisions Needed:**
- Base threshold: Fixed CPU load limit when entropy is 0 (e.g., 50%)
- Max threshold: CPU limit when entropy is maximal (e.g., 25%)
- Functional form: Linear interpolation? Sigmoid? Exponential decay?
- Entropy range normalization: Min entropy 0, max entropy log₂(bins)?
- Formula example: threshold(e) = base - (base - min) * (e / e_max)
- Adaptation speed: How quickly to update threshold on entropy changes?

**Success Indicators:**
- Specify parametric formula with clear interpretation
- Identify parameter ranges from scheduling literature
- Document relationship assumptions between entropy and scheduling safety

---

## Phase 5: Baseline Scheduler Specification

**Objective:** Define the fixed-threshold scheduler that serves as comparison baseline.

**Research Questions:**
1. What is a standard fixed CPU threshold for background jobs? (50%? 70%? 80%?)
2. How do production systems currently make schedule-vs-don't-schedule decisions?
3. What background job scheduling strategies exist in real systems? (Nice levels? Cgroups? Custom?)

**Key Search Topics:**
- "Background job scheduling" + "Linux" + "nice level"
- "CPU cgroup" + "background tasks"
- "Batch scheduling" + "CPU threshold"
- "Low-priority tasks" + "scheduling"

**Concrete Design Decisions Needed:**
- Baseline threshold value: Most common choice in literature (e.g., 50-60%?)
- Decision rule: "Schedule if CPU < threshold" or include other factors?
- Job priority mechanism: Nice level adjustment? IO class? Cgroup limits?
- No momentum component in baseline (pure threshold-based)

**Success Indicators:**
- Identify standard threshold choices in production systems
- Document baseline scheduling strategy used in comparison
- Ensure baseline is fair/representative for comparison

---

## Phase 6: Success Metrics Definition

**Objective:** Specify precise definitions and measurement methods for all four success criteria.

**Research Questions:**
1. How is "completion time variance" measured in scheduling papers? (Coefficient of variation? Std dev?)
2. How do papers measure "latency impact" on foreground traffic? (Percentile latencies? Slowdown factors?)
3. How is correlation computed between entropy and scheduling outcomes? (Pearson? Spearman?)
4. How to quantify "false positives"? (Scheduling events followed by immediate load spike?)

**Key Search Topics:**
- "Variance reduction" measurement in scheduling papers
- "Percentile latency" + "SLO" + "measurement"
- "Completion time distribution" + "scheduling"
- "Fairness metrics" + "scheduling"
- "False positive rate" + "prediction" + "resource management"

**Concrete Design Decisions Needed:**
- Completion time variance: Use coefficient of variation (σ/μ) or relative standard deviation?
- Foreground latency: Measure p50, p95, p99? Which matters most?
- Entropy-safety correlation: Measure correlation between {entropy sample, outcome} pairs over window?
- False positive definition: Schedule at t, then load jumps >10% in next 5 seconds?
- Statistical significance: Minimum sample size, confidence intervals, hypothesis tests?

**Success Indicators:**
- Define all four metrics with clear mathematical formulas
- Specify measurement procedures and aggregation methods
- Identify appropriate statistical tests for significance
- Document success criterion thresholds (20%, 10%, r>0.7, false-positive rate)

---

## Phase 7: Related Work & Novelty Analysis

**Objective:** Verify positioning relative to related work and identify genuine novelty gaps.

**Research Questions:**
1. Do papers on Mixture-of-Schedulers (2511.11628) discuss entropy or load entropy-based routing?
2. Does PREACT (3673038.3673135) use entropy-based adaptation? What exactly does it use?
3. Do load trend papers (cited in hypothesis) combine trend + entropy? Or just trend?
4. Has entropy been combined with momentum-based dispatch timing before?

**Key Search Topics:**
- Fetch and review the hypothesis-cited papers:
  - 2511.11628 (Mixture-of-Schedulers)
  - 3673038.3673135 (PREACT)
  - 2606.02982 (DriftSched)
  - 2601.19624 (RL entropy scheduling)
- "Entropy" + "scheduling" cross-check in recent papers
- "Momentum dispatch" + "scheduling"
- "Bursty workload" + "adaptive" + review top results

**Concrete Design Decisions Needed:**
- Confirm novelty claim: Entropy-driven thresholds are NOT used in cited work
- Confirm momentum component: Dispatch timing based on negative momentum is novel approach
- Document exact differentiation from each related work
- Identify whether combination of entropy + momentum is the core novelty

**Success Indicators:**
- Retrieve and summarize key findings from 4 cited papers
- Confirm entropy-based threshold adaptation is genuinely novel
- Confirm momentum-based dispatch is genuinely novel contribution
- Document positioning summary for executor to include

---

## Research Output Structure

The executor should produce `research_out.json` with:

```json
{
  "answer": {
    "entropy_estimator_design": {
      "window_duration_seconds": <number>,
      "sampling_frequency_hz": <number>,
      "discretization_bins": <number>,
      "bin_ranges": <array>,
      "data_source": "<string>",
      "entropy_formula": "<string>",
      "bias_correction_method": "<string>",
      "rationale": "<string>"
    },
    "momentum_estimator_design": {
      "window_size_samples": <number>,
      "derivative_method": "<string>",
      "smoothing_method": "<string>",
      "smoothing_parameter": <number>,
      "negative_momentum_threshold": "<string>",
      "rationale": "<string>"
    },
    "adaptive_threshold_formula": {
      "functional_form": "<string>",
      "parameters": {
        "base_threshold_percent": <number>,
        "min_threshold_percent": <number>,
        "max_entropy_normalized": <number>
      },
      "formula": "<mathematical string>",
      "interpretation": "<string>",
      "rationale": "<string>"
    },
    "baseline_scheduler": {
      "threshold_percent": <number>,
      "decision_rule": "<string>",
      "job_priority_mechanism": "<string>",
      "rationale": "<string>"
    },
    "success_metrics": {
      "completion_time_variance": {
        "definition": "<string>",
        "formula": "<string>",
        "target_reduction_percent": <number>
      },
      "foreground_latency_p95": {
        "definition": "<string>",
        "target_improvement_percent": <number>
      },
      "entropy_safety_correlation": {
        "definition": "<string>",
        "method": "<string>",
        "target_r": <number>
      },
      "false_positive_rate": {
        "definition": "<string>",
        "measurement_window_seconds": <number>,
        "spike_threshold_percent": <number>
      }
    },
    "novelty_summary": {
      "entropy_based_adaptation": "<whether this component is novel>",
      "momentum_dispatch": "<whether this component is novel>",
      "differentiation_from_related_work": "<string>"
    }
  },
  "sources": [
    "<list of papers/sources consulted>"
  ],
  "follow_up_questions": [
    "<questions for next iteration if needed>"
  ]
}
```

---

## Research Implementation Notes

1. **Search Strategy:** Start with broad searches on adaptive scheduling, then progressively narrow to entropy and momentum specifically.

2. **Paper Retrieval:** For high-value papers (especially the 4 cited in hypothesis), fetch and grep for specific details on:
   - How they adapt scheduling decisions
   - What signals they use (entropy? load trend? QPS?)
   - What success metrics they report

3. **Synthesis:** For each design component, synthesize findings from multiple sources to build consensus on parameter ranges.

4. **Fallback:** If a specific technique has no literature, the executor should document the assumption and design choice rationale.

5. **Validation:** Ensure all formulas and parameters are internally consistent (e.g., entropy normalization matches bin count).

6. **Timeline:** Approximately 1-2 hours of focused web research should suffice, organized as:
   - 20 min: Adaptive scheduling landscape
   - 15 min: Entropy estimation specifics
   - 15 min: Load momentum methods
   - 15 min: Threshold formula design
   - 10 min: Baseline scheduler
   - 15 min: Success metrics detail
   - 10 min: Related work verification
   - 10 min: Synthesis and JSON generation
````

### [21] TOOL RESULT — Write · 2026-08-24 10:52:45 UTC

````
{"type": "create", "filePath": "/tmp/claude-0/-ai-inventor-aii-data-runs-run-a-GYNIuwcKDN-3-invention-loop-iter-1-gen-plan-gen-plan-research-1/scratchpad/research_plan.md", "content": "# Research Plan: Entropy-Adaptive Background Job Scheduling\n\n## Overview\nThis research establishes concrete design parameters for an entropy-adaptive background job scheduler that improves performance under bursty CPU loads by adapting scheduling thresholds to measured load entropy and prioritizing negative load momentum.\n\n---\n\n## Phase 1: Adaptive Scheduling & Entropy-Based Approaches Literature Survey\n\n**Objective:** Identify how existing systems adapt scheduling decisions and whether entropy or information-theoretic measures have been applied to CPU scheduling.\n\n**Research Questions:**\n1. How do modern OS schedulers (Linux CFS, BFQ, Windows scheduler) currently adapt to workload characteristics?\n2. What adaptive scheduling techniques exist in data center and cloud scheduling literature?\n3. Have information-theoretic concepts (Shannon entropy, mutual information) been applied to resource allocation?\n4. What does the literature say about entropy as a predictability signal?\n\n**Key Search Topics:**\n- \"Adaptive CPU scheduler\" + workload classification\n- \"Entropy resource allocation\" + \"scheduling\" + \"prediction\"\n- \"Load prediction scheduling\" + \"bursty workloads\"\n- \"Mixture of experts scheduling\" (the 2511.11628 paper mentioned in hypothesis)\n- \"Predictive scheduling\" + \"data center\" + \"QoS\"\n- \"Load forecasting\" + \"kernel scheduler\"\n\n**Success Indicators:**\n- Identify ≥3 papers on adaptive scheduling approaches and their mechanisms\n- Find evidence of entropy/information-theoretic approaches in resource allocation\n- Document how existing systems measure \"load predictability\"\n- Identify gaps between fixed-threshold and adaptive approaches\n\n---\n\n## Phase 2: Load Monitoring & Entropy Estimation Design\n\n**Objective:** Specify concrete parameters for the Shannon entropy estimator: window size, load sampling rate, discretization strategy, and data source.\n\n**Research Questions:**\n1. How is CPU load typically measured and sampled in monitoring systems? (1-sec, 5-sec, 60-sec intervals?)\n2. What load averaging algorithms are standard? (Linux load average, EWMA, others?)\n3. What are typical window sizes for load-based decisions? (10s, 60s, 300s?)\n4. How should CPU load be discretized for entropy calculation? (Percentile buckets? Fixed ranges?)\n5. What entropy estimation methods handle short windows with limited samples?\n6. How much variance exists in load entropy measurements over 60s windows?\n\n**Key Search Topics:**\n- \"Linux load average\" calculation and history\n- \"CPU load monitoring\" + \"sampling frequency\" + \"monitoring systems\"\n- \"Entropy estimation\" + \"limited samples\" + \"bias correction\"\n- \"Load distribution\" analysis in web servers / data centers\n- \"Burstiness metric\" + \"workload characterization\"\n- \"Window size\" + \"load prediction\" + \"resource scheduling\"\n\n**Concrete Design Decisions Needed:**\n- Window duration: Candidate values from literature (e.g., 10s, 30s, 60s, 120s)\n- Sampling frequency: How often to sample load (e.g., every 100ms, 1s, 5s)\n- Discretization: Number of entropy bins (e.g., 5-10 bins for 0-100% load range)\n- Data source: proc/stat, /proc/loadavg, or custom instrumentation?\n- Entropy formula: Standard Shannon entropy H = -Σ p_i * log(p_i)\n- Bias correction: Plugin estimator, Miller-Madow, or Linsker?\n\n**Success Indicators:**\n- Identify standard load monitoring practices\n- Find papers on entropy estimation with finite samples\n- Specify window size based on OS load averaging practices\n- Document discretization approach with justification\n\n---\n\n## Phase 3: Load Momentum / Trend Analysis\n\n**Objective:** Specify concrete method for computing load gradient/momentum and smoothing strategy.\n\n**Research Questions:**\n1. How do existing systems compute load trends? (Simple difference? Polynomial fit? EWMA?)\n2. What smoothing techniques reduce noise in load gradient estimates?\n3. How much lag/delay is acceptable in momentum estimation?\n4. How are load trends used in existing resource allocation decisions?\n5. What is typical load derivative magnitude for bursty workloads?\n\n**Key Search Topics:**\n- \"Load trend\" + \"prediction\" + \"forecasting\"\n- \"First-order derivative\" + \"noisy signals\" + \"CPU load\"\n- \"Rate of change\" + \"resource scheduling\"\n- \"EWMA\" + \"trend smoothing\"\n- \"Savitzky-Golay filter\" + \"load\" (if smoothing discussion exists)\n- \"PID controller\" + \"resource allocation\" (for inspiration from control systems)\n- \"Momentum\" + \"scheduling\" in RL / control literature\n\n**Concrete Design Decisions Needed:**\n- Momentum window: How far back to look (e.g., last 2-5 load samples)\n- Derivative method: Simple difference, linear regression over window, or EWMA?\n- Smoothing: Alpha parameter for EWMA or window size for regression?\n- Negative momentum threshold: What counts as \"decreasing trend\"? (e.g., >1% decrease?)\n- Detection delay: How recent must momentum be to be useful?\n\n**Success Indicators:**\n- Specify derivative estimation method with noise tolerance analysis\n- Document typical load gradient magnitudes for bursty workloads\n- Identify smoothing parameter ranges from literature\n- Define threshold for \"negative momentum\" scheduling opportunity\n\n---\n\n## Phase 4: Adaptive Threshold Formula\n\n**Objective:** Design the specific mathematical function mapping entropy → scheduling CPU limit.\n\n**Research Questions:**\n1. What functional forms are used for adaptive thresholding in other domains? (Sigmoid? Linear? Logarithmic?)\n2. How do scheduling thresholds vary in practice? (What range: 30%-80%?)\n3. What is the relationship between load entropy and scheduling risk tolerance?\n4. How aggressive should the adaptation be? (Large swings vs. conservative changes?)\n\n**Key Search Topics:**\n- \"Adaptive threshold\" + \"resource allocation\"\n- \"Control system\" + \"setpoint adaptation\"\n- \"Scheduling threshold\" + \"QoS\"\n- \"Risk-aware scheduling\"\n- \"Entropy vs. safety\" tradeoffs\n\n**Concrete Design Decisions Needed:**\n- Base threshold: Fixed CPU load limit when entropy is 0 (e.g., 50%)\n- Max threshold: CPU limit when entropy is maximal (e.g., 25%)\n- Functional form: Linear interpolation? Sigmoid? Exponential decay?\n- Entropy range normalization: Min entropy 0, max entropy log₂(bins)?\n- Formula example: threshold(e) = base - (base - min) * (e / e_max)\n- Adaptation speed: How quickly to update threshold on entropy changes?\n\n**Success Indicators:**\n- Specify parametric formula with clear interpretation\n- Identify parameter ranges from scheduling literature\n- Document relationship assumptions between entropy and scheduling safety\n\n---\n\n## Phase 5: Baseline Scheduler Specification\n\n**Objective:** Define the fixed-threshold scheduler that serves as comparison baseline.\n\n**Research Questions:**\n1. What is a standard fixed CPU threshold for background jobs? (50%? 70%? 80%?)\n2. How do production systems currently make schedule-vs-don't-schedule decisions?\n3. What background job scheduling strategies exist in real systems? (Nice levels? Cgroups? Custom?)\n\n**Key Search Topics:**\n- \"Background job scheduling\" + \"Linux\" + \"nice level\"\n- \"CPU cgroup\" + \"background tasks\"\n- \"Batch scheduling\" + \"CPU threshold\"\n- \"Low-priority tasks\" + \"scheduling\"\n\n**Concrete Design Decisions Needed:**\n- Baseline threshold value: Most common choice in literature (e.g., 50-60%?)\n- Decision rule: \"Schedule if CPU < threshold\" or include other factors?\n- Job priority mechanism: Nice level adjustment? IO class? Cgroup limits?\n- No momentum component in baseline (pure threshold-based)\n\n**Success Indicators:**\n- Identify standard threshold choices in production systems\n- Document baseline scheduling strategy used in comparison\n- Ensure baseline is fair/representative for comparison\n\n---\n\n## Phase 6: Success Metrics Definition\n\n**Objective:** Specify precise definitions and measurement methods for all four success criteria.\n\n**Research Questions:**\n1. How is \"completion time variance\" measured in scheduling papers? (Coefficient of variation? Std dev?)\n2. How do papers measure \"latency impact\" on foreground traffic? (Percentile latencies? Slowdown factors?)\n3. How is correlation computed between entropy and scheduling outcomes? (Pearson? Spearman?)\n4. How to quantify \"false positives\"? (Scheduling events followed by immediate load spike?)\n\n**Key Search Topics:**\n- \"Variance reduction\" measurement in scheduling papers\n- \"Percentile latency\" + \"SLO\" + \"measurement\"\n- \"Completion time distribution\" + \"scheduling\"\n- \"Fairness metrics\" + \"scheduling\"\n- \"False positive rate\" + \"prediction\" + \"resource management\"\n\n**Concrete Design Decisions Needed:**\n- Completion time variance: Use coefficient of variation (σ/μ) or relative standard deviation?\n- Foreground latency: Measure p50, p95, p99? Which matters most?\n- Entropy-safety correlation: Measure correlation between {entropy sample, outcome} pairs over window?\n- False positive definition: Schedule at t, then load jumps >10% in next 5 seconds?\n- Statistical significance: Minimum sample size, confidence intervals, hypothesis tests?\n\n**Success Indicators:**\n- Define all four metrics with clear mathematical formulas\n- Specify measurement procedures and aggregation methods\n- Identify appropriate statistical tests for significance\n- Document success criterion thresholds (20%, 10%, r>0.7, false-positive rate)\n\n---\n\n## Phase 7: Related Work & Novelty Analysis\n\n**Objective:** Verify positioning relative to related work and identify genuine novelty gaps.\n\n**Research Questions:**\n1. Do papers on Mixture-of-Schedulers (2511.11628) discuss entropy or load entropy-based routing?\n2. Does PREACT (3673038.3673135) use entropy-based adaptation? What exactly does it use?\n3. Do load trend papers (cited in hypothesis) combine trend + entropy? Or just trend?\n4. Has entropy been combined with momentum-based dispatch timing before?\n\n**Key Search Topics:**\n- Fetch and review the hypothesis-cited papers:\n  - 2511.11628 (Mixture-of-Schedulers)\n  - 3673038.3673135 (PREACT)\n  - 2606.02982 (DriftSched)\n  - 2601.19624 (RL entropy scheduling)\n- \"Entropy\" + \"scheduling\" cross-check in recent papers\n- \"Momentum dispatch\" + \"scheduling\"\n- \"Bursty workload\" + \"adaptive\" + review top results\n\n**Concrete Design Decisions Needed:**\n- Confirm novelty claim: Entropy-driven thresholds are NOT used in cited work\n- Confirm momentum component: Dispatch timing based on negative momentum is novel approach\n- Document exact differentiation from each related work\n- Identify whether combination of entropy + momentum is the core novelty\n\n**Success Indicators:**\n- Retrieve and summarize key findings from 4 cited papers\n- Confirm entropy-based threshold adaptation is genuinely novel\n- Confirm momentum-based dispatch is genuinely novel contribution\n- Document positioning summary for executor to include\n\n---\n\n## Research Output Structure\n\nThe executor should produce `research_out.json` with:\n\n```json\n{\n  \"answer\": {\n    \"entropy_estimator_design\": {\n      \"window_duration_seconds\": <number>,\n      \"sampling_frequency_hz\": <number>,\n      \"discretization_bins\": <number>,\n      \"bin_ranges\": <array>,\n      \"data_source\": \"<string>\",\n      \"entropy_formula\": \"<string>\",\n      \"bias_correction_method\": \"<string>\",\n      \"rationale\": \"<string>\"\n    },\n    \"momentum_estimator_design\": {\n      \"window_size_samples\": <number>,\n      \"derivative_method\": \"<string>\",\n      \"smoothing_method\": \"<string>\",\n      \"smoothing_parameter\": <number>,\n      \"negative_momentum_threshold\": \"<string>\",\n      \"rationale\": \"<string>\"\n    },\n    \"adaptive_threshold_formula\": {\n      \"functional_form\": \"<string>\",\n      \"parameters\": {\n        \"base_threshold_percent\": <number>,\n        \"min_threshold_percent\": <number>,\n        \"max_entropy_normalized\": <number>\n      },\n      \"formula\": \"<mathematical string>\",\n      \"interpretation\": \"<string>\",\n      \"rationale\": \"<string>\"\n    },\n    \"baseline_scheduler\": {\n      \"threshold_percent\": <number>,\n      \"decision_rule\": \"<string>\",\n      \"job_priority_mechanism\": \"<string>\",\n      \"rationale\": \"<string>\"\n    },\n    \"success_metrics\": {\n      \"completion_time_variance\": {\n        \"definition\": \"<string>\",\n        \"formula\": \"<string>\",\n        \"target_reduction_percent\": <number>\n      },\n      \"foreground_latency_p95\": {\n        \"definition\": \"<string>\",\n        \"target_improvement_percent\": <number>\n      },\n      \"entropy_safety_correlation\": {\n        \"definition\": \"<string>\",\n        \"method\": \"<string>\",\n        \"target_r\": <number>\n      },\n      \"false_positive_rate\": {\n        \"definition\": \"<string>\",\n        \"measurement_window_seconds\": <number>,\n        \"spike_threshold_percent\": <number>\n      }\n    },\n    \"novelty_summary\": {\n      \"entropy_based_adaptation\": \"<whether this component is novel>\",\n      \"momentum_dispatch\": \"<whether this component is novel>\",\n      \"differentiation_from_related_work\": \"<string>\"\n    }\n  },\n  \"sources\": [\n    \"<list of papers/sources consulted>\"\n  ],\n  \"follow_up_questions\": [\n    \"<questions for next iteration if needed>\"\n  ]\n}\n```\n\n---\n\n## Research Implementation Notes\n\n1. **Search Strategy:** Start with broad searches on adaptive scheduling, then progressively narrow to entropy and momentum specifically.\n\n2. **Paper Retrieval:** For high-value papers (especially the 4 cited in hypothesis), fetch and grep for specific details on:\n   - How they adapt scheduling decisions\n   - What signals they use (entropy? load trend? QPS?)\n   - What success metrics they report\n\n3. **Synthesis:** For each design component, synthesize findings from multiple sources to build consensus on parameter ranges.\n\n4. **Fallback:** If a specific technique has no literature, the executor should document the assumption and design choice rationale.\n\n5. **Validation:** Ensure all formulas and parameters are internally consistent (e.g., entropy normalization matches bin count).\n\n6. **Timeline:** Approximately 1-2 hours of focused web research should suffice, organized as:\n   - 20 min: Adaptive scheduling landscape\n   - 15 min: Entropy estimation specifics\n   - 15 min: Load momentum methods\n   - 15 min: Threshold formula design\n   - 10 min: Baseline scheduler\n   - 15 min: Success metrics detail\n   - 10 min: Related work verification\n   - 10 min: Synthesis and JSON generation\n", "structuredPatch": [], "originalFile": null, "userModified": false}
````

### [22] ASSISTANT · 2026-08-24 10:53:31 UTC

```
Now I'll create the final JSON plan output in the required format:
```

### [23] TOOL CALL — Write · 2026-08-24 10:53:31 UTC

```
File: ./.terminal_claude_agent_struct_out.json

{
  "title": "Design Parameters for Entropy-Adaptive Scheduler",
  "summary": "Establish concrete design specifications for an entropy-adaptive background job scheduler through literature review of adaptive scheduling, load entropy estimation, load momentum analysis, adaptive threshold formulas, and baseline scheduler design.",
  "runpod_compute_profile": "cpu_light",
  "question": "What concrete design parameters enable entropy-adaptive background job scheduling to outperform fixed-threshold schedulers under bursty CPU loads?",
  "research_plan": "## Phase 1: Adaptive Scheduling & Entropy Literature (1.5 hours)\n\n**Objective:** Survey existing adaptive scheduling approaches and identify whether entropy/information-theoretic measures have been applied to CPU scheduling decisions.\n\n**Steps:**\n1. Search for adaptive scheduling in modern OS kernels (Linux CFS, BFQ, Windows) and how they adapt to workload characteristics\n2. Search for entropy or information-theoretic approaches in resource allocation literature\n3. Review the hypothesis-cited related work papers (2511.11628 Mixture-of-Schedulers, 3673038.3673135 PREACT, 2606.02982 DriftSched, 2601.19624 RL entropy) to understand:\n   - What signals they use for adaptation (workload type? load entropy? QPS prediction? token drift?)\n   - Whether they combine entropy with other signals\n   - Whether momentum/trend-based dispatch timing is used\n4. Search for data center scheduling and QoS-aware scheduling approaches\n5. Document findings on gap between fixed-threshold and adaptive approaches\n\n**Deliverable:** Summary of adaptive scheduling landscape with evidence of novelty gaps.\n\n---\n\n## Phase 2: Load Entropy Estimator Design (1 hour)\n\n**Objective:** Specify concrete parameters for Shannon entropy calculation from CPU load samples.\n\n**Steps:**\n1. Search for standard CPU load monitoring practices:\n   - How Linux load average is calculated and sampled\n   - Typical monitoring intervals in production systems (1s? 5s? 60s?)\n   - Data sources (/proc/stat, /proc/loadavg, or perf counters)\n\n2. Research entropy estimation methods:\n   - Search for Shannon entropy estimation with limited samples\n   - Find papers on bias correction (Miller-Madow, plugin, Linsker methods)\n   - Document typical entropy values for different load patterns\n\n3. Determine discretization strategy:\n   - Search for load distribution analysis in web servers/data centers\n   - Identify optimal number of entropy bins (typically 5-10)\n   - Define bin boundaries (percentile-based vs. fixed ranges)\n\n4. Research burstiness metrics to validate entropy signal:\n   - Coefficient of variation in load\n   - Hurst exponent or autocorrelation measures\n   - How burstiness correlates with scheduling difficulty\n\n**Decisions to Make:**\n- Window duration: Recommend 30-120 second windows (check OS load average conventions)\n- Sampling frequency: Specify 100ms-1s intervals\n- Discretization: Number of bins and boundary strategy\n- Entropy formula: Confirm H = -Σ p_i * log₂(p_i) is appropriate\n- Bias correction method: Choose based on typical sample counts\n\n**Deliverable:** Detailed entropy estimator specification with parameter justification.\n\n---\n\n## Phase 3: Load Momentum Estimator Design (1 hour)\n\n**Objective:** Specify method for computing load gradient and smoothing strategy.\n\n**Steps:**\n1. Research load prediction and trend analysis:\n   - Search for load forecasting methods in resource management literature\n   - Document typical first-order derivative approaches (simple difference, linear regression, EWMA)\n   - Find papers on smoothing techniques for noisy load data (Savitzky-Golay, EWMA)\n\n2. Study existing momentum/trend-based decisions:\n   - Search for PID controllers or control systems in resource allocation (inspiration)\n   - Look for rate-of-change signals in resource scheduling\n   - Document acceptable lag/delay tolerance\n\n3. Characterize load gradients in bursty workloads:\n   - Search for load spike magnitude and frequency data\n   - Estimate typical derivative values for scheduled vs. unscheduled loads\n   - Determine threshold for \"negative momentum\" (e.g., >1% decrease)\n\n4. Evaluate smoothing strategies:\n   - EWMA: Find recommended alpha values for load-like signals (typically 0.1-0.3)\n   - Linear regression: Window size tradeoffs (smaller = responsive, larger = robust)\n   - Determine detection delay requirements\n\n**Decisions to Make:**\n- Derivative method: Simple difference or EWMA? (trade responsiveness vs. noise)\n- Smoothing window: 2-5 load samples (5-120 seconds depending on sample rate)\n- Negative momentum threshold: Specific percentage decrease rate\n- Update frequency: How often to recompute momentum\n\n**Deliverable:** Load momentum estimator specification with noise tolerance analysis.\n\n---\n\n## Phase 4: Adaptive Threshold Formula Design (45 minutes)\n\n**Objective:** Design the mapping function from entropy → scheduling CPU limit.\n\n**Steps:**\n1. Research adaptive thresholding in other domains:\n   - Search for threshold adaptation in control systems, resource allocation\n   - Document functional forms used (linear, sigmoid, exponential, logarithmic)\n   - Find examples of entropy-driven threshold adjustment\n\n2. Determine threshold ranges:\n   - What CPU load limits are typical for background jobs? (25%-80% range?)\n   - How much variation is reasonable between entropy extremes?\n   - Document adaptation speed (gradual vs. aggressive)\n\n3. Design the formula:\n   - Establish base case: threshold when entropy is 0 (low variability → permissive)\n   - Establish conservative case: threshold when entropy is maximum (high variability → conservative)\n   - Choose functional form: Linear interpolation is simplest; consider sigmoid for smoother saturation\n\n4. Validate formula properties:\n   - High entropy (bursty load) → LOW threshold (conservative scheduling)\n   - Low entropy (smooth load) → HIGH threshold (aggressive scheduling)\n   - Monotonicity: More entropy always means lower threshold or constant\n\n**Decisions to Make:**\n- Base threshold (low entropy): e.g., 60-70%\n- Min threshold (high entropy): e.g., 20-30%\n- Functional form: Linear or sigmoid\n- Normalization: Entropy range 0 to log₂(bins)\n\n**Deliverable:** Mathematical formula with clear parameter semantics.\n\n---\n\n## Phase 5: Baseline Scheduler Specification (30 minutes)\n\n**Objective:** Define the fixed-threshold scheduler used for comparison.\n\n**Steps:**\n1. Research production background scheduling:\n   - Search for Linux nice level usage, cgroup CPU limits\n   - Identify standard CPU thresholds used (e.g., 50%, 60%)\n   - Document how systems currently decide to run background jobs\n\n2. Select representative baseline:\n   - Fixed threshold approach (no entropy, no momentum)\n   - Threshold value justified from literature\n   - Simple decision rule: \"Schedule if CPU < threshold\"\n\n3. Ensure fair comparison:\n   - Baseline and adaptive both use same background job priority mechanism (nice level? cgroups?)\n   - Both measure same foreground latency metrics\n   - Both operate on same synthetic workload\n\n**Decisions to Make:**\n- Baseline CPU threshold: Recommend 50-60% based on literature\n- Decision rule: Pure threshold only, no other factors\n- Job priority: Same as adaptive scheduler\n\n**Deliverable:** Formal specification of baseline scheduler.\n\n---\n\n## Phase 6: Success Metrics Definition (1 hour)\n\n**Objective:** Specify precise formulas and measurement procedures for all success criteria.\n\n**Steps:**\n1. Completion time variance reduction (target: 20%+):\n   - Search for variance/variability metrics in scheduling papers\n   - Decide: Coefficient of variation σ/μ or other normalized metric?\n   - Specify: How to aggregate across job batch sizes\n   - Justify: Why 20% is a meaningful threshold\n\n2. Foreground latency improvement (target: 10%+):\n   - Search for p95, p99 latency as SLO metrics in literature\n   - Decide: p50 vs. p95 vs. p99? (p95 is industry standard)\n   - Specify: Latency under adaptive vs. baseline\n   - Define: \"Improvement\" = (baseline - adaptive) / baseline * 100%\n\n3. Entropy-safety correlation (target: r > 0.7):\n   - Search for Pearson vs. Spearman correlation in scheduling literature\n   - Decide: Correlation between entropy samples and scheduling outcomes\n   - Specify: What counts as \"outcome\"? (foreground latency impact? completion delay?)\n   - Ensure: Sufficient samples for correlation (n ≥ 30-50)\n\n4. False positive rate definition:\n   - Define: Scheduling at time t, then load jumps >X% within Y seconds\n   - Typical thresholds: >10-20% jump in 2-5 second window\n   - Count false positives: % of schedules followed by immediate spike\n   - Target: Lower is better; baseline is comparison point\n\n5. Statistical significance:\n   - Minimum trials/samples: 50-100 runs per scheduler\n   - Confidence intervals: 95% CI around mean metrics\n   - Hypothesis tests: t-test for latency, Fisher z-test for correlation\n\n**Decisions to Make:**\n- Variance metric: σ/μ (coefficient of variation)\n- Foreground latency: p95 latency percentile\n- Correlation method: Pearson r over windowed entropy-outcome pairs\n- False positive window: 5-second lookahead, >15% spike threshold\n\n**Deliverable:** Precise metric definitions with formulas and success thresholds.\n\n---\n\n## Phase 7: Related Work Verification & Novelty (1.5 hours)\n\n**Objective:** Confirm that entropy-adaptive + momentum-based dispatch are genuinely novel.\n\n**Steps:**\n1. Fetch and carefully read the four hypothesis-cited papers:\n   - 2511.11628 (Mixture-of-Schedulers): Does it use entropy? How does it route to expert schedulers?\n   - 3673038.3673135 (PREACT): Uses QPS prediction, not entropy. What is the exact adaptation signal?\n   - 2606.02982 (DriftSched): GPU inference, uses token drift. Different substrate/signal.\n   - 2601.19624 (RL entropy): Exploration policy in RL, not CPU load scheduling.\n\n2. Document exact differentiation:\n   - Mixture-of-Schedulers: Routes based on WORKLOAD TYPE, not LOAD ENTROPY → Novel\n   - PREACT: Predicts QPS at data center scale, not single-machine load entropy → Novel\n   - DriftSched: GPU-specific, token-drift signal, not CPU entropy → Novel\n   - RL entropy: Exploration tuning, not resource allocation → Novel\n\n3. Cross-check for entropy + momentum combination:\n   - Search: \"Entropy scheduling\" (last 3 years)\n   - Search: \"Momentum dispatch\" or \"gradient-based scheduling\"\n   - Confirm: No existing system combines entropy threshold adaptation + momentum-based timing\n\n4. Document positioning summary:\n   - Core novelty: Entropy-driven threshold adaptation is new to this domain\n   - Secondary novelty: Momentum/gradient-based dispatch timing within entropy zones\n   - Contribution: Combines information theory (entropy) + control systems (momentum) for background jobs\n\n**Deliverable:** Related work summary confirming novelty, including differentiators for each cited paper.\n\n---\n\n## Final Synthesis & JSON Output (30 minutes)\n\n**Steps:**\n1. Consolidate all findings into structured JSON with:\n   - Entropy estimator design (window, bins, formula, rationale)\n   - Momentum estimator design (method, smoothing, threshold)\n   - Adaptive threshold formula (functional form, parameters, interpretation)\n   - Baseline scheduler specification (threshold, rule, priority mechanism)\n   - Success metrics (precise definitions, formulas, targets)\n   - Novelty summary (what's novel vs. related work)\n\n2. Validate consistency:\n   - Entropy normalization matches bin count\n   - Threshold formula parameters are in same units\n   - Metrics can all be measured from synthetic workload\n   - Success criteria are realistic but ambitious\n\n3. Generate follow-up questions:\n   - Are there open questions for the executor/designer?\n   - Should momentum-based dispatch use weighted history or single sample?\n   - How to handle entropy initialization (cold start)?\n   - Is entropy discretization or continuous distribution better?\n\n**Deliverable:** research_out.json with complete design specification.",
  "explanation": "This research establishes all design parameters needed for the executor to implement and test the entropy-adaptive scheduler. The hypothesis claims that adapting CPU scheduling thresholds based on load entropy (unpredictability) and prioritizing negative load momentum will improve both background job completion time and foreground latency under bursty workloads. To test this properly, we must first specify: (1) how to measure entropy from CPU load samples, (2) how to estimate momentum/load trends, (3) the exact formula mapping entropy to scheduling limits, (4) what baseline scheduler to compare against, and (5) precise success metrics to validate the hypothesis. Literature review on adaptive scheduling, load monitoring, entropy estimation, and control systems informs these design choices. Without these specifications, the executor cannot implement the system credibly or measure success rigorously."
}
```

### [24] TOOL RESULT — Write · 2026-08-24 10:53:31 UTC

```
{"type": "create", "filePath": "./.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"Design Parameters for Entropy-Adaptive Scheduler\",\n  \"summary\": \"Establish concrete design specifications for an entropy-adaptive background job scheduler through literature review of adaptive scheduling, load entropy estimation, load momentum analysis, adaptive threshold formulas, and baseline scheduler design.\",\n  \"runpod_compute_profile\": \"cpu_light\",\n  \"question\": \"What concrete design parameters enable entropy-adaptive background job scheduling to outperform fixed-threshold schedulers under bursty CPU loads?\",\n  \"research_plan\": \"## Phase 1: Adaptive Scheduling & Entropy Literature (1.5 hours)\\n\\n**Objective:** Survey existing adaptive scheduling approaches and identify whether entropy/information-theoretic measures have been applied to CPU scheduling decisions.\\n\\n**Steps:**\\n1. Search for adaptive scheduling in modern OS kernels (Linux CFS, BFQ, Windows) and how they adapt to workload characteristics\\n2. Search for entropy or information-theoretic approaches in resource allocation literature\\n3. Review the hypothesis-cited related work papers (2511.11628 Mixture-of-Schedulers, 3673038.3673135 PREACT, 2606.02982 DriftSched, 2601.19624 RL entropy) to understand:\\n   - What signals they use for adaptation (workload type? load entropy? QPS prediction? token drift?)\\n   - Whether they combine entropy with other signals\\n   - Whether momentum/trend-based dispatch timing is used\\n4. Search for data center scheduling and QoS-aware scheduling approaches\\n5. Document findings on gap between fixed-threshold and adaptive approaches\\n\\n**Deliverable:** Summary of adaptive scheduling landscape with evidence of novelty gaps.\\n\\n---\\n\\n## Phase 2: Load Entropy Estimator Design (1 hour)\\n\\n**Objective:** Specify concrete parameters for Shannon entropy calculation from CPU load samples.\\n\\n**Steps:**\\n1. Search for standard CPU load monitoring practices:\\n   - How Linux load average is calculated and sampled\\n   - Typical monitoring intervals in production systems (1s? 5s? 60s?)\\n   - Data sources (/proc/stat, /proc/loadavg, or perf counters)\\n\\n2. Research entropy estimation methods:\\n   - Search for Shannon entropy estimation with limited samples\\n   - Find papers on bias correction (Miller-Madow, plugin, Linsker methods)\\n   - Document typical entropy values for different load patterns\\n\\n3. Determine discretization strategy:\\n   - Search for load distribution analysis in web servers/data centers\\n   - Identify optimal number of entropy bins (typically 5-10)\\n   - Define bin boundaries (percentile-based vs. fixed ranges)\\n\\n4. Research burstiness metrics to validate entropy signal:\\n   - Coefficient of variation in load\\n   - Hurst exponent or autocorrelation measures\\n   - How burstiness correlates with scheduling difficulty\\n\\n**Decisions to Make:**\\n- Window duration: Recommend 30-120 second windows (check OS load average conventions)\\n- Sampling frequency: Specify 100ms-1s intervals\\n- Discretization: Number of bins and boundary strategy\\n- Entropy formula: Confirm H = -Σ p_i * log₂(p_i) is appropriate\\n- Bias correction method: Choose based on typical sample counts\\n\\n**Deliverable:** Detailed entropy estimator specification with parameter justification.\\n\\n---\\n\\n## Phase 3: Load Momentum Estimator Design (1 hour)\\n\\n**Objective:** Specify method for computing load gradient and smoothing strategy.\\n\\n**Steps:**\\n1. Research load prediction and trend analysis:\\n   - Search for load forecasting methods in resource management literature\\n   - Document typical first-order derivative approaches (simple difference, linear regression, EWMA)\\n   - Find papers on smoothing techniques for noisy load data (Savitzky-Golay, EWMA)\\n\\n2. Study existing momentum/trend-based decisions:\\n   - Search for PID controllers or control systems in resource allocation (inspiration)\\n   - Look for rate-of-change signals in resource scheduling\\n   - Document acceptable lag/delay tolerance\\n\\n3. Characterize load gradients in bursty workloads:\\n   - Search for load spike magnitude and frequency data\\n   - Estimate typical derivative values for scheduled vs. unscheduled loads\\n   - Determine threshold for \\\"negative momentum\\\" (e.g., >1% decrease)\\n\\n4. Evaluate smoothing strategies:\\n   - EWMA: Find recommended alpha values for load-like signals (typically 0.1-0.3)\\n   - Linear regression: Window size tradeoffs (smaller = responsive, larger = robust)\\n   - Determine detection delay requirements\\n\\n**Decisions to Make:**\\n- Derivative method: Simple difference or EWMA? (trade responsiveness vs. noise)\\n- Smoothing window: 2-5 load samples (5-120 seconds depending on sample rate)\\n- Negative momentum threshold: Specific percentage decrease rate\\n- Update frequency: How often to recompute momentum\\n\\n**Deliverable:** Load momentum estimator specification with noise tolerance analysis.\\n\\n---\\n\\n## Phase 4: Adaptive Threshold Formula Design (45 minutes)\\n\\n**Objective:** Design the mapping function from entropy → scheduling CPU limit.\\n\\n**Steps:**\\n1. Research adaptive thresholding in other domains:\\n   - Search for threshold adaptation in control systems, resource allocation\\n   - Document functional forms used (linear, sigmoid, exponential, logarithmic)\\n   - Find examples of entropy-driven threshold adjustment\\n\\n2. Determine threshold ranges:\\n   - What CPU load limits are typical for background jobs? (25%-80% range?)\\n   - How much variation is reasonable between entropy extremes?\\n   - Document adaptation speed (gradual vs. aggressive)\\n\\n3. Design the formula:\\n   - Establish base case: threshold when entropy is 0 (low variability → permissive)\\n   - Establish conservative case: threshold when entropy is maximum (high variability → conservative)\\n   - Choose functional form: Linear interpolation is simplest; consider sigmoid for smoother saturation\\n\\n4. Validate formula properties:\\n   - High entropy (bursty load) → LOW threshold (conservative scheduling)\\n   - Low entropy (smooth load) → HIGH threshold (aggressive scheduling)\\n   - Monotonicity: More entropy always means lower threshold or constant\\n\\n**Decisions to Make:**\\n- Base threshold (low entropy): e.g., 60-70%\\n- Min threshold (high entropy): e.g., 20-30%\\n- Functional form: Linear or sigmoid\\n- Normalization: Entropy range 0 to log₂(bins)\\n\\n**Deliverable:** Mathematical formula with clear parameter semantics.\\n\\n---\\n\\n## Phase 5: Baseline Scheduler Specification (30 minutes)\\n\\n**Objective:** Define the fixed-threshold scheduler used for comparison.\\n\\n**Steps:**\\n1. Research production background scheduling:\\n   - Search for Linux nice level usage, cgroup CPU limits\\n   - Identify standard CPU thresholds used (e.g., 50%, 60%)\\n   - Document how systems currently decide to run background jobs\\n\\n2. Select representative baseline:\\n   - Fixed threshold approach (no entropy, no momentum)\\n   - Threshold value justified from literature\\n   - Simple decision rule: \\\"Schedule if CPU < threshold\\\"\\n\\n3. Ensure fair comparison:\\n   - Baseline and adaptive both use same background job priority mechanism (nice level? cgroups?)\\n   - Both measure same foreground latency metrics\\n   - Both operate on same synthetic workload\\n\\n**Decisions to Make:**\\n- Baseline CPU threshold: Recommend 50-60% based on literature\\n- Decision rule: Pure threshold only, no other factors\\n- Job priority: Same as adaptive scheduler\\n\\n**Deliverable:** Formal specification of baseline scheduler.\\n\\n---\\n\\n## Phase 6: Success Metrics Definition (1 hour)\\n\\n**Objective:** Specify precise formulas and measurement procedures for all success criteria.\\n\\n**Steps:**\\n1. Completion time variance reduction (target: 20%+):\\n   - Search for variance/variability metrics in scheduling papers\\n   - Decide: Coefficient of variation σ/μ or other normalized metric?\\n   - Specify: How to aggregate across job batch sizes\\n   - Justify: Why 20% is a meaningful threshold\\n\\n2. Foreground latency improvement (target: 10%+):\\n   - Search for p95, p99 latency as SLO metrics in literature\\n   - Decide: p50 vs. p95 vs. p99? (p95 is industry standard)\\n   - Specify: Latency under adaptive vs. baseline\\n   - Define: \\\"Improvement\\\" = (baseline - adaptive) / baseline * 100%\\n\\n3. Entropy-safety correlation (target: r > 0.7):\\n   - Search for Pearson vs. Spearman correlation in scheduling literature\\n   - Decide: Correlation between entropy samples and scheduling outcomes\\n   - Specify: What counts as \\\"outcome\\\"? (foreground latency impact? completion delay?)\\n   - Ensure: Sufficient samples for correlation (n ≥ 30-50)\\n\\n4. False positive rate definition:\\n   - Define: Scheduling at time t, then load jumps >X% within Y seconds\\n   - Typical thresholds: >10-20% jump in 2-5 second window\\n   - Count false positives: % of schedules followed by immediate spike\\n   - Target: Lower is better; baseline is comparison point\\n\\n5. Statistical significance:\\n   - Minimum trials/samples: 50-100 runs per scheduler\\n   - Confidence intervals: 95% CI around mean metrics\\n   - Hypothesis tests: t-test for latency, Fisher z-test for correlation\\n\\n**Decisions to Make:**\\n- Variance metric: σ/μ (coefficient of variation)\\n- Foreground latency: p95 latency percentile\\n- Correlation method: Pearson r over windowed entropy-outcome pairs\\n- False positive window: 5-second lookahead, >15% spike threshold\\n\\n**Deliverable:** Precise metric definitions with formulas and success thresholds.\\n\\n---\\n\\n## Phase 7: Related Work Verification & Novelty (1.5 hours)\\n\\n**Objective:** Confirm that entropy-adaptive + momentum-based dispatch are genuinely novel.\\n\\n**Steps:**\\n1. Fetch and carefully read the four hypothesis-cited papers:\\n   - 2511.11628 (Mixture-of-Schedulers): Does it use entropy? How does it route to expert schedulers?\\n   - 3673038.3673135 (PREACT): Uses QPS prediction, not entropy. What is the exact adaptation signal?\\n   - 2606.02982 (DriftSched): GPU inference, uses token drift. Different substrate/signal.\\n   - 2601.19624 (RL entropy): Exploration policy in RL, not CPU load scheduling.\\n\\n2. Document exact differentiation:\\n   - Mixture-of-Schedulers: Routes based on WORKLOAD TYPE, not LOAD ENTROPY → Novel\\n   - PREACT: Predicts QPS at data center scale, not single-machine load entropy → Novel\\n   - DriftSched: GPU-specific, token-drift signal, not CPU entropy → Novel\\n   - RL entropy: Exploration tuning, not resource allocation → Novel\\n\\n3. Cross-check for entropy + momentum combination:\\n   - Search: \\\"Entropy scheduling\\\" (last 3 years)\\n   - Search: \\\"Momentum dispatch\\\" or \\\"gradient-based scheduling\\\"\\n   - Confirm: No existing system combines entropy threshold adaptation + momentum-based timing\\n\\n4. Document positioning summary:\\n   - Core novelty: Entropy-driven threshold adaptation is new to this domain\\n   - Secondary novelty: Momentum/gradient-based dispatch timing within entropy zones\\n   - Contribution: Combines information theory (entropy) + control systems (momentum) for background jobs\\n\\n**Deliverable:** Related work summary confirming novelty, including differentiators for each cited paper.\\n\\n---\\n\\n## Final Synthesis & JSON Output (30 minutes)\\n\\n**Steps:**\\n1. Consolidate all findings into structured JSON with:\\n   - Entropy estimator design (window, bins, formula, rationale)\\n   - Momentum estimator design (method, smoothing, threshold)\\n   - Adaptive threshold formula (functional form, parameters, interpretation)\\n   - Baseline scheduler specification (threshold, rule, priority mechanism)\\n   - Success metrics (precise definitions, formulas, targets)\\n   - Novelty summary (what's novel vs. related work)\\n\\n2. Validate consistency:\\n   - Entropy normalization matches bin count\\n   - Threshold formula parameters are in same units\\n   - Metrics can all be measured from synthetic workload\\n   - Success criteria are realistic but ambitious\\n\\n3. Generate follow-up questions:\\n   - Are there open questions for the executor/designer?\\n   - Should momentum-based dispatch use weighted history or single sample?\\n   - How to handle entropy initialization (cold start)?\\n   - Is entropy discretization or continuous distribution better?\\n\\n**Deliverable:** research_out.json with complete design specification.\",\n  \"explanation\": \"This research establishes all design parameters needed for the executor to implement and test the entropy-adaptive scheduler. The hypothesis claims that adapting CPU scheduling thresholds based on load entropy (unpredictability) and prioritizing negative load momentum will improve both background job completion time and foreground latency under bursty workloads. To test this properly, we must first specify: (1) how to measure entropy from CPU load samples, (2) how to estimate momentum/load trends, (3) the exact formula mapping entropy to scheduling limits, (4) what baseline scheduler to compare against, and (5) precise success metrics to validate the hypothesis. Literature review on adaptive scheduling, load monitoring, entropy estimation, and control systems informs these design choices. Without these specifications, the executor cannot implement the system credibly or measure success rigorously.\"\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [25] ASSISTANT · 2026-08-24 10:53:39 UTC

```
Perfect! I've created a comprehensive research plan for the entropy-adaptive background job scheduler design. The plan is now saved in `./.terminal_claude_agent_struct_out.json`.

## Summary

The research plan establishes **7 phases** to ground the entropy-adaptive scheduler hypothesis in literature and concrete design parameters:

1. **Adaptive Scheduling & Entropy Literature** — Survey how modern OS schedulers adapt, whether entropy has been applied to scheduling, and verify novelty against cited related work

2. **Load Entropy Estimator Design** — Specify window duration, sampling rate, discretization strategy, bias correction method, and data source for Shannon entropy calculation

3. **Load Momentum Estimator** — Define derivative estimation method (simple difference vs. EWMA), smoothing strategy, and detection thresholds for negative load momentum

4. **Adaptive Threshold Formula** — Design the mathematical mapping from entropy → CPU scheduling limit, with clear parameter semantics (base threshold, min threshold, functional form)

5. **Baseline Scheduler** — Specify the fixed-threshold scheduler used for fair comparison

6. **Success Metrics** — Define precise formulas for:
   - 20%+ completion time variance reduction
   - 10%+ p95 latency improvement
   - r > 0.7 entropy-safety correlation
   - False positive rate measurement

7. **Related Work Verification** — Confirm that entropy-based threshold adaptation + momentum-based dispatch are genuinely novel contributions

Each phase includes concrete research questions, specific search terms, decisions to make, and deliverables. The executor can follow this step-by-step to gather literature, synthesize findings, and produce a detailed specification JSON with all design parameters justified by evidence.

**Output file:** `./.terminal_claude_agent_struct_out.json` ✓
```
