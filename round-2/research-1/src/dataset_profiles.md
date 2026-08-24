# Real-World Workload Dataset Profiles

## Summary Table

| Dataset | Source | Duration | Scale | Format | Size (Comp) | Granularity | Access | Quality Notes |
|---------|--------|----------|-------|--------|------------|-------------|--------|----------------|
| **Azure V2** | Microsoft Research | 30 days | 2.7M VMs | CSV | 156GB | 5-min | GitHub Blob Storage | Well-documented, no known gaps |
| **Azure V1** | Microsoft Research | 30 days | 2M VMs | CSV | 78.5GB | 5-min | GitHub Blob Storage | Complete schema, legacy |
| **Alibaba 2018** | Alibaba | 8 days | 4k machines | CSV | 49GB | 300-sec | Survey-gated | Heavy-tail bursts, known gaps [60K-89K] seconds |
| **Alibaba 2017** | Alibaba | 24 hours | 1.3k machines | CSV | — | 300-sec | Survey-gated | Shorter trace, co-location effects |
| **Google 2011** | Google | 29 days | 12.5k machines | Binary/text | 41GB | 5-min + 1-sec sample | Google Cloud Storage | Disk data only 14 days, <1% missing usage |
| **Google 2019** | Google | 31 days | 8 clusters | BigQuery | 2.4TB | 5-min histograms | Google BigQuery | Largest scale, requires BigQuery access |
| **Wikipedia Clicks** | Wikimedia | Monthly | — | TSV | ~GB/month | — | Public download | Request rate proxy, not CPU direct |

---

## AZURE VM TRACES V2 (Recommended for initial validation)

**Publication**: Microsoft Research  
**Repository**: https://github.com/Azure/AzurePublicDataset  
**Download Links**: Available in `AzurePublicDatasetLinksV2.txt`  
**Citation**: "Resource Central: Understanding and Predicting Workloads for Improved Resource Management in Large Cloud Platforms" (SOSP'17)

### Key Characteristics
- **Duration**: 30 consecutive days (fixed period: one geographical region)
- **Scale**: 2,695,548 VMs, 6,687 subscriptions
- **Total Readings**: 1,942,780,023 CPU utilization readings (1.9B)
- **Total VM-hours**: 104,371,713
- **Total vCore-hours**: >380,000,000
- **Files**: 198 CSV files
- **Uncompressed Size**: 235GB
- **Compressed Size**: 156GB

### Schema
Column fields per VM:
1. Encrypted subscription ID
2. Encrypted deployment ID
3. Deployment-level timestamp (VM creation)
4. VM count per deployment
5. Deployment size category
6. Encrypted VM ID
7. VM creation timestamp
8. VM deletion timestamp
9. Max CPU (lifetime)
10. Avg CPU (lifetime)
11. P95 Max CPU (lifetime)
12. VM category
13. VM vCore count (bucket)
14. VM memory (bucket)
15. **Measurement timestamp (5-min intervals)**
16. **Min CPU (in 5-min window)**
17. **Avg CPU (in 5-min window)**
18. **Max CPU (in 5-min window)**
19. vCore bucket definition
20. Memory bucket definition

**Critical Columns for Entropy**: 16, 17, 18 (CPU utilization values)  
**Time Resolution**: 5-minute intervals

### Data Quality
- ✅ No known missing-data issues at aggregate level
- ✅ Encrypted for privacy (no user/application data exposed)
- ✅ Jupyter notebook available comparing to full 2019 production workload
- ✅ Well-documented schema

### Known Limitations
- 5-minute granularity (coarser than sub-minute variations)
- Normalized resource values (cannot infer raw CPU cores)
- No per-VM network or I/O metrics
- Single geographical region only

### Entropy Analysis Suitability
- **Pros**: 30-day duration captures 4+ weeks of periodicity; 2.7M VMs enable aggregation analysis; clean data with minimal missing values
- **Cons**: 5-minute granularity coarser than ideal; cannot compute sub-5-min entropy windows; large file count requires parsing overhead
- **Recommended Approach**: Aggregate 5-min samples into 60-min windows (12 consecutive samples), compute entropy per window; alternatively, use 5-min windows directly (one reading = one sample in entropy distribution)

---

## ALIBABA CLUSTER TRACES 2018 (Recommended as primary)

**Publication**: Alibaba Open Cluster Trace Program  
**Repository**: https://github.com/alibaba/clusterdata  
**Access**: Survey-gated at http://alibabadeveloper.mikecrm.com/BdJtacN (no payment)  
**Download**: bash `fetchData.sh` after survey completion

### Key Characteristics
- **Duration**: 8 consecutive days
- **Scale**: ~4,000 machines
- **Total Size**: 98GB (49GB tarball + 49GB individual files)
- **File Count**: 6 tables (each its own file)
- **Sampled From**: Alibaba production cluster (Sigma + Fuxi schedulers)

### Core Files
1. **machine_meta.csv**: Machine metadata and event log (ADD, softerror, harderror events)
2. **machine_usage.csv**: Machine resource usage with **Linux load averages (1/5/15 min)**
3. **container_meta.csv**: Online service (container) metadata
4. **container_usage.csv**: Container resource usage
5. **batch_instance.csv**: Batch job instance records
6. **batch_task.csv**: Batch job task records

### Schema (machine_usage.csv - Key for Entropy)
Column fields:
1. **timestamp** (seconds from trace start)
2. **machineID**
3. **util:CPU** (normalized 0-100)
4. **util:memory** (normalized 0-100)
5. **util:disk** (normalized 0-100)
6. **load1** (Linux 1-minute load average)
7. **load5** (Linux 5-minute load average)
8. **load15** (Linux 15-minute load average)

**Critical Columns for Entropy**: 3 (CPU utilization)  
**Time Resolution**: 300-second (5-minute) intervals  
**Measurement Duration**: 12 consecutive hours of usage data disclosed per trace period

### Data Quality
- ⚠️ **Known Issue**: ~85% of missing task_id/job_id occur in timestamp range [60K, 89K] seconds
- ⚠️ **Known Issue**: Some instance IDs in container_usage.csv missing from container_event.csv
- ⚠️ **Known Issue**: Minimal missing data in usage information for batch_instance.csv
- ✅ Heavy-tail burst patterns confirmed in literature [Cheng et al. 2018]
- ✅ Co-location effects well-documented (Sigma online scheduler + Fuxi batch scheduler interference)

### Entropy Analysis Suitability
- **Pros**: 8-day duration captures multiple daily cycles + anomalies; 4k machines enable cluster-wide analysis; confirmed heavy-tail burstiness; co-location effects visible; fine-grained container/batch separation
- **Cons**: 300-second (5-min) granularity; 12-hour usage data window per trace (not continuous); missing task IDs in mid-trace period
- **Recommended Approach**: 
  - Filter machines with ≥95% data completeness over 8 days
  - Avoid timestamp range [60K, 89K] seconds or impute using neighboring values
  - Compute entropy at 5-min window resolution (one data point = one bin entry)
  - Aggregate load5 (5-min Linux load average) across machines to compare against synthetic baselines
  - Separate online (container) vs batch workloads for comparative entropy analysis

---

## GOOGLE CLUSTER TRACE 2011 (clusterdata-2011-2)

**Publication**: Google Borg Team  
**Repository**: https://github.com/google/cluster-data  
**Mailing List**: https://groups.google.com/forum/#!forum/googleclusterdata-discuss (join required)  
**Download**: Google Cloud Storage bucket `clusterdata-2011-2` (requires gcloud SDK)  
**Documentation**: v2.1 format + schema document (Google Drive link on repository)  
**Citation**: "Large-scale cluster management at Google with Borg" (EuroSys'15)

### Key Characteristics
- **Duration**: 29 days (May 1-29, 2011, US Eastern timezone; trace timestamp starts at 600s)
- **Scale**: 12.5k-machine Borg cell
- **Total Size**: 41GB compressed
- **Sampling**: 5-minute aggregated metrics + random 1-second CPU sample per 5-min period (added in v2.1)
- **Workload Type**: Multi-purpose cluster (mix of production and best-effort jobs)

### Schema (Task Usage - Key for Entropy)
- **timestamp**: 5-minute reporting interval
- **job_id, task_index**: Job and task identifiers
- **CPU**: Number of CPUs used (not normalized)
- **memory**: Memory used in bytes
- ****disk**: Disk I/O (uncertain metric)
- **cpus_requested, memory_requested**: Requested resources
- **1-second CPU sample**: Random sample from within the 5-minute period

**Critical Columns for Entropy**: CPU (usage not normalized)  
**Time Resolution**: 5-minute aggregation with 1-second sample  
**Job Priorities**: 0-11 (0-1 free, 9-11 production, 12 monitoring)

### Data Quality
- ⚠️ **Known Issue**: Disk-time-fraction data only in first ~14 days
- ⚠️ **Known Issue**: ~0.013% of task events and ~0.0008% of job events have non-empty "missing info" field
- ⚠️ **Known Issue**: ~0.05% of job/task scheduling events missing, <1% of resource usage missing
- ⚠️ **Known Issue**: Some CPI/MAI (cycles per instruction, memory accesses per instruction) clearly inaccurate due to hardware counter bugs
- ✅ Largest publicly available cluster trace at 12.5k machines
- ✅ Long duration (29 days) for periodicity analysis

### Entropy Analysis Suitability
- **Pros**: 29-day duration; 12.5k-machine scale; historical precedent; 1-second samples enable fine-grained entropy if desired
- **Cons**: Requires Google Cloud credentials and storage setup; resource values not normalized (need per-machine baseline); disk data unreliable; CPI/MAI metrics problematic
- **Recommended Approach**:
  - Focus on CPU column; normalize by task's **cpus_requested** to get utilization ratio
  - Exclude first 14 days if disk metrics needed
  - Use 5-minute aggregated values for compatibility with Azure/Alibaba
  - Optionally use 1-second samples for high-resolution entropy (enables 60-second windows directly)
  - Filter tasks with <1% missing measurements

---

## WIKIPEDIA CLICKSTREAM & PAGE VIEW TRACES

**Publication**: Wikimedia Analytics  
**Source**: https://dumps.wikimedia.org/other/analytics/  
**Data Type**: Request logs (not CPU loads)  
**Granularity**: Monthly downloads, hourly or finer aggregation available  
**Format**: TSV (Clickstream: referer, resource, count columns)

### Characteristics
- **Clickstream**: (source article, destination article, click count) pairs from Wikipedia navigation
- **Page Views**: Request counts per article, aggregated over time periods
- **Frequency**: Monthly releases
- **Size**: ~GB per month depending on aggregation level

### Entropy Analysis Suitability
- **Pros**: Request rate is a valid proxy for workload intensity; monthly releases enable long-term pattern study; free, no survey required
- **Cons**: Measures request rate (application-level) not CPU load (system-level); may not transfer to CPU scheduling domain; no per-server metrics
- **Recommendation**: Use as **tertiary validation** only; confirm findings from Azure/Alibaba/Google before generalizing to request-driven workloads

---

## ENTROPY COMPUTATION REFERENCE PARAMETERS

### Standard Configuration
- **Window Size**: 60 seconds (real traces: adapt to granularity, e.g., 12 × 5-min samples for Azure/Alibaba)
- **Bins**: 8 equiprobable percentile bins (0th, 12.5th, 25th, ..., 87.5th, 100th percentiles)
- **Bias Correction**: Miller-Madow (H_corrected = H_raw + (K-1)/(2*N*ln(2)))
- **Max Entropy (8 bins)**: log2(8) = 3 bits
- **Min Entropy (1 bin)**: 0 bits

### Synthetic Baseline Configuration
- **Poisson Baseline**: λ = observed mean arrival rate; load = Poisson spike train + periodic (60s, 300s, 3600s sine waves)
- **Pareto Baseline**: α ≈ 1.5-2.0; inter-arrival heavy-tail; simulates burst clustering
- **Sample Size**: ≥10M samples (equivalent to largest real trace duration)

---

## Access Checklist for Executor

- [ ] **Azure V2**: Download from GitHub Blob Storage links; validate ~235GB uncompressed
- [ ] **Alibaba 2018**: Complete survey; run `fetchData.sh`; verify checksum sha256sum; untar ~98GB
- [ ] **Google 2011**: Set up gcloud SDK; authenticate; download from `clusterdata-2011-2` bucket; extract ~41GB
- [ ] **Sanity Check**: Each dataset should have ≥1M time-series samples per machine; ≥7 days continuous measurement
- [ ] **Entropy Test**: Compute entropy on 100-machine subset; verify range reasonable (0.0-3.0 bits)
