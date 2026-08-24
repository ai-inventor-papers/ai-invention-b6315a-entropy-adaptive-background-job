# gen_art_research_1 — test_idea

> Phase: `invention_loop` · round 1 · `gen_art`
> Run: `run_a-GYNIuwcKDN` — Entropy-Adaptive Background Job Scheduling for Bursty Workloads
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_research_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-24 10:54:40 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact executor (Step 3.3: GEN_ART in the invention loop)

Executing a plan to produce a concrete artifact.
GEN_PAPER_TEXT will use your artifact in the next paper draft.

Rigorous artifact with clear results → strong paper. Sloppy artifact → misdirected research.
</your_role>
</ai_inventor_context>

<task>
Conduct thorough, unbiased research on the given topic.
Adapt your investigation approach based on the research question and domain.
</task>

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

<critical_requirements>
1. SOURCE DIVERSITY - Consult MANY sources (10+), not just the first few results
2. AVOID SELECTION BIAS - Actively seek contradicting viewpoints, not just confirming ones
3. TRIANGULATE - Cross-reference claims across multiple independent sources
4. ACKNOWLEDGE UNCERTAINTY - Be honest about confidence levels and limitations
5. SYNTHESIZE - Produce a coherent answer that accounts for conflicting evidence
</critical_requirements>

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

Read and STRICTLY follow these skills: aii-web-tools.

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_a-GYNIuwcKDN/3_invention_loop/iter_1/gen_art/gen_art_research_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_a-GYNIuwcKDN/3_invention_loop/iter_1/gen_art/gen_art_research_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_a-GYNIuwcKDN/3_invention_loop/iter_1/gen_art/gen_art_research_1/file.py`, `/ai-inventor/aii_data/runs/run_a-GYNIuwcKDN/3_invention_loop/iter_1/gen_art/gen_art_research_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_a-GYNIuwcKDN/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for prior work and the field's landscape to ground your research.

- **aii-handbook-auto-computational-linguistics** — Field handbook for computational linguistics as a SCIENCE of language — grammaticality and minimal pairs (BLiMP), surprisal versus reading times, linguistic structure in LMs, annotator disagreement an
- **aii-handbook-auto-mechanistic-interpretability** — Field handbook for mechanistic interpretability of neural networks — circuit discovery, activation and attribution patching, sparse autoencoders, transcoders, attribution graphs, steering vectors, pro
- **aii-handbook-auto-multi-agent-llm-systems** — Field handbook for multi-agent LLM systems (MAS) — orchestration topology, multi-agent debate, mixture-of-agents, verifier and critic agents, inter-agent protocols (MCP/A2A), failure attribution and s
- **aii-handbook-auto-neurosymbolic** — Field handbook for neuro-symbolic AI — text-to-logic autoformalization (NL to FOL), LLM-plus-solver and prover pipelines (Prolog, ASP, SMT), probabilistic-differentiable NeSy (DeepProbLog, Scallop), r
</available_domain_handbooks>

<artifact_plan>
id: gen_plan_research_1_idx1
type: research
title: Design Parameters for Entropy-Adaptive Scheduler
summary: >-
  Establish concrete design specifications for an entropy-adaptive background job scheduler through literature review of adaptive
  scheduling, load entropy estimation, load momentum analysis, adaptive threshold formulas, and baseline scheduler design.
runpod_compute_profile: cpu_light
question: >-
  What concrete design parameters enable entropy-adaptive background job scheduling to outperform fixed-threshold schedulers
  under bursty CPU loads?
research_plan: |-
  ## Phase 1: Adaptive Scheduling & Entropy Literature (1.5 hours)

  **Objective:** Survey existing adaptive scheduling approaches and identify whether entropy/information-theoretic measures have been applied to CPU scheduling decisions.

  **Steps:**
  1. Search for adaptive scheduling in modern OS kernels (Linux CFS, BFQ, Windows) and how they adapt to workload characteristics
  2. Search for entropy or information-theoretic approaches in resource allocation literature
  3. Review the hypothesis-cited related work papers (2511.11628 Mixture-of-Schedulers, 3673038.3673135 PREACT, 2606.02982 DriftSched, 2601.19624 RL entropy) to understand:
     - What signals they use for adaptation (workload type? load entropy? QPS prediction? token drift?)
     - Whether they combine entropy with other signals
     - Whether momentum/trend-based dispatch timing is used
  4. Search for data center scheduling and QoS-aware scheduling approaches
  5. Document findings on gap between fixed-threshold and adaptive approaches

  **Deliverable:** Summary of adaptive scheduling landscape with evidence of novelty gaps.

  ---

  ## Phase 2: Load Entropy Estimator Design (1 hour)

  **Objective:** Specify concrete parameters for Shannon entropy calculation from CPU load samples.

  **Steps:**
  1. Search for standard CPU load monitoring practices:
     - How Linux load average is calculated and sampled
     - Typical monitoring intervals in production systems (1s? 5s? 60s?)
     - Data sources (/proc/stat, /proc/loadavg, or perf counters)

  2. Research entropy estimation methods:
     - Search for Shannon entropy estimation with limited samples
     - Find papers on bias correction (Miller-Madow, plugin, Linsker methods)
     - Document typical entropy values for different load patterns

  3. Determine discretization strategy:
     - Search for load distribution analysis in web servers/data centers
     - Identify optimal number of entropy bins (typically 5-10)
     - Define bin boundaries (percentile-based vs. fixed ranges)

  4. Research burstiness metrics to validate entropy signal:
     - Coefficient of variation in load
     - Hurst exponent or autocorrelation measures
     - How burstiness correlates with scheduling difficulty

  **Decisions to Make:**
  - Window duration: Recommend 30-120 second windows (check OS load average conventions)
  - Sampling frequency: Specify 100ms-1s intervals
  - Discretization: Number of bins and boundary strategy
  - Entropy formula: Confirm H = -Σ p_i * log₂(p_i) is appropriate
  - Bias correction method: Choose based on typical sample counts

  **Deliverable:** Detailed entropy estimator specification with parameter justification.

  ---

  ## Phase 3: Load Momentum Estimator Design (1 hour)

  **Objective:** Specify method for computing load gradient and smoothing strategy.

  **Steps:**
  1. Research load prediction and trend analysis:
     - Search for load forecasting methods in resource management literature
     - Document typical first-order derivative approaches (simple difference, linear regression, EWMA)
     - Find papers on smoothing techniques for noisy load data (Savitzky-Golay, EWMA)

  2. Study existing momentum/trend-based decisions:
     - Search for PID controllers or control systems in resource allocation (inspiration)
     - Look for rate-of-change signals in resource scheduling
     - Document acceptable lag/delay tolerance

  3. Characterize load gradients in bursty workloads:
     - Search for load spike magnitude and frequency data
     - Estimate typical derivative values for scheduled vs. unscheduled loads
     - Determine threshold for "negative momentum" (e.g., >1% decrease)

  4. Evaluate smoothing strategies:
     - EWMA: Find recommended alpha values for load-like signals (typically 0.1-0.3)
     - Linear regression: Window size tradeoffs (smaller = responsive, larger = robust)
     - Determine detection delay requirements

  **Decisions to Make:**
  - Derivative method: Simple difference or EWMA? (trade responsiveness vs. noise)
  - Smoothing window: 2-5 load samples (5-120 seconds depending on sample rate)
  - Negative momentum threshold: Specific percentage decrease rate
  - Update frequency: How often to recompute momentum

  **Deliverable:** Load momentum estimator specification with noise tolerance analysis.

  ---

  ## Phase 4: Adaptive Threshold Formula Design (45 minutes)

  **Objective:** Design the mapping function from entropy → scheduling CPU limit.

  **Steps:**
  1. Research adaptive thresholding in other domains:
     - Search for threshold adaptation in control systems, resource allocation
     - Document functional forms used (linear, sigmoid, exponential, logarithmic)
     - Find examples of entropy-driven threshold adjustment

  2. Determine threshold ranges:
     - What CPU load limits are typical for background jobs? (25%-80% range?)
     - How much variation is reasonable between entropy extremes?
     - Document adaptation speed (gradual vs. aggressive)

  3. Design the formula:
     - Establish base case: threshold when entropy is 0 (low variability → permissive)
     - Establish conservative case: threshold when entropy is maximum (high variability → conservative)
     - Choose functional form: Linear interpolation is simplest; consider sigmoid for smoother saturation

  4. Validate formula properties:
     - High entropy (bursty load) → LOW threshold (conservative scheduling)
     - Low entropy (smooth load) → HIGH threshold (aggressive scheduling)
     - Monotonicity: More entropy always means lower threshold or constant

  **Decisions to Make:**
  - Base threshold (low entropy): e.g., 60-70%
  - Min threshold (high entropy): e.g., 20-30%
  - Functional form: Linear or sigmoid
  - Normalization: Entropy range 0 to log₂(bins)

  **Deliverable:** Mathematical formula with clear parameter semantics.

  ---

  ## Phase 5: Baseline Scheduler Specification (30 minutes)

  **Objective:** Define the fixed-threshold scheduler used for comparison.

  **Steps:**
  1. Research production background scheduling:
     - Search for Linux nice level usage, cgroup CPU limits
     - Identify standard CPU thresholds used (e.g., 50%, 60%)
     - Document how systems currently decide to run background jobs

  2. Select representative baseline:
     - Fixed threshold approach (no entropy, no momentum)
     - Threshold value justified from literature
     - Simple decision rule: "Schedule if CPU < threshold"

  3. Ensure fair comparison:
     - Baseline and adaptive both use same background job priority mechanism (nice level? cgroups?)
     - Both measure same foreground latency metrics
     - Both operate on same synthetic workload

  **Decisions to Make:**
  - Baseline CPU threshold: Recommend 50-60% based on literature
  - Decision rule: Pure threshold only, no other factors
  - Job priority: Same as adaptive scheduler

  **Deliverable:** Formal specification of baseline scheduler.

  ---

  ## Phase 6: Success Metrics Definition (1 hour)

  **Objective:** Specify precise formulas and measurement procedures for all success criteria.

  **Steps:**
  1. Completion time variance reduction (target: 20%+):
     - Search for variance/variability metrics in scheduling papers
     - Decide: Coefficient of variation σ/μ or other normalized metric?
     - Specify: How to aggregate across job batch sizes
     - Justify: Why 20% is a meaningful threshold

  2. Foreground latency improvement (target: 10%+):
     - Search for p95, p99 latency as SLO metrics in literature
     - Decide: p50 vs. p95 vs. p99? (p95 is industry standard)
     - Specify: Latency under adaptive vs. baseline
     - Define: "Improvement" = (baseline - adaptive) / baseline * 100%

  3. Entropy-safety correlation (target: r > 0.7):
     - Search for Pearson vs. Spearman correlation in scheduling literature
     - Decide: Correlation between entropy samples and scheduling outcomes
     - Specify: What counts as "outcome"? (foreground latency impact? completion delay?)
     - Ensure: Sufficient samples for correlation (n ≥ 30-50)

  4. False positive rate definition:
     - Define: Scheduling at time t, then load jumps >X% within Y seconds
     - Typical thresholds: >10-20% jump in 2-5 second window
     - Count false positives: % of schedules followed by immediate spike
     - Target: Lower is better; baseline is comparison point

  5. Statistical significance:
     - Minimum trials/samples: 50-100 runs per scheduler
     - Confidence intervals: 95% CI around mean metrics
     - Hypothesis tests: t-test for latency, Fisher z-test for correlation

  **Decisions to Make:**
  - Variance metric: σ/μ (coefficient of variation)
  - Foreground latency: p95 latency percentile
  - Correlation method: Pearson r over windowed entropy-outcome pairs
  - False positive window: 5-second lookahead, >15% spike threshold

  **Deliverable:** Precise metric definitions with formulas and success thresholds.

  ---

  ## Phase 7: Related Work Verification & Novelty (1.5 hours)

  **Objective:** Confirm that entropy-adaptive + momentum-based dispatch are genuinely novel.

  **Steps:**
  1. Fetch and carefully read the four hypothesis-cited papers:
     - 2511.11628 (Mixture-of-Schedulers): Does it use entropy? How does it route to expert schedulers?
     - 3673038.3673135 (PREACT): Uses QPS prediction, not entropy. What is the exact adaptation signal?
     - 2606.02982 (DriftSched): GPU inference, uses token drift. Different substrate/signal.
     - 2601.19624 (RL entropy): Exploration policy in RL, not CPU load scheduling.

  2. Document exact differentiation:
     - Mixture-of-Schedulers: Routes based on WORKLOAD TYPE, not LOAD ENTROPY → Novel
     - PREACT: Predicts QPS at data center scale, not single-machine load entropy → Novel
     - DriftSched: GPU-specific, token-drift signal, not CPU entropy → Novel
     - RL entropy: Exploration tuning, not resource allocation → Novel

  3. Cross-check for entropy + momentum combination:
     - Search: "Entropy scheduling" (last 3 years)
     - Search: "Momentum dispatch" or "gradient-based scheduling"
     - Confirm: No existing system combines entropy threshold adaptation + momentum-based timing

  4. Document positioning summary:
     - Core novelty: Entropy-driven threshold adaptation is new to this domain
     - Secondary novelty: Momentum/gradient-based dispatch timing within entropy zones
     - Contribution: Combines information theory (entropy) + control systems (momentum) for background jobs

  **Deliverable:** Related work summary confirming novelty, including differentiators for each cited paper.

  ---

  ## Final Synthesis & JSON Output (30 minutes)

  **Steps:**
  1. Consolidate all findings into structured JSON with:
     - Entropy estimator design (window, bins, formula, rationale)
     - Momentum estimator design (method, smoothing, threshold)
     - Adaptive threshold formula (functional form, parameters, interpretation)
     - Baseline scheduler specification (threshold, rule, priority mechanism)
     - Success metrics (precise definitions, formulas, targets)
     - Novelty summary (what's novel vs. related work)

  2. Validate consistency:
     - Entropy normalization matches bin count
     - Threshold formula parameters are in same units
     - Metrics can all be measured from synthetic workload
     - Success criteria are realistic but ambitious

  3. Generate follow-up questions:
     - Are there open questions for the executor/designer?
     - Should momentum-based dispatch use weighted history or single sample?
     - How to handle entropy initialization (cold start)?
     - Is entropy discretization or continuous distribution better?

  **Deliverable:** research_out.json with complete design specification.
explanation: >-
  This research establishes all design parameters needed for the executor to implement and test the entropy-adaptive scheduler.
  The hypothesis claims that adapting CPU scheduling thresholds based on load entropy (unpredictability) and prioritizing
  negative load momentum will improve both background job completion time and foreground latency under bursty workloads. To
  test this properly, we must first specify: (1) how to measure entropy from CPU load samples, (2) how to estimate momentum/load
  trends, (3) the exact formula mapping entropy to scheduling limits, (4) what baseline scheduler to compare against, and
  (5) precise success metrics to validate the hypothesis. Literature review on adaptive scheduling, load monitoring, entropy
  estimation, and control systems informs these design choices. Without these specifications, the executor cannot implement
  the system credibly or measure success rigorously.
</artifact_plan>

<investigation_process>
1. DIVERGE: Brainstorm multiple angles/framings of the question before searching. Think across fields — what adjacent domains might have relevant insights?
2. SEARCH: Multiple queries per angle with different phrasings to discover the landscape
3. FETCH: Read promising URLs at high level. Snippets are NOT enough — fetch full pages
4. DETAIL: aii-web-tools fetch_grep for specifics from key pages/PDFs
5. CONTRAST: Actively try to disprove your emerging conclusions. Search with different phrasings, "[topic] criticism", "[topic] limitations". Check across fields — the same finding may exist under different names
6. SYNTHESIZE: Integrate into balanced conclusion
7. ITERATE: Expect to repeat steps 2-6 if findings are incomplete or one-sided. Don't settle on first results
8. SUMMARIZE: Output JSON must include 'title' and 'summary' fields
</investigation_process>

<output_requirements>
- Write research_out.json to your workspace with all findings
- Provide your finding as clear prose WITH NUMBERED CITATIONS
- EVERY factual claim must have a citation number in brackets: [1], [2], [1, 3], etc.
- Include BOTH supporting AND contradicting evidence
- Be explicit about confidence level and what would change it
- End with follow-up questions for further investigation
</output_requirements>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

Research everything specified in the artifact plan, but you may also investigate additional relevant aspects beyond what's listed. Investigate this question thoroughly.

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ResearchExpectedFiles": {
      "description": "All expected output files from research artifact.",
      "properties": {
        "output": {
          "description": "Path to research output JSON. Example: 'research_out.json'",
          "title": "Output",
          "type": "string"
        }
      },
      "required": [
        "output"
      ],
      "title": "ResearchExpectedFiles",
      "type": "object"
    },
    "Source": {
      "description": "A source used in the research.",
      "properties": {
        "index": {
          "description": "Citation number (1, 2, 3, ...)",
          "title": "Index",
          "type": "integer"
        },
        "url": {
          "description": "Full URL of the source",
          "title": "Url",
          "type": "string"
        },
        "title": {
          "description": "Title of the article/page",
          "title": "Title",
          "type": "string"
        },
        "summary": {
          "description": "Brief summary of what this source contributed",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "index",
        "url",
        "title",
        "summary"
      ],
      "title": "Source",
      "type": "object"
    }
  },
  "description": "Research artifact \u2014 structured output + file metadata.\n\nConducts thorough web research using the aii-web-tools skill.\nReturns structured JSON output with citations.",
  "properties": {
    "title": {
      "default": "",
      "description": "Artifact title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); describe the content, not a status.",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "layman_summary": {
      "default": "",
      "description": "One-sentence plain-language summary of what this artifact does, accessible to non-experts. Used only in the per-artifact README, not in downstream prompts.",
      "maxLength": 250,
      "minLength": 80,
      "title": "Layman Summary",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Summary for downstream artifacts: what this artifact provides",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/ResearchExpectedFiles",
      "description": "All output files you created. Must include research_out.json with your research findings."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    },
    "answer": {
      "description": "Comprehensive answer with NUMBERED CITATIONS. Cite sources by number: 'Claim [1].' or 'According to [2, 3]...'",
      "title": "Answer",
      "type": "string"
    },
    "sources": {
      "description": "All sources used, with index matching citation numbers in answer",
      "items": {
        "$ref": "#/$defs/Source"
      },
      "title": "Sources",
      "type": "array"
    },
    "follow_up_questions": {
      "description": "2-3 follow-up questions that emerged from the investigation",
      "items": {
        "type": "string"
      },
      "title": "Follow Up Questions",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files",
    "answer",
    "sources",
    "follow_up_questions"
  ],
  "title": "ResearchArtifact",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-08-24 10:54:40 UTC

```
Find a better heuristic for scheduling background jobs on a machine with bursty CPU load.
```

### [3] SKILL-INPUT — aii-web-tools · 2026-08-24 10:54:46 UTC

The agent loaded the **aii-web-tools** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-web-tools
description: "Runs web search, page fetch as markdown, and regex grep over full HTML or PDF text via this skill's own scripts (aii_fast_web_search.py, aii_fast_web_fetch.py) — a free-first keyless search stack with Serper fallback that works even where built-in WebSearch and WebFetch are absent. Use when a query, page, or paper must be searched, read, or mined for an exact quote, number, table value, or methodology sentence, and whenever a lossy summary would lose the detail. Triggers: web search, scholarly search, OpenAlex, Crossref, Serper, fetch a URL as markdown, read a PDF, arXiv, regex grep a page, exact quote, table value, citation check. NOT for: planning a broad multi-source literature review or mass verification campaign — use aii-web-research-tools; NOT for a PDF file already on disk — extraction, form filling, merging and PDF creation are anthropic-pdf; NOT for driving a browser or testing a UI."
---

## Web tools

You have three web capabilities: **search**, **fetch**, and **grep** (exact
regex extraction over a full page or PDF).

**Pick where they come from, in this order:**

1. **If you have built-in `WebSearch` / `WebFetch` tools, PREFER those over the
   scripts below.** They may be **deferred tools** (listed by name but with
   schemas not yet loaded) — if so, call `ToolSearch("select:WebSearch,WebFetch")`
   ONCE to load them, then use them normally. Do not skip them just because they
   need that one extra load step; they are the preferred path. Pair them with the
   `aii_web_tools__fetch_grep` script below when you need exact text / numbers /
   methodology that a summary would miss, or when reading a PDF.
2. **Only if you have NO built-in `WebSearch` / `WebFetch`** (e.g. the OpenHands
   backend), use the scripts in this skill (below). They are our own
   implementations — free-first web search (keyless general/scholarly engines,
   Serper fallback), html2text + PyMuPDF for fetch, and regex grep over the full
   document text. They work without any built-in web tools.

Workflow either way: **search** (discover) → **fetch** (read for the gist) →
**grep** (pull exact details / read PDFs).

---

## Running the scripts

Run every script with the skill's pre-provisioned interpreter (it already has
`requests`, `html2text`, `pymupdf`, `python-dotenv`). Set `PY` once:

```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-web-tools"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

### 1. Search the web (free-first: general or scholarly)

```bash
# general web (default): keyless engines (ddgs, marginalia); Serper only if they miss
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "neuro-symbolic FOL translation LLM" --max-results 10
# scholarly mode: OpenAlex + Crossref (DOIs, citation counts)
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "neuro-symbolic FOL translation" --mode scholarly
```

Returns ranked title / URL / snippet lines. `--mode general` (default) uses
keyless general engines; `--mode scholarly` uses academic APIs. Both fall back
to Serper (paid) only when the free engines miss. Use search first to scan the
landscape; snippets are for discovery only — fetch a page before judging it.

### 2. Fetch a page as markdown (HTML or PDF)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" fetch --url "https://arxiv.org/abs/2303.11366" --max-chars 10000
```

`--max-chars` caps output (default 10000); `--char-offset N` pages further in.
Handles PDFs transparently via PyMuPDF.

### 3. Grep a page or PDF (exact regex extraction)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" grep --url "https://arxiv.org/pdf/2303.11366" --pattern "verbal reinforcement" --max-matches 20 --context-chars 200
```

Returns only the matching sections with surrounding context — the right tool
for exact numbers, table values, methodology, or long PDFs where a summary
would lose the detail. `-i` for case-insensitive.

**Parallelize** independent searches/fetches in one turn; only sequence a
fetch after the search that produced its URL.

---

## Notes

- The scripts call our ability server. If a script prints
  `Ability service not available`, the server is down — say so rather than
  silently improvising a different search method.
- Do **not** hand-roll your own `requests`/scraping for search when these
  tools are available: Serper returns clean Google results and the fetch/grep
  scripts already handle HTML, PDFs, and encoding.
````

### [4] SYSTEM-USER prompt · 2026-08-24 10:59:34 UTC

```
<validation-feedback>
Attempt 1 failed validation.

Schema validation found 1 problem — fix ALL of them at once:
  - at `layman_summary`: 'This research provides the complete design blueprint for a smarter background job scheduler that adapts CPU limits based on how unpredictable the current workload is, improving both job completion time and responsiveness of foreground tasks under bursty loads.' is too long (at most 250 characters, got 260)
Every required field must be present and every field type must match the schema.

Produce `.terminal_claude_agent_struct_out.json` again so it contains corrected JSON that matches the schema. Do not invent new fields.
</validation-feedback>
```

### [5] SYSTEM-USER prompt · 2026-08-24 11:00:02 UTC

```
<verification_failed>
Your research output failed verification (attempt 1/10).
</verification_failed>

<schema_errors>
JSON SCHEMA ERRORS:
  - research_out.json: Missing required 'answer' field
  - research_out.json: Missing required 'follow_up_questions' field

Fix: research_out.json must have:
     {
       "answer": "comprehensive answer with [1], [2] citations",
       "sources": [{"index": 1, "url": "...", "title": "...", "summary": "..."}],
       "follow_up_questions": ["Question 1?", "Question 2?"],
       "summary": "what was found"
     }

     Each citation [N] in answer MUST match a source with that index.
</schema_errors>

<content_warnings>
CONTENT ISSUES:
  - research_out.json: 'answer' is too short
  - research_out.json: Only 0 follow-up questions (recommend 2-3)

Fix: Ensure answer is comprehensive, has proper citations, and all sources are cited.
</content_warnings>

<task>
FIX ISSUES:
1. Output valid research_out.json with all required fields
2. Ensure every factual claim has a numbered citation [1], [2], etc.
3. Ensure every source has a matching citation in the answer
</task>
```
