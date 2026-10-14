# SkillSight — Project Flow & Pipeline Architecture

```text
INPUT DATA
    ↓
PREPROCESSING
    ↓
SKILL EXTRACTION
    ↓
EDA (EXPLORATORY DATA ANALYSIS)
    ↓
VISUALIZATION
    ↓
MACHINE LEARNING
    ↓
DASHBOARD
```

---

## Stage-by-Stage Specifications

### 1. INPUT DATA (Raw Data Ingestion)
- **Python File**: None (Raw storage / ingestion layer)
- **Input**: 
  - `data/raw_jobs.csv` (15,886 job records, 27 raw columns, 64.4 MB)
  - `data/job_postings.csv` (identical copy of raw jobs dataset)
  - `data/benefits.csv` (13,763 rows linking job_id to benefits)
- **Output**: Raw tabular files ready for preprocessing
- **Purpose**: Acts as the ground-truth data store containing scraped LinkedIn job postings, full unstructured job descriptions, salary figures, and employment attributes.

---

### 2. PREPROCESSING
- **Python File**: `src/preprocessing.py`
- **Input**: `data/raw_jobs.csv`
- **Output**: `data/cleaned_jobs.csv` (15,886 rows, 21 columns, 61.1 MB)
- **Purpose**: 
  - Deduplicates jobs based on `job_id`.
  - Imputes missing values (`description` -> `""`, `title` -> `"Unknown"`, `location` -> `"Unknown"`, `formatted_experience_level` -> `"Not Specified"`).
  - Cleans and normalizes text whitespace using regex (`\s+` -> `" "`).
  - Synthesizes a unified `salary` metric from `med_salary` and the average of `min_salary` and `max_salary`.
  - Categorizes remote work (`remote_status`: `"Remote"`, `"On-site"`, `"Not Specified"`).
  - Prunes unused metadata columns to produce an optimized tabular dataset.

---

### 3. SKILL EXTRACTION
- **Python File**: `src/skill_extraction.py`
- **Input**: `data/cleaned_jobs.csv`
- **Output**: `outputs/results/skill_frequency.csv` (56 tracked skills with job counts and demand percentages)
- **Purpose**: 
  - Defines a technical taxonomy of 49 skills across 8 domains (Languages, Databases, Web, AI/Data Science, Cloud, DevOps, BI, APIs).
  - Maps multi-word synonyms and acronyms (e.g., `golang`, `sklearn`, `amazon web services`).
  - Applies safe regex lookaround pattern matching `(?<!\w)keyword(?!\w)` on lowercased job descriptions to handle special symbols (e.g., `C++`, `C#`, `Node.js`) while preventing false substring matches (e.g., "Go" in "Good").
  - Deduplicates skill mentions per job using Python `set` so each skill is counted at most once per listing.
  - Aggregates global frequency counts and computes market demand percentages.

---

### 4. EDA (EXPLORATORY DATA ANALYSIS)
- **Python File**: `src/analysis.py` & `notebooks/job_market_analysis.ipynb`
- **Input**: `data/cleaned_jobs.csv` & `outputs/results/skill_frequency.csv`
- **Output**: 
  - `outputs/results/top_job_titles.csv`
  - `outputs/results/top_locations.csv`
  - `outputs/results/top_companies.csv`
  - `outputs/results/experience_levels.csv`
  - `outputs/results/work_type.csv`
  - `outputs/results/remote_jobs.csv`
  - `outputs/results/salary_summary.csv`
  - `outputs/results/dataset_summary.csv`
- **Purpose**: 
  - Computes descriptive statistics across employment types, seniority levels, geographic hubs, and hiring companies.
  - Calculates compensation metrics (mean, median, min, max salary) across the non-null salary subset (6,502 postings).
  - Profiles the macro dataset characteristics to uncover hiring trends.

---

### 5. VISUALIZATION
- **Python File**: `src/visualization.py` (to be created) & `notebooks/job_market_analysis.ipynb`
- **Input**: Summarized metrics in `outputs/results/*.csv` and `data/cleaned_jobs.csv`
- **Output**: High-resolution chart figures saved in `outputs/charts/` (e.g., `top_skills_bar.png`, `salary_distribution.png`, `experience_distribution.png`, `remote_work_pie.png`)
- **Purpose**: 
  - Generates visual plots using Matplotlib, Seaborn, and Plotly.
  - Enables visual pattern recognition for skill ranking, salary spreads, and regional demand.
  - Provides exportable graphics for analytical reports and presentations.

---

### 6. MACHINE LEARNING
- **Python File**: `src/ml_models.py` or dedicated notebook section (to be implemented)
- **Input**: `data/cleaned_jobs.csv` and binary/TF-IDF extracted skill matrix
- **Output**: Trained model artifacts (e.g., `outputs/models/salary_predictor.joblib` or cluster assignments)
- **Purpose**: 
  - **Skill-Based Job Clustering (Unsupervised)**: Groups job listings by skill co-occurrences (K-Means/DBSCAN) to discover tech stack archetypes.
  - **Salary Prediction (Supervised Regression)**: Trains a regression model (Random Forest / Gradient Boosting) to estimate salary based on skills, location, and experience level.
  - **Skill Association Rule Mining / Correlation**: Uncovers complementary tech pairs (e.g., Python + AWS, React + TypeScript).

---

### 7. DASHBOARD
- **Python File**: `dashboard/app.py`
- **Input**: `data/cleaned_jobs.csv` and `outputs/results/*.csv`
- **Output**: Interactive Streamlit web interface accessible via browser
- **Purpose**: 
  - Serves as the user-facing presentation layer.
  - Displays high-level KPI cards (Total Jobs, Unique Roles, Locations).
  - Provides dynamic filtering by role, location, remote status, and experience level.
  - Renders interactive skill demand charts and salary insights for non-technical users.
