# SkillSight

**SkillSight: Personalized Career Intelligence & Skill Roadmap Platform**

SkillSight is an end-to-end data science and personalized career intelligence platform. It analyzes 15,886 multi-attribute LinkedIn job postings to extract in-demand skills, benchmark hiring dynamics, and predict compensation. By cross-referencing this empirical dataset with an individual's academic background, technical skills, and career goals, SkillSight pinpoints exact skill gaps, highlights market-relevant technologies, computes an explainable Career Readiness Score, and generates a personalized, multi-phase career roadmap with tailored portfolio projects and real-time progress tracking.

---

## The Complete User Journey

SkillSight is designed from the ground up for students, aspiring engineers, career transitioners, and academic mentors. The user experience is structured as an interactive 25-step journey:

```
USER
 ↓
REGISTER / LOGIN
 ↓
CREATE CAREER PROFILE
 ↓
ENTER ACADEMIC INFORMATION
 ↓
ADD CURRENT SKILLS
 ↓
SELECT SKILL PROFICIENCY
 ↓
SELECT TARGET CAREER
 ↓
SELECT PREFERENCES
 ↓
SKILLSIGHT ANALYZES PROFILE
 ↓
COMPARES WITH JOB MARKET
 ↓
IDENTIFIES SKILL GAPS
 ↓
SHOWS MARKET-RELEVANT TECHNOLOGIES
 ↓
SHOWS CAREER ROLE ALIGNMENT
 ↓
GENERATES PERSONALIZED ROADMAP
 ↓
RECOMMENDS PROJECTS
 ↓
SHOWS SALARY INSIGHTS
 ↓
TRACKS LEARNING PROGRESS
 ↓
UPDATES ROADMAP
```

### Key Interactive Phases
1. **Authentication & Session**: Secure login or 1-Click Academic Demo Mode (pre-seeded as Alex Morgan, 3rd Year B.Tech Computer Science).
2. **Personalized Telemetry**: Instant overview of Career Readiness Score (0–100), roadmap completion percentage, "What Should I Learn Next?" (top 3 priority skills), and Career Market Alerts.
3. **Profile & Competency Management**: Self-serve entry of degree, branch, year, CGPA, certifications, and categorized technical skills with three proficiency levels (**Beginner**, **Intermediate**, **Advanced**).
4. **Skill-Gap Analysis**: Clear segregation of **Already Acquired (✓)** vs. **Skills To Develop (→)** with exact dataset demand percentages, priority tiers (HIGH, MEDIUM, LOW), and explainable pedagogical reasoning.
5. **Emerging Technology Radar**: Exploration of market-relevant technologies across AI/ML, Cloud, DevOps, Data Engineering, and Modern Web backed by verified job-posting frequency.
6. **Multi-Role Skill Alignment**: Compatibility scoring across 14 career tracks (Data Scientist, Data Analyst, ML Engineer, Java Developer, Backend Developer, Full Stack Developer, etc.).
7. **Personalized Salary Insights**: Live inference using a supervised `RandomForestRegressor` model predicting annual salary based on user career preferences.
8. **Career Roadmap & Project Recommender**: 5-phase personalized curriculum with tailored hands-on portfolio projects mapped to candidate skill gaps.
9. **Real-Time Progress Tracking**: SQLite-backed interactive checklist allowing users to toggle status between *Not Started*, *In Progress*, and *Completed*.

---

## System Architecture: User Workflow vs. System Workflow

| Dimension | User Workflow (Frontend Experience) | System Workflow (Data Engineering & ML) |
| :--- | :--- | :--- |
| **Primary Focus** | Career self-assessment, gap analysis & guidance | Vectorized cleaning, text NLP, regression & persistence |
| **User Interface** | 12-page Streamlit authenticated web application | Python scripts, Pandas pipelines, Scikit-learn models |
| **Data Ingestion** | Form inputs (academic details, skills, proficiencies) | Raw LinkedIn CSV datasets (`data/cleaned_jobs.csv`) |
| **Data Storage** | SQLite (`data/skillsight.db`) for user accounts & tracking | CSV summaries (`outputs/results/`) & serialized PKL model |
| **Outputs** | Personalized roadmap, readiness score, recommendations | Model evaluation metrics (MAE: $35,525.24, R²: 0.2699) |

### System Execution Architecture

```
                    SKILLSIGHT V2 ARCHITECTURE
                                |
        +-----------------------+-----------------------+
        |                                               |
   JOB MARKET DATA                                 USER PROFILE
   (15,886 Postings)                               (SQLite DB: data/skillsight.db)
        |                                               |
        ↓                                               ↓
Skill Extraction (49 Skills)                   Academic Background
        |                                      Current Skills & Proficiencies
        ↓                                      Career Preferences
Market Analysis (EDA & ML Pipeline)                     |
        |                                               |
        +-----------------------+-----------------------+
                                ↓
                        PERSONALIZATION ENGINE
                                |
        +-----------------------+-----------------------+
        |                       |                       |
   Skill Gap Analyzer       Role Matcher           Tech Radar
   (Missing Skills)         (Alignment %)          (Market Demand)
        |                       |                       |
        +-----------------------+-----------------------+
                                ↓
                        CAREER INTELLIGENCE
                                |
        +-----------------------+-----------------------+
        |                       |                       |
  Career Roadmap        Project Recommender     Salary Insights
  (5 Phases)            (Skill-gap Based)       (RF Model Live Inference)
        |
        ↓
  Progress Tracking (SQLite Real-Time Synchronization)
```

---

## Project Structure

```text
SkillSight/
│
├── dashboard/
│   └── app.py                         # Authenticated 12-page Streamlit career platform
│
├── data/
│   ├── cleaned_jobs.csv               # 15,886 cleaned job postings (23 columns)
│   ├── raw_jobs.csv                   # Raw LinkedIn listing corpus
│   ├── job_postings.csv               # Source dataset
│   └── skillsight.db                  # SQLite database (users, profiles, skills, progress)
│
├── notebooks/
│   └── job_market_analysis.ipynb      # 26-cell zero-error reproducible analysis notebook
│
├── outputs/
│   ├── charts/                        # 10 publication-quality PNG charts
│   ├── results/                       # 14 analytical CSV summaries & salary_model.pkl
│   ├── SkillSight_User_Workflow.md    # Complete 25-step user journey documentation
│   ├── SkillSight_Progress_Report.docx # 16-section comprehensive academic progress report
│   ├── SkillSight_V2_IMPLEMENTATION_STATUS.md # V2 architecture audit
│   └── FINAL_PROJECT_STATUS.md        # Verified completion audit and project metrics
│
├── src/
│   ├── database.py                    # SQLite schema, context manager, and demo seeding
│   ├── auth.py                        # PBKDF2 password hashing & authentication
│   ├── user_profile.py                # Skills taxonomy, role benchmarks, and profile CRUD
│   ├── skill_gap.py                   # Deterministic skill-gap analyzer
│   ├── career_matching.py             # Multi-role skill alignment scoring
│   ├── emerging_tech.py               # Market-relevant technology radar
│   ├── roadmap.py                     # Personalized 5-phase career roadmap generator
│   ├── project_recommender.py         # Rule-based capstone project recommender
│   ├── progress_tracker.py            # SQLite roadmap progress tracker
│   ├── personalization.py             # Career readiness score & "What to Learn Next"
│   ├── preprocessing.py               # Dataset cleansing and salary unification
│   ├── skill_extraction.py            # Boundary-safe regex skill extractor
│   ├── analysis.py                    # 12-stage exploratory data analysis
│   ├── visualization.py               # Matplotlib chart generation pipeline
│   └── ml_model.py                    # Random Forest salary regression pipeline
│
├── requirements.txt                   # Python environment dependencies
├── README.md                          # Project documentation
└── report.docx                        # Formatted academic progress report
```

---

## Academic Positioning & Disclaimers

SkillSight is an explainable decision-support and career intelligence tool.
- It is **NOT** a recruitment system, employment agency, or hiring guarantee.
- It is **NOT** a replacement for human academic mentorship or career counseling.
- It **DOES NOT** invent unverified future growth predictions; all demand metrics are derived directly from the verified 15,886 LinkedIn job-posting dataset.
- The **Career Readiness Score** is an analytical estimate based on candidate profile attributes and empirical market standards.

---

## Setup & Execution Instructions

### 1. Environment Setup
```bash
pip install -r requirements.txt
```

### 2. Run Baseline Data Science Pipeline
```bash
python src/preprocessing.py
python src/skill_extraction.py
python src/analysis.py
python src/visualization.py
python src/ml_model.py
```

### 3. Launch the Streamlit Platform
```bash
streamlit run dashboard/app.py
```
*Tip: You can use the **⚡ One-Click Academic Demo Mode** button on the sign-in screen to explore the personalized dashboard immediately, or register a new user account.*

### 4. Run the Jupyter Notebook
```bash
jupyter notebook notebooks/job_market_analysis.ipynb
```
