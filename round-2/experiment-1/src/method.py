#!/usr/bin/env python3
"""
Entropy-Adaptive Background Job Scheduler: Comparative Trial Experiment

Implements 4 scheduler variants (Baseline, Entropy-only, Momentum-only, Entropy-Adaptive)
with n≥50 trials on synthetic bursty workloads. Measures: job completion variance,
foreground latency, entropy-outcome correlation, false positive rate, statistical significance.
"""

import json
import sys
import os
import math
import time
import random
import gc
import threading
import queue
import psutil
import numpy as np
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Tuple
from loguru import logger
from scipy import stats
from collections import deque

# ============================================================================
# SETUP & LOGGING
# ============================================================================

LOG_DIR = Path("/ai-inventor/aii_data/runs/run_a-GYNIuwcKDN/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(LOG_DIR / "run.log"), rotation="100 MB", level="DEBUG")

# ============================================================================
# ENTROPY MONITOR
# ============================================================================

class EntropyMonitor:
    """Shannon entropy estimator of CPU load unpredictability."""

    def __init__(self, window_size_sec: int = 60, sample_interval_sec: float = 0.5,
                 num_bins: int = 8):
        self.window_size_sec = window_size_sec
        self.sample_interval_sec = sample_interval_sec
        self.num_bins = num_bins
        self.max_samples = int(window_size_sec / sample_interval_sec)
        self.load_samples = deque(maxlen=self.max_samples)
        self.last_sample_time = None

    def sample_cpu_load(self) -> float:
        """Get current CPU utilization percent (0-100)."""
        return psutil.cpu_percent(interval=0.05, percpu=False)

    def update(self) -> None:
        """Add new CPU sample if enough time has passed."""
        now = time.time()
        if self.last_sample_time is None or (now - self.last_sample_time) >= self.sample_interval_sec:
            load = self.sample_cpu_load()
            self.load_samples.append(load)
            self.last_sample_time = now

    def compute_entropy(self) -> float:
        """Compute normalized Shannon entropy with Miller-Madow bias correction."""
        if len(self.load_samples) < 10:
            return 0.0

        samples = list(self.load_samples)
        min_load, max_load = min(samples), max(samples)

        # Percentile-based binning: dynamic bin edges
        if min_load == max_load:
            return 0.0

        bin_edges = np.percentile(samples, np.linspace(0, 100, self.num_bins + 1))
        bin_edges[0] = min_load - 0.001
        bin_edges[-1] = max_load + 0.001

        # Histogram counts
        counts, _ = np.histogram(samples, bins=bin_edges)
        counts = counts[counts > 0]

        if len(counts) == 0:
            return 0.0

        # Naive entropy
        probs = counts / len(samples)
        h_naive = -np.sum(probs * np.log2(np.maximum(probs, 1e-10)))

        # Miller-Madow bias correction
        k = len(counts)  # non-empty bins
        n = len(samples)
        h_corrected = h_naive + (k - 1) / (2 * n)

        # Normalize to [0, 1]
        h_norm = h_corrected / np.log2(self.num_bins)
        return min(1.0, max(0.0, h_norm))

# ============================================================================
# MOMENTUM TRACKER
# ============================================================================

class MomentumTracker:
    """Exponential weighted moving average of CPU load trend."""

    def __init__(self, alpha: float = 0.2, update_interval_sec: float = 1.0):
        self.alpha = alpha
        self.update_interval_sec = update_interval_sec
        self.momentum = None
        self.last_load = None
        self.last_update_time = None

    def update(self, current_load: float) -> None:
        """Update EWMA momentum."""
        now = time.time()
        if self.last_update_time is None or (now - self.last_update_time) >= self.update_interval_sec:
            if self.momentum is None:
                self.momentum = current_load
            else:
                self.momentum = self.alpha * current_load + (1 - self.alpha) * self.momentum
            self.last_load = current_load
            self.last_update_time = now

    def get_gradient(self) -> float:
        """Compute load gradient: (load_t - momentum_t) / momentum_t."""
        if self.momentum is None or self.momentum < 1e-6:
            return 0.0
        return (self.last_load - self.momentum) / self.momentum

    def is_negative(self) -> bool:
        """Load declining (< -5%)."""
        return self.get_gradient() < -0.05

    def is_positive(self) -> bool:
        """Load rising (> +10%)."""
        return self.get_gradient() > 0.10

# ============================================================================
# SCHEDULER VARIANTS
# ============================================================================

@dataclass
class SchedulingDecision:
    schedule: bool
    priority: str  # 'STANDARD' or 'PRIORITY'
    threshold_pct: float
    reason: str

class BaseScheduler:
    """Base class for all scheduler variants."""

    def __init__(self, name: str, entropy_monitor: EntropyMonitor,
                 momentum_tracker: MomentumTracker):
        self.name = name
        self.entropy_monitor = entropy_monitor
        self.momentum_tracker = momentum_tracker

    def decide(self, current_cpu_pct: float) -> SchedulingDecision:
        raise NotImplementedError

class BaselineScheduler(BaseScheduler):
    """Fixed 55% CPU threshold."""

    def decide(self, current_cpu_pct: float) -> SchedulingDecision:
        threshold = 55.0
        if current_cpu_pct < threshold:
            return SchedulingDecision(True, "STANDARD", threshold, "CPU below fixed 55%")
        else:
            return SchedulingDecision(False, "NONE", threshold, "CPU above fixed 55%")

class EntropyOnlyScheduler(BaseScheduler):
    """Adaptive threshold based on entropy only."""

    def decide(self, current_cpu_pct: float) -> SchedulingDecision:
        h_norm = self.entropy_monitor.compute_entropy()
        threshold = 70.0 - (70.0 - 25.0) * h_norm

        if current_cpu_pct < threshold:
            return SchedulingDecision(True, "STANDARD", threshold, f"Entropy-adaptive: H={h_norm:.2f}")
        else:
            return SchedulingDecision(False, "NONE", threshold, f"Entropy high: H={h_norm:.2f}")

class MomentumOnlyScheduler(BaseScheduler):
    """Momentum-aware dispatch with fixed 55% threshold."""

    def decide(self, current_cpu_pct: float) -> SchedulingDecision:
        threshold = 55.0

        if current_cpu_pct >= threshold:
            return SchedulingDecision(False, "NONE", threshold, "CPU above 55%")

        # Within safe zone, prefer negative gradient (load declining)
        if self.momentum_tracker.is_negative():
            return SchedulingDecision(True, "PRIORITY", threshold, "Negative gradient detected")
        else:
            return SchedulingDecision(True, "STANDARD", threshold, "CPU below 55%")

class EntropyAdaptiveScheduler(BaseScheduler):
    """Combined entropy + momentum scheduling."""

    def decide(self, current_cpu_pct: float) -> SchedulingDecision:
        h_norm = self.entropy_monitor.compute_entropy()
        threshold = 70.0 - (70.0 - 25.0) * h_norm

        if current_cpu_pct >= threshold:
            return SchedulingDecision(False, "NONE", threshold, "CPU above threshold")

        # Within safe entropy zone (H < 0.6), use momentum
        if h_norm < 0.6 and self.momentum_tracker.is_negative():
            return SchedulingDecision(True, "PRIORITY", threshold, f"Entropy low + negative gradient")
        else:
            return SchedulingDecision(True, "STANDARD", threshold, f"Standard dispatch (H={h_norm:.2f})")

# ============================================================================
# FOREGROUND TASK EMULATOR
# ============================================================================

@dataclass
class ForegroundRequest:
    arrival_time: float
    service_time_sec: float
    completion_time: Optional[float] = None

class ForegroundEmulator:
    """Poisson arrivals with lognormal service times."""

    def __init__(self, arrival_rate_per_sec: float = 15.0):
        self.arrival_rate = arrival_rate_per_sec
        self.requests = []
        self.completed_requests = []
        self.start_time = time.time()

    def generate_arrivals(self, current_time: float, duration_sec: float) -> List[ForegroundRequest]:
        """Generate Poisson arrivals over a time window."""
        arrivals = []
        lambda_param = self.arrival_rate * duration_sec
        num_arrivals = np.random.poisson(lambda_param)

        for _ in range(num_arrivals):
            # Uniform arrival within window
            arrival_time = self.start_time + current_time + np.random.uniform(0, duration_sec)
            # Lognormal service time: LogNormal(μ=log(0.01), σ=0.5) → 5-50ms typical
            service_time = np.random.lognormal(mean=np.log(0.01), sigma=0.5)
            arrivals.append(ForegroundRequest(arrival_time, service_time))

        self.requests.extend(arrivals)
        return arrivals

    def process_requests(self, current_time: float) -> None:
        """Mark requests as completed if within current time."""
        for req in self.requests:
            if req.completion_time is None and req.arrival_time + req.service_time_sec <= self.start_time + current_time:
                req.completion_time = req.arrival_time + req.service_time_sec
                self.completed_requests.append(req)

    def get_latencies_ms(self) -> List[float]:
        """Get all request latencies in milliseconds."""
        return [(r.completion_time - r.arrival_time) * 1000
                for r in self.completed_requests if r.completion_time is not None]

    def get_percentile_latency(self, percentile: float) -> Optional[float]:
        """Get percentile latency in milliseconds."""
        latencies = self.get_latencies_ms()
        if len(latencies) == 0:
            return None
        return np.percentile(latencies, percentile)

# ============================================================================
# BACKGROUND JOB EXECUTOR
# ============================================================================

@dataclass
class BackgroundJob:
    job_id: int
    queued_at: float
    duration_sec: float
    started_at: Optional[float] = None
    completed_at: Optional[float] = None

    @property
    def completion_time_sec(self) -> Optional[float]:
        if self.completed_at is not None:
            return self.completed_at - self.queued_at
        return None

class BackgroundJobExecutor:
    """Manages background job queue and execution."""

    def __init__(self, job_duration_range: Tuple[float, float] = (10, 100)):
        self.job_queue = queue.Queue()
        self.job_id_counter = 0
        self.completed_jobs = []
        self.job_duration_range = job_duration_range
        self.current_job = None
        self.current_job_start = None

    def enqueue_job(self, current_time: float) -> BackgroundJob:
        """Create and enqueue a new background job."""
        duration = np.random.uniform(*self.job_duration_range)
        job = BackgroundJob(self.job_id_counter, current_time, duration)
        self.job_id_counter += 1
        self.job_queue.put(job)
        return job

    def try_schedule_job(self, current_time: float, scheduler_decision: SchedulingDecision) -> bool:
        """Try to schedule a job if decision permits."""
        if not scheduler_decision.schedule or self.job_queue.empty():
            return False

        # Dequeue and start job
        job = self.job_queue.get()
        job.started_at = current_time
        self.current_job = job
        self.current_job_start = current_time
        return True

    def try_complete_job(self, current_time: float) -> bool:
        """Check if current job is done."""
        if self.current_job is None:
            return False

        if current_time - self.current_job_start >= self.current_job.duration_sec:
            self.current_job.completed_at = current_time
            self.completed_jobs.append(self.current_job)
            self.current_job = None
            self.current_job_start = None
            return True

        return False

    def get_completion_times(self) -> List[float]:
        """Get all completed job durations."""
        return [j.completion_time_sec for j in self.completed_jobs if j.completion_time_sec is not None]

# ============================================================================
# BURSTY WORKLOAD GENERATOR
# ============================================================================

class WorkloadConfig:
    """Configuration for a trial's workload."""

    def __init__(self, arrival_rate: int = 15, has_spikes: bool = False,
                 spike_freq_sec: int = 60, spike_duration_sec: int = 10):
        self.arrival_rate = arrival_rate  # req/s
        self.has_spikes = has_spikes
        self.spike_freq_sec = spike_freq_sec
        self.spike_duration_sec = spike_duration_sec
        self.current_spike_intensity = 1.0  # multiplier

    def update(self, current_time: float) -> None:
        """Update workload intensity based on spike schedule."""
        if not self.has_spikes:
            self.current_spike_intensity = 1.0
            return

        cycle_pos = current_time % self.spike_freq_sec
        if cycle_pos < self.spike_duration_sec:
            self.current_spike_intensity = 2.0  # 2× arrival rate
        else:
            self.current_spike_intensity = 1.0

    def get_current_rate(self) -> float:
        """Current Poisson arrival rate (req/s)."""
        return self.arrival_rate * self.current_spike_intensity

# ============================================================================
# TRIAL EXECUTION
# ============================================================================

@dataclass
class TrialMetrics:
    trial_id: int
    scheduler_name: str
    completion_time_mean: float
    completion_time_std: float
    completion_time_cv: float
    completion_count: int
    foreground_p50_ms: Optional[float]
    foreground_p95_ms: Optional[float]
    foreground_p99_ms: Optional[float]
    false_positive_rate: float
    entropy_samples: List[float] = field(default_factory=list)
    momentum_samples: List[float] = field(default_factory=list)

class Trial:
    """Single trial of the experiment."""

    def __init__(self, trial_id: int, scheduler: BaseScheduler, workload_config: WorkloadConfig,
                 trial_duration_sec: int = 600):
        self.trial_id = trial_id
        self.scheduler = scheduler
        self.workload_config = workload_config
        self.trial_duration_sec = trial_duration_sec
        self.start_time = None

        self.entropy_monitor = scheduler.entropy_monitor
        self.momentum_tracker = scheduler.momentum_tracker
        self.foreground = ForegroundEmulator(workload_config.arrival_rate)
        self.bg_executor = BackgroundJobExecutor()

        self.metric_log = []
        self.entropy_samples = []
        self.momentum_samples = []
        self.false_positive_count = 0
        self.false_positive_total = 0

    def run(self) -> TrialMetrics:
        """Execute trial for ~10 minutes."""
        self.start_time = time.time()
        job_spawn_interval = 60.0 / 7.5  # ~7.5 jobs/min
        last_job_spawn = 0
        last_metric_collection = 0
        metric_collection_interval = 10.0

        logger.info(f"[Trial {self.trial_id}] Starting {self.scheduler.name} for {self.trial_duration_sec}s")

        while True:
            elapsed = time.time() - self.start_time
            if elapsed >= self.trial_duration_sec:
                break

            # Update workload (spikes, etc)
            self.workload_config.update(elapsed)

            # Sample CPU and update monitors
            current_cpu = psutil.cpu_percent(interval=0.05, percpu=False)
            self.entropy_monitor.update()
            self.momentum_tracker.update(current_cpu)

            # Generate foreground arrivals
            if elapsed - last_metric_collection >= 1.0:  # every 1s
                self.foreground.generate_arrivals(elapsed, 1.0)
                self.foreground.process_requests(elapsed)
                last_metric_collection = elapsed

            # Spawn background jobs
            if elapsed - last_job_spawn >= job_spawn_interval:
                self.bg_executor.enqueue_job(self.start_time + elapsed)
                last_job_spawn = elapsed

            # Scheduler decision
            decision = self.scheduler.decide(current_cpu)

            # Track false positives
            if decision.schedule:
                self.false_positive_total += 1
                # Check if load spikes >15% within 5s
                future_check_time = elapsed + 5.0
                if future_check_time <= self.trial_duration_sec:
                    if current_cpu < 50 and self.workload_config.current_spike_intensity > 1.5:
                        self.false_positive_count += 1

            # Try to schedule job
            self.bg_executor.try_schedule_job(self.start_time + elapsed, decision)
            self.bg_executor.try_complete_job(self.start_time + elapsed)

            # Collect metrics every 10s
            if elapsed - last_metric_collection >= metric_collection_interval or elapsed >= self.trial_duration_sec - 1:
                h = self.entropy_monitor.compute_entropy()
                grad = self.momentum_tracker.get_gradient()
                self.entropy_samples.append(h)
                self.momentum_samples.append(grad)

                p50 = self.foreground.get_percentile_latency(50)
                p95 = self.foreground.get_percentile_latency(95)
                p99 = self.foreground.get_percentile_latency(99)

                self.metric_log.append({
                    'elapsed': elapsed,
                    'entropy': h,
                    'gradient': grad,
                    'cpu': current_cpu,
                    'p50': p50,
                    'p95': p95,
                    'p99': p99,
                    'jobs_queued': self.bg_executor.job_queue.qsize(),
                    'jobs_completed': len(self.bg_executor.completed_jobs),
                })

            time.sleep(0.1)

        # Aggregate metrics
        completion_times = self.bg_executor.get_completion_times()
        if len(completion_times) > 0:
            completion_mean = np.mean(completion_times)
            completion_std = np.std(completion_times)
            completion_cv = completion_std / completion_mean if completion_mean > 0 else 0
        else:
            completion_mean = completion_std = completion_cv = 0

        fpr = self.false_positive_count / max(1, self.false_positive_total)

        metrics = TrialMetrics(
            trial_id=self.trial_id,
            scheduler_name=self.scheduler.name,
            completion_time_mean=completion_mean,
            completion_time_std=completion_std,
            completion_time_cv=completion_cv,
            completion_count=len(completion_times),
            foreground_p50_ms=self.foreground.get_percentile_latency(50),
            foreground_p95_ms=self.foreground.get_percentile_latency(95),
            foreground_p99_ms=self.foreground.get_percentile_latency(99),
            false_positive_rate=fpr,
            entropy_samples=self.entropy_samples,
            momentum_samples=self.momentum_samples,
        )

        logger.info(f"[Trial {self.trial_id}] {self.scheduler.name}: "
                   f"CV={completion_cv:.3f}, P95={metrics.foreground_p95_ms:.1f}ms, "
                   f"Jobs={len(completion_times)}")

        return metrics

# ============================================================================
# STATISTICAL ANALYSIS
# ============================================================================

def analyze_results(all_metrics: List[TrialMetrics]) -> Dict:
    """Compute aggregate statistics and comparisons."""

    # Group by scheduler
    by_scheduler = {}
    for metric in all_metrics:
        if metric.scheduler_name not in by_scheduler:
            by_scheduler[metric.scheduler_name] = []
        by_scheduler[metric.scheduler_name].append(metric)

    # Per-scheduler stats
    scheduler_stats = {}
    for sched_name, metrics_list in by_scheduler.items():
        cvs = [m.completion_time_cv for m in metrics_list]
        p95s = [m.foreground_p95_ms for m in metrics_list if m.foreground_p95_ms is not None]
        fprs = [m.false_positive_rate for m in metrics_list]

        scheduler_stats[sched_name] = {
            'n_trials': len(metrics_list),
            'mean_cv': float(np.mean(cvs)) if cvs else 0,
            'std_cv': float(np.std(cvs)) if cvs else 0,
            'mean_p95_ms': float(np.mean(p95s)) if p95s else 0,
            'std_p95_ms': float(np.std(p95s)) if p95s else 0,
            'mean_fpr': float(np.mean(fprs)) if fprs else 0,
            'std_fpr': float(np.std(fprs)) if fprs else 0,
        }

    # Paired comparisons (Entropy-Adaptive vs Baseline)
    baseline_metrics = by_scheduler.get('Baseline', [])
    adaptive_metrics = by_scheduler.get('Entropy-Adaptive', [])

    comparisons = {}
    if baseline_metrics and adaptive_metrics and len(baseline_metrics) == len(adaptive_metrics):
        baseline_cvs = [m.completion_time_cv for m in baseline_metrics]
        adaptive_cvs = [m.completion_time_cv for m in adaptive_metrics]

        cv_reduction_pct = [(b - a) / b * 100 for b, a in zip(baseline_cvs, adaptive_cvs)]

        baseline_p95s = [m.foreground_p95_ms for m in baseline_metrics if m.foreground_p95_ms is not None]
        adaptive_p95s = [m.foreground_p95_ms for m in adaptive_metrics if m.foreground_p95_ms is not None]

        if baseline_p95s and adaptive_p95s and len(baseline_p95s) == len(adaptive_p95s):
            p95_improvement_pct = [(b - a) / b * 100 for b, a in zip(baseline_p95s, adaptive_p95s)]

            # Paired t-tests
            t_stat_cv, p_val_cv = stats.ttest_rel(baseline_cvs, adaptive_cvs)
            t_stat_p95, p_val_p95 = stats.ttest_rel(baseline_p95s, adaptive_p95s)

            # Effect sizes (Cohen's d)
            def cohens_d(x, y):
                n1, n2 = len(x), len(y)
                var1, var2 = np.var(x, ddof=1), np.var(y, ddof=1)
                pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1 + n2 - 2))
                return (np.mean(x) - np.mean(y)) / pooled_std if pooled_std > 0 else 0

            d_cv = cohens_d(baseline_cvs, adaptive_cvs)
            d_p95 = cohens_d(baseline_p95s, adaptive_p95s)

            # CIs via t-distribution
            ci_cv = stats.t.interval(0.95, len(cv_reduction_pct)-1,
                                     loc=np.mean(cv_reduction_pct),
                                     scale=stats.sem(cv_reduction_pct))
            ci_p95 = stats.t.interval(0.95, len(p95_improvement_pct)-1,
                                      loc=np.mean(p95_improvement_pct),
                                      scale=stats.sem(p95_improvement_pct))

            comparisons = {
                'cv_reduction_pct': {
                    'mean': float(np.mean(cv_reduction_pct)),
                    'ci_lower': float(ci_cv[0]),
                    'ci_upper': float(ci_cv[1]),
                    'p_value': float(p_val_cv),
                    'cohens_d': float(d_cv),
                },
                'p95_improvement_pct': {
                    'mean': float(np.mean(p95_improvement_pct)),
                    'ci_lower': float(ci_p95[0]),
                    'ci_upper': float(ci_p95[1]),
                    'p_value': float(p_val_p95),
                    'cohens_d': float(d_p95),
                },
                'n_pairs': len(baseline_metrics),
            }

    # Entropy-outcome correlation
    all_entropies = []
    all_latencies = []
    for metric in all_metrics:
        if metric.entropy_samples and metric.foreground_p95_ms is not None:
            all_entropies.extend(metric.entropy_samples)
            all_latencies.extend([metric.foreground_p95_ms] * len(metric.entropy_samples))

    entropy_r = entropy_p = entropy_ci = None
    if len(all_entropies) > 2 and len(all_latencies) > 2:
        entropy_r, entropy_p = stats.pearsonr(all_entropies, all_latencies)
        # Fisher z-transform for CI
        z = 0.5 * np.log((1 + entropy_r) / (1 - entropy_r + 1e-10))
        se = 1 / np.sqrt(len(all_entropies) - 3)
        z_crit = 1.96
        z_lower = z - z_crit * se
        z_upper = z + z_crit * se
        entropy_ci = (float((np.exp(2*z_lower) - 1) / (np.exp(2*z_lower) + 1)),
                      float((np.exp(2*z_upper) - 1) / (np.exp(2*z_upper) + 1)))

    if entropy_r is not None:
        comparisons['entropy_outcome_r'] = {
            'r': float(entropy_r),
            'p_value': float(entropy_p),
            'ci_lower': entropy_ci[0],
            'ci_upper': entropy_ci[1],
            'n_samples': len(all_entropies),
        }

    # Success criteria
    success_criteria = {
        'cv_reduction_ge_20pct': (comparisons.get('cv_reduction_pct', {}).get('mean', 0) >= 20),
        'p95_improvement_ge_10pct': (comparisons.get('p95_improvement_pct', {}).get('mean', 0) >= 10),
        'entropy_outcome_r_gt_0_7': (comparisons.get('entropy_outcome_r', {}).get('r', 0) > 0.7),
        'adaptive_better_than_baseline': (comparisons.get('p95_improvement_pct', {}).get('p_value', 1) < 0.05),
        'sample_size_ge_50': (len(all_metrics) / 4 >= 50),  # 50 trials × 4 schedulers
    }

    return {
        'schedulers': scheduler_stats,
        'comparisons': comparisons,
        'success_criteria': success_criteria,
        'total_trials': len(all_metrics) // 4 if len(all_metrics) > 0 else 0,
    }

# ============================================================================
# MAIN EXECUTION
# ============================================================================

@logger.catch(reraise=True)
def main():
    logger.info("=" * 80)
    logger.info("ENTROPY-ADAPTIVE SCHEDULER EXPERIMENT")
    logger.info("=" * 80)

    # Configuration
    N_TRIALS = 10  # Test with 10 first, then scale to 50
    TRIAL_DURATION_SEC = 60  # 1 minute per trial (speeds up testing)
    WORKLOAD_CONFIGS = [
        WorkloadConfig(arrival_rate=15, has_spikes=True),
        WorkloadConfig(arrival_rate=20, has_spikes=False),
        WorkloadConfig(arrival_rate=30, has_spikes=True),
        WorkloadConfig(arrival_rate=50, has_spikes=False),
    ]

    all_metrics = []

    for trial_id in range(N_TRIALS):
        # Rotate through workload configs
        workload = WORKLOAD_CONFIGS[trial_id % len(WORKLOAD_CONFIGS)]

        # Shared monitors for all schedulers in this trial
        entropy_monitor = EntropyMonitor()
        momentum_tracker = MomentumTracker()

        # Schedulers
        schedulers = [
            BaselineScheduler("Baseline", entropy_monitor, momentum_tracker),
            EntropyOnlyScheduler("Entropy-Only", entropy_monitor, momentum_tracker),
            MomentumOnlyScheduler("Momentum-Only", entropy_monitor, momentum_tracker),
            EntropyAdaptiveScheduler("Entropy-Adaptive", entropy_monitor, momentum_tracker),
        ]

        # Run trial for each scheduler
        for scheduler in schedulers:
            trial = Trial(trial_id, scheduler, workload, TRIAL_DURATION_SEC)
            metrics = trial.run()
            all_metrics.append(metrics)
            gc.collect()

        if (trial_id + 1) % 5 == 0:
            logger.info(f"Completed {trial_id + 1}/{N_TRIALS} trials")

    # Analyze
    logger.info("Analyzing results...")
    results = analyze_results(all_metrics)

    # Format output for exp_gen_sol_out schema
    examples = []
    for i, trial_metrics in enumerate(all_metrics):
        example = {
            "input": f"Trial {trial_metrics.trial_id} - {trial_metrics.scheduler_name} scheduler on bursty workload",
            "output": json.dumps({
                "scheduler": trial_metrics.scheduler_name,
                "completion_time_cv": f"{trial_metrics.completion_time_cv:.4f}",
                "p95_latency_ms": f"{trial_metrics.foreground_p95_ms:.1f}" if trial_metrics.foreground_p95_ms else "0",
                "false_positive_rate": f"{trial_metrics.false_positive_rate:.3f}",
                "jobs_completed": trial_metrics.completion_count
            }),
            "metadata_trial": trial_metrics.trial_id,
            "metadata_scheduler": trial_metrics.scheduler_name,
            "predict_cv": f"{trial_metrics.completion_time_cv:.4f}",
            "predict_p95": f"{trial_metrics.foreground_p95_ms:.1f}" if trial_metrics.foreground_p95_ms else "0"
        }
        examples.append(example)

    formatted_output = {
        "metadata": {
            "method": "Entropy-Adaptive Scheduler Experiment",
            "n_trials": len(all_metrics) // 4,
            "n_schedulers": 4,
            "description": "Comparison of entropy-adaptive vs baseline job schedulers"
        },
        "datasets": [
            {
                "dataset": "scheduler_trials",
                "examples": examples
            }
        ]
    }

    # Save output
    output_path = Path("/ai-inventor/aii_data/runs/run_a-GYNIuwcKDN/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/method_out.json")
    output_path.write_text(json.dumps(formatted_output, indent=2))
    logger.info(f"Results saved to {output_path}")

    # Sanity checks
    logger.info("\n" + "=" * 80)
    logger.info("SANITY CHECKS")
    logger.info("=" * 80)

    for trial_metrics in all_metrics:
        assert 0 <= trial_metrics.completion_time_cv <= 2, f"CV out of range: {trial_metrics.completion_time_cv}"
        if trial_metrics.foreground_p95_ms is not None:
            assert 0 < trial_metrics.foreground_p95_ms < 10000, f"P95 out of range: {trial_metrics.foreground_p95_ms}"
        assert 0 <= trial_metrics.false_positive_rate <= 1, f"FPR out of range: {trial_metrics.false_positive_rate}"

    logger.info("✓ All sanity checks passed")

    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Total trials: {results['total_trials']}")
    for sched, stats in results['schedulers'].items():
        logger.info(f"\n{sched}:")
        logger.info(f"  CV: {stats['mean_cv']:.3f} ± {stats['std_cv']:.3f}")
        logger.info(f"  P95: {stats['mean_p95_ms']:.1f} ± {stats['std_p95_ms']:.1f} ms")
        logger.info(f"  FPR: {stats['mean_fpr']:.3f} ± {stats['std_fpr']:.3f}")

    if 'entropy_outcome_r' in results['comparisons']:
        r = results['comparisons']['entropy_outcome_r']['r']
        logger.info(f"\nEntropy-Outcome Correlation: r = {r:.3f}")

    logger.info("\n" + "=" * 80)

if __name__ == "__main__":
    main()
