# SkillSight – User Workflow

**SkillSight: Personalized Career Intelligence & Skill Roadmap Platform**

SkillSight empowers students, aspiring engineers, career transitioners, and academic mentors by combining macro-level job-market analytics with personalized profile intelligence.

This document describes the complete end-to-end user experience and interaction flow from the **user's point of view**.

---

## The Personalized User Journey

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

---

## 1. Registration & Authentication

When the user navigates to SkillSight:
- **Landing & Security**: The user is presented with a secure sign-in portal. The user can:
  - **Sign In** using their registered email address and secure password.
  - **Create Account** by providing their name, email, and password. SkillSight immediately hashes passwords with PBKDF2-HMAC-SHA256 and initializes an empty career profile in SQLite.
  - **⚡ One-Click Academic Demo Mode**: Academic evaluators and viva panelists can click one button to instantly launch an active demonstration session (pre-loaded as **Alex Morgan**, 3rd Year B.Tech Computer Science student targeting a Data Scientist role).
- **Session Persistence**: Once authenticated, the user's session remains active across all navigation tabs, preserving their customized data.

---

## 2. Personalized Welcome & Executive Telemetry

Immediately upon entering the dashboard, the user sees a personalized executive banner and top-level KPI telemetry:
- **Welcome Banner**: Displays the user's name, target career role, academic program, current semester/year, readiness score, and live roadmap progress.
- **Metric Highlights**:
  - **Career Readiness Score**: E.g., `61 / 100` (*Competitive Progress*), decomposed into measurable factors.
  - **Roadmap Completion**: E.g., `40.0%` (4 of 10 items completed).
  - **Skills Acquired**: Total skills currently saved in the user's inventory.
  - **Target Role & Work Mode**: E.g., `Data Scientist (Remote)`.
- **"What Should I Learn Next?"**: The system immediately presents the top 3 priority skill recommendations derived from target role gaps and market demand (e.g., AWS, Machine Learning, Scikit-learn), accompanied by clear, explainable reasoning.
- **Career Market Alerts**: Contextual informational alerts based on the 15,886 job-posting dataset highlighting high-priority missing competencies and salary benchmarks.

---

## 3. Candidate Profile & Competency Management

On the **My Profile** page, the user builds and refines their personal profile across three intuitive tabs:
1. **Academic & Personal**:
   - Degree (B.Tech, B.E., B.Sc, BCA, M.Tech, etc.)
   - Branch / Specialization (Computer Science, Data Science, IT, etc.)
   - Current Academic Year & Expected Graduation Year
   - CGPA / Academic Percentage
   - Optional Certifications & Summary of Completed Projects
   - Portfolio / GitHub link
2. **Technical Skills & Proficiency Levels**:
   - Categorized multi-select pickers covering Programming Languages, Databases, Frameworks, AI & Data Science, Cloud, DevOps, and BI tools.
   - Capability to add custom, unlisted skills (e.g., Rust, Next.js, Solidity).
   - For **every** selected skill, the user selects their proficiency level: **Beginner**, **Intermediate**, or **Advanced**.
3. **Target Career Preferences**:
   - Preferred Role selection from 14 benchmark roles (or custom role entry).
   - Geographic preference (United States, New York, San Francisco, Austin, Remote, etc.).
   - Work mode preference (Remote, Hybrid, On-site, Any).
   - Expected annual salary range ($ Min and $ Max).
   - Employment format (Full-time, Internship, Contract).

Saving any tab updates the local SQLite database in real time.

---

## 4. Personalized Skill Intelligence

On the **Skill Analysis** page:
- The user reviews a consolidated inventory of their currently acquired skills, broken down by proficiency level.
- Alongside their personal inventory, the user observes the macro-level **Top 15 Technical Skills** ranked by market demand in the LinkedIn dataset (e.g., Excel at 16.34%, SQL at 4.81%, Python at 3.88%, AWS at 3.04%), allowing immediate benchmarking of personal strengths against employer expectations.

---

## 5. Skill Gap Analysis

On the **Skill Gap** page:
- The user examines an explainable breakdown comparing their current skills against their selected target role:
  - **Role Skill Coverage**: A percentage progress indicator (e.g., `33.3%` coverage).
  - **Already Acquired (✓)**: Benchmark skills the user already possesses, tagged with their proficiency level and whether they are a core foundational skill.
  - **Skills To Develop (→)**: Missing competencies ordered by suggested learning sequence. Each missing skill displays:
    * Exact dataset demand percentage and posting count.
    * Priority tier: **HIGH PRIORITY**, **MEDIUM PRIORITY**, or **LOW PRIORITY**.
    * Explainable rationale explaining why the skill is critical for the target role.

---

## 6. Macro Job Market Telemetry

On the **Job Market** page:
- The user steps back to analyze macro-level trends across the entire 15,886-posting LinkedIn dataset:
  - Top 15 job titles (commercial, analytical, and engineering).
  - Geographic employment hubs (New York, Chicago, Houston, Atlanta, Los Angeles).
  - Seniority breakdown (Mid-Senior: 32.00%, Entry-level: 23.25%, Director/Executive: 5.16%).
  - Employment work types (Full-time: 80.85%, Contract: 10.95%).
  - Remote work distribution (14.73% Remote vs. 85.27% On-site/Unspecified).

---

## 7. Market-Relevant Technology Radar

On the **Emerging Technologies** page:
- The user explores the **Market-Relevant Technology Radar** organized across 5 critical domains:
  1. *AI & Machine Learning* (Machine Learning, Deep Learning, NLP, AI)
  2. *Cloud Computing & Infrastructure* (AWS, Azure, Google Cloud)
  3. *DevOps & Containerization* (Docker, Kubernetes, Terraform)
  4. *Data Engineering & Big Data* (Apache Spark, Kafka, Databricks)
  5. *Modern Web & Distributed Systems* (React, TypeScript, Microservices)
- Each technology card displays verified dataset demand share, related job roles, complementary skill stacks, and an explainable "Why learn this" summary.
- Clearly labeled as: *Market-Relevant Technology (Verified in LinkedIn Dataset)* to prevent ungrounded trend claims.

---

## 8. Career Role Compatibility & Skill Alignment

On the **Career Roles** page:
- The user reviews a compatibility ranking across **14 distinct career tracks** (Data Scientist, Data Analyst, Machine Learning Engineer, Java Developer, Backend Developer, Frontend Developer, Full Stack Developer, Cloud Engineer, DevOps Engineer, etc.).
- For each role, SkillSight calculates an explainable **Skill Alignment Percentage**:
  - Highlights existing transferable competencies already in the user's inventory.
  - Lists the highest-priority missing skills required to transition into that career track.
- Enables students to identify alternative career options where their existing skill portfolio provides an immediate competitive advantage.

---

## 9. Personalized Salary Insights & Prediction

On the **Salary Insights** page:
- The user accesses data-grounded compensation analytics:
  - Dataset descriptive statistics: Mean ($70,188), Median ($65,000), Standard Deviation ($77,639).
  - Average salary broken down by experience tier and work type.
- **Interactive Machine Learning Predictor**:
  - The form is pre-populated with the user's preferred experience level, work type, location, and target role discipline.
  - The user clicks **"Predict Annual Compensation"** to run inference through the trained `RandomForestRegressor` pipeline.
  - SkillSight immediately outputs a data-grounded compensation estimate (e.g., `$115,290.80 USD`) along with model evaluation context (MAE: $35,525.24, R²: 0.2699).

---

## 10. Personalized Career Roadmap

On the **Career Roadmap** page:
- SkillSight dynamically synthesizes the user's profile, skill gaps, and market priorities into a structured **5-Phase Career Curriculum**:
  - **Phase 1: Foundation & Prerequisite Mastery** (3–5 weeks)
  - **Phase 2: Core Domain & Role Competencies** (6–8 weeks)
  - **Phase 3: Advanced Architecture & Specialization** (5–7 weeks)
  - **Phase 4: Cloud Infrastructure & Production Readiness** (4–6 weeks)
  - **Phase 5: Job Readiness, Capstones & Interview Prep** (3–4 weeks)
- Every missing skill is placed into its pedagogically appropriate phase with priority badges (**HIGH**, **MEDIUM**, **LOW**) and explainable rationales.
- The roadmap automatically synchronizes with the user's SQLite progress database.

---

## 11. Recommended Portfolio Projects

On the **Recommended Projects** page:
- The user reviews curated, rule-based portfolio project specifications tailored specifically to their missing skills:
  - E.g., *Customer Churn Prediction & Retention System*
  - *Enterprise Sales & Revenue Analytics Dashboard*
  - *Job Market Intelligence & Salary Prediction Platform*
  - *Scalable E-Commerce RESTful Microservices API*
- Each project card outlines:
  - Targeted skills developed (highlighting which of the user's missing skills are addressed).
  - Difficulty level (Beginner, Intermediate, Advanced).
  - Recommended tech stack and libraries.
  - Concrete expected deliverable and portfolio impact.

---

## 12. Real-Time Progress Tracker

On the **Progress Tracker** page:
- The user actively manages and tracks their learning journey:
  - A real-time progress bar visualizes overall percentage completion.
  - Metric cards show total items, completed items, skills mastered, and projects finished.
  - For every roadmap item across all 5 phases, the user can toggle the status dropdown between **Not Started**, **In Progress**, and **Completed**.
  - Status updates and completion timestamps are saved immediately to SQLite, dynamically updating the user's Career Readiness Score and executive banner upon reload.

---

## 13. System Positioning & Academic Context

On the **About** page:
- The user reviews the architectural principles, data sources, and academic boundaries of the platform.
- Re-iterates that SkillSight is an explainable decision-support tool that bridges candidate qualifications with empirical job market data, maintaining complete transparency without black-box claims or artificial employment guarantees.
