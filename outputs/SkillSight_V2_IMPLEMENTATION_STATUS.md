# SkillSight V2: Implementation Status & Architecture Audit

**Platform:** SkillSight – Personalized Career Intelligence & Skill Roadmap Platform  
**Target Path:** `D:\DSPROJ\SkillSight`  
**Date:** September 21, 2026  
**Auditor:** SkillSight Data Science Engineering  

---

## 1. Features Implemented

1. **User Authentication & Session Management**:
   - Secure account registration and login using PBKDF2-HMAC-SHA256 password hashing with unique 16-byte random salts.
   - One-Click Academic Demo Mode for immediate evaluation during viva or demonstration.
   - Session persistence across Streamlit navigation tabs with secure logout.
2. **Academic & Career Profiling**:
   - Captures degree, branch, semester/year, graduation year, CGPA, certifications, and portfolio links.
   - Categorized technical skill taxonomy covering Programming Languages, Databases, Frameworks, AI & Data Science, Cloud, DevOps, and BI.
   - Support for custom user-added skills.
   - Three-tiered proficiency rating for every skill: **Beginner**, **Intermediate**, and **Advanced**.
3. **Target Career Preferences**:
   - Role selection across 14 benchmark roles or custom titles.
   - Work mode preferences (Remote, Hybrid, On-site, Any), geographic hub selection, and expected salary range.
4. **Personalized Skill-Gap Analyzer**:
   - Automatically contrasts candidate competencies with benchmark target role requirements.
   - Segregates into **Already Acquired (✓)** vs. **Skills To Develop (→)**.
   - Missing skills are annotated with exact dataset demand percentage, priority ranking (HIGH, MEDIUM, LOW), and explainable rationale.
5. **Career Readiness Score Engine**:
   - Computes an explainable 0–100 score across 5 weighted dimensions:
     * Skill Coverage (45 pts)
     * Proficiency Depth (20 pts)
     * Academic Alignment (15 pts)
     * Experience Match (10 pts)
     * Projects & Certifications (10 pts)
6. **"What Should I Learn Next?"**:
   - Ranks top 3 priority skill recommendations with pedagogical and market-grounded reasoning.
7. **Career Market Alerts**:
   - Dynamic alert banners reflecting high-demand missing skills, candidate strengths, workplace flexibility, and compensation data.
8. **Market-Relevant Technology Radar**:
   - Groups verified technologies into AI/ML, Cloud, DevOps, Big Data, and Modern Web.
   - Displays real dataset frequency, demand percentages, and practical learning summaries.
9. **Multi-Role Compatibility Matching**:
   - Computes Skill Alignment percentages across 14 career tracks to highlight alternative career pathways.
10. **Supervised ML Salary Prediction**:
    - Live inference using the trained Scikit-learn `RandomForestRegressor` pipeline pre-populated with candidate preferences.
11. **Personalized 5-Phase Career Roadmap**:
    - Dynamically generates a 5-phase structured curriculum (Foundation, Core Domain, Specialization, Cloud/DevOps, Job Readiness) tailored around candidate gaps.
12. **Hands-On Project Recommender**:
    - Recommends rule-based portfolio projects specifically chosen to resolve candidate skill gaps.
13. **Real-Time Progress Tracker**:
    - Interactive status checklist (Not Started, In Progress, Completed) stored in SQLite with real-time percentage progress calculation.
14. **12-Page Responsive Streamlit Dashboard**:
    - Redesigned UI with personalized header, metric cards, progress bars, and navigation menu.

---

## 2. Files Created & Modified

### New Backend Modules (`src/`)
- [`src/database.py`](file:///D:/DSPROJ/SkillSight/src/database.py): SQLite schema definition, context manager, and demo data seeding.
- [`src/auth.py`](file:///D:/DSPROJ/SkillSight/src/auth.py): PBKDF2 password hashing, user registration, and login verification.
- [`src/user_profile.py`](file:///D:/DSPROJ/SkillSight/src/user_profile.py): Skill taxonomy, role benchmarks, and CRUD operations for profiles.
- [`src/skill_gap.py`](file:///D:/DSPROJ/SkillSight/src/skill_gap.py): Deterministic skill-gap analyzer and priority sequencer.
- [`src/career_matching.py`](file:///D:/DSPROJ/SkillSight/src/career_matching.py): Multi-role skill alignment and compatibility scoring.
- [`src/emerging_tech.py`](file:///D:/DSPROJ/SkillSight/src/emerging_tech.py): Market-relevant technology radar across 5 domains.
- [`src/roadmap.py`](file:///D:/DSPROJ/SkillSight/src/roadmap.py): Personalized 5-phase career roadmap generator.
- [`src/project_recommender.py`](file:///D:/DSPROJ/SkillSight/src/project_recommender.py): Rule-based capstone project recommender.
- [`src/progress_tracker.py`](file:///D:/DSPROJ/SkillSight/src/progress_tracker.py): SQLite synchronization and status update engine.
- [`src/personalization.py`](file:///D:/DSPROJ/SkillSight/src/personalization.py): Career readiness score, "What to Learn Next", and market alerts.

### Modified Files
- [`dashboard/app.py`](file:///D:/DSPROJ/SkillSight/dashboard/app.py): Redesigned into an authenticated 12-page personalized platform.
- [`notebooks/job_market_analysis.ipynb`](file:///D:/DSPROJ/SkillSight/notebooks/job_market_analysis.ipynb): Extended to 26 cells including personalization engine demonstration, executed with 0 errors.
- [`README.md`](file:///D:/DSPROJ/SkillSight/README.md): Comprehensive updates covering user workflow, system architecture, and setup instructions.
- [`outputs/SkillSight_User_Workflow.md`](file:///D:/DSPROJ/SkillSight/outputs/SkillSight_User_Workflow.md): Detailed 25-step user journey.
- [`outputs/SkillSight_Progress_Report.docx`](file:///D:/DSPROJ/SkillSight/outputs/SkillSight_Progress_Report.docx) & [`report.docx`](file:///D:/DSPROJ/SkillSight/report.docx): 16 formal academic sections, ~4–5 pages.
- [`outputs/FINAL_PROJECT_STATUS.md`](file:///D:/DSPROJ/SkillSight/outputs/FINAL_PROJECT_STATUS.md): Complete module audit checklist.

---

## 3. Database Tables (SQLite: `data/skillsight.db`)

1. `users`: `id`, `name`, `email`, `password_hash`, `created_at`
2. `user_profiles`: `id`, `user_id`, `degree`, `branch`, `academic_year`, `graduation_year`, `cgpa`, `education_level`, `certifications`, `projects_summary`, `portfolio_url`, `updated_at`
3. `user_skills`: `id`, `user_id`, `skill_name`, `category`, `proficiency`, `updated_at`
4. `career_preferences`: `id`, `user_id`, `preferred_role`, `preferred_location`, `work_mode`, `expected_salary_min`, `expected_salary_max`, `preferred_industry`, `employment_type`, `experience_level`, `career_interests`, `updated_at`
5. `learning_progress`: `id`, `user_id`, `item_name`, `item_type`, `phase`, `status`, `target_role`, `completed_at`, `updated_at`

---

## 4. Existing Modules Preserved

The original baseline pipeline remains 100% operational:
- `src/preprocessing.py` $\rightarrow$ Produces `data/cleaned_jobs.csv` (15,886 rows, 23 columns)
- `src/skill_extraction.py` $\rightarrow$ Produces `outputs/results/skill_frequency.csv` (54 detected skills)
- `src/analysis.py` $\rightarrow$ Produces 14 CSV summaries in `outputs/results/`
- `src/visualization.py` $\rightarrow$ Produces 10 PNG charts in `outputs/charts/`
- `src/ml_model.py` $\rightarrow$ Produces `outputs/results/salary_model.pkl` (RandomForestRegressor, MAE: $35,525.24, R²: 0.2699)

---

## 5. Testing & Verification Status

| Component | Test Methodology | Result |
| :--- | :--- | :--- |
| **Database & Schema** | Connection context manager, table DDL, foreign keys | PASS (0 errors) |
| **Authentication** | Registration, PBKDF2 hashing, demo session login | PASS (0 errors) |
| **Skill-Gap Engine** | Gap calculation, priority sorting, demand matching | PASS (0 errors) |
| **Personalization Engine** | Readiness score decomposition, top 3 skill picker | PASS (0 errors) |
| **Streamlit Dashboard** | Official `AppTest` framework across all 12 pages | PASS (0 errors) |
| **Interactive Prediction** | Live Random Forest inference via Streamlit button | PASS ($115,290.80) |
| **Progress Tracker** | Real-time status toggling in SQLite | PASS (0 errors) |
| **Jupyter Notebook** | 26 cells executed via nbformat runner | PASS (0 error cells) |

---

## 6. Known Limitations

1. **Cross-Sectional Dataset**: Telemetry captures a single collection window from 2023 without multi-year longitudinal tracking.
2. **Salary Sparsity**: 59.07% of job listings omit salary data; the ML model reflects organizations practicing wage transparency.
3. **Analytical Estimate Nature**: Career Readiness Scores and Salary Predictions are statistical decision-support estimates, not recruitment or hiring guarantees.

---

## 7. Future Enhancements

1. **Automated Resume Parsing**: Integrate PDF parsing to populate candidate skills and proficiencies automatically.
2. **Continuous Ingestion Pipeline**: Connect to live employment APIs to track quarterly demand trends.
3. **Gamified Practice Milestones**: Link roadmap milestones directly to curated LeetCode/HackerRank coding challenges.
