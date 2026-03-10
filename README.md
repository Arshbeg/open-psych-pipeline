## Project Sentinel: Open-Science Pipeline for Physiological Data

### 📋 Summary
**This project** is research engineering pipeline designed to process, analyze, and valorize psychological and neurophysiological data. **I have plans to make it more complex and sophisticated with more variety of data (Generated fake data) in the upcoming days**.
*It's for my own research enthusiasm and educational purposes* 

Simulating a **2x2 Factorial Design** (Stress vs. Control × High vs. Low Cognitive Load), this repository demonstrates a complete scientific data lifecycle. It transitions from the synthesis of raw ECG sensor data, through automated digital signal processing (DSP), statistical analysis in R, and concludes with a web-based valorization dashboard.

---

## 📂 Data Management Plan (DMP) & Architecture
The aim of this project is to adhere to **open science** and **FAIR** (Findable, Accessible, Interoperable, Reusable) data principles.
This project was strictly architected according to **Open Science** and **FAIR** (Findable, Accessible, Interoperable, Reusable) data principles. The repository also serves as a DMP, ensuring data integrity, reproducibility, and secure handling of simulated human-subject data.



### The FAIR Implementation:
1. **Findable (Metadata):** All recordings are strictly indexed in an immutable `metadata.csv` logbook, mapping each `participant_id` to their experimental condition and behavioral outcomes.
2. **Accessible (Raw vs. Processed Isolation):** The architecture separates raw data (`data/raw/`) from generated analytical outputs (`data/processed/`). Raw files are treated as "read-only" to prevent data corruption during processing.
3. **Interoperable (Cross-Language):** The pipeline bridges Python (Data Engineering) and R (Statistics) using standardized `.csv` data structures, ensuring researchers/stakeholders can access the data in their software of choice (R, SPSS, Excel, JASP).
4. **Reusable (Containerization):** The entire computing environment, including Python packages and pre-compiled R CRAN binaries, is containerized via a `Dockerfile` to guarantee perfect reproducibility across different operating systems.

### Directory Structure
```text
open-psych-pipeline/
├── data/
│   ├── raw/                 # [Immutable] 30 synthetic 250Hz ECG recordings
│   └── processed/           # [Generated] Extracted HRV metrics and R-Stats tables
├── scripts/                 # Processing Engine
│   ├── generate_data.py     # Simulates the Dual-Task paradigm data
│   ├── process_signals.py   # Signal cleaning & peak detection (Python/NeuroKit2)
│   └── run_statistics.R     # Methodological analysis via Linear Models (R/broom)
├── app/
│   └── dashboard.py         # Streamlit-based Valorization interface
├── Dockerfile               # Environment containerization for reproducibility
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation & DMP
```
## 🔬 The Pipeline Methodology & Technical Calculations

### Phase 1: Data Acquisition & Synthesis (`Python`)
* Simulates a cross-sectional between-subjects design (N=30) undergoing a simulated "Dual-Task" cognitive load paradigm under Stress vs. Control conditions.
* Generates realistic physiological signals (Electrocardiogram - ECG) with intentionally injected sensor noise, sampled at 250Hz for a duration of 1 to 2 minutes per subject.
* Generates behavioral outcomes (`reaction_time_ms` and `accuracy`) demonstrating a classic interaction effect where stress exponentially degrades performance during difficult tasks.

### Phase 2: Signal Processing & Feature Extraction (`Python / NeuroKit2`)
* Automates the batch processing of raw physiological arrays.
* Filtering: Applies bandpass filtering to remove simulated high-frequency sensor noise and baseline wander.
* Peak Detection: Algorithmically identifies R-peaks (individual heartbeats) to calculate NN-intervals.

#### Note: Handling Missing Data in HRV Calculations
In the generated `processed_data.csv`, several Heart Rate Variability (HRV) columns (such as `HRV_SDANN5`, `HRV_SDNNI5`, and `HRV_SDNNI2`) contain `NaN` (Not a Number) values. This is by mathematical design, not an error.
* `NeuroKit2` computes a comprehensive suite of HRV metrics. Metrics ending in "5" (e.g., `SDANN5`) calculate the standard deviation of averages over continuous 5-minute segments.
* Because our experimental task protocol simulates ultra-short-term recordings (1 to 2 minutes), `NeuroKit2` correctly identifies the lack of required duration and returns `NaN` to preserve mathematical integrity.
* The Biomarker Used: For this ultra-short-term analysis, the pipeline correctly relies on RMSSD (Root Mean Square of Successive Differences), which is the gold-standard metric for measuring parasympathetic nervous system activity (stress) in time windows under 2 minutes.

### Phase 3: Methodological Analysis (`R / broom`)
* Ingests the processed multi-modal dataset into an R environment.
* Runs standard Ordinary Least Squares (OLS) Linear Models using `lm()` to test for significant main effects and interaction effects. (Note: Mixed-Effects Models via `lme4` were initially considered but correctly downgraded to OLS due to the cross-sectional, non-repeated-measures nature of the aggregated data).
* Statistical Findings: The R script confirms a statistically significant interaction effect (`groupStress:difficultyLow`, p < 0.05), proving that psychological stress disproportionately impairs reaction time and autonomic nervous system regulation during high-load tasks.
* Exports tidy statistical coefficients back to the pipeline via the `broom` package.

### Phase 4: Data Valorization (`Python / Streamlit`)
* This phase focuses on the valorization of the research findings.
* A fully interactive Streamlit dashboard designed for non-technical researchers and stakeholders.
* Features dynamic participant selection, raw waveform inspection, and global statistical visualizations.

## 🚀 Reproducibility & Deployment
To guarantee that this pipeline runs consistently, the environment has been fully containerized using Docker, integrating both the Python runtime and R tools.

#### Run via Docker (Recommended for Open Science Reproducibility)

```bash
# Build the multi-language environment
docker build -t project-sentinel .

# Launch the interactive dashboard
docker run -p 8501:8501 project-sentinel
```

#### Run Locally (Development Mode)
Ensure you have Python 3.11+ and R 4.3+ installed.

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate & Process Data (Python Engine)
python scripts/generate_data.py
python scripts/process_signals.py

# 3. Run Methodological Analysis (R Engine)
Rscript scripts/run_statistics.R

# 4. Launch the Valorization Dashboard (Python Engine)
streamlit run app/dashboard.py
```
