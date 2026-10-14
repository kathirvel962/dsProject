"""SkillSight - Module 4: Job Market Analysis / Exploratory Data Analysis (EDA).

Performs comprehensive exploratory analysis across the cleaned LinkedIn job postings dataset:
1. Top Technical Skills Analysis (from skill_frequency.csv)
2. Top Job Titles Analysis
3. Top Locations Analysis
4. Top Hiring Companies Analysis
5. Experience Level Distribution
6. Work Type Distribution
7. Remote Work Breakdown
8. Overall Salary Descriptive Statistics
9. Salary by Experience Level
10. Salary by Work Type
11. Location Summary & Geographical Concentration
12. Overall Dataset Summary Statistics
"""

import os
import numpy as np
import pandas as pd

# File paths
CLEANED_JOBS_FILE = "data/cleaned_jobs.csv"
SKILL_FREQUENCY_FILE = "outputs/results/skill_frequency.csv"
OUTPUT_DIR = "outputs/results"


def run_analysis(
    jobs_path: str = CLEANED_JOBS_FILE,
    skills_path: str = SKILL_FREQUENCY_FILE,
    output_dir: str = OUTPUT_DIR,
) -> dict:
    """Execute the full EDA pipeline and export CSV artifacts."""
    print("=" * 60)
    print("SKILLSIGHT - JOB MARKET ANALYSIS & EDA (MODULE 4)")
    print("=" * 60)

    # --------------------------------------------------
    # 0. SETUP & DATA INGESTION
    # --------------------------------------------------
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n[1/12] Loading cleaned jobs dataset from: {jobs_path}")
    jobs = pd.read_csv(jobs_path)
    total_jobs = len(jobs)
    print(f"Total job postings loaded: {total_jobs:,}")

    # Load skill frequency results if available
    skills_df = None
    if os.path.exists(skills_path):
        print(f"Loading skill frequency data from: {skills_path}")
        skills_df = pd.read_csv(skills_path)
    else:
        print(f"Warning: {skills_path} not found. Skill analysis may be limited.")

    # --------------------------------------------------
    # 1. TOP TECHNICAL SKILLS
    # --------------------------------------------------
    print("\n[2/12] Analyzing Top Technical Skills...")
    if skills_df is not None:
        # Sort skills by job count descending and select top in-demand skills
        top_skills = (
            skills_df.sort_values(by="Job_Count", ascending=False)
            .head(20)
            .reset_index(drop=True)
        )
        top_skills_path = os.path.join(output_dir, "top_skills.csv")
        top_skills.to_csv(top_skills_path, index=False)
        print(f"Saved top technical skills to: {top_skills_path}")
    else:
        top_skills = pd.DataFrame(columns=["Skill", "Job_Count", "Demand_Percentage"])

    # --------------------------------------------------
    # 2. TOP JOB TITLES
    # --------------------------------------------------
    print("\n[3/12] Analyzing Top Job Titles...")
    # Clean text: replace empty strings or nulls with Unknown
    clean_titles = jobs["title"].fillna("Unknown").replace(r"^\s*$", "Unknown", regex=True)
    top_titles = clean_titles.value_counts().head(20).reset_index()
    top_titles.columns = ["Job_Title", "Job_Count"]

    top_titles_path = os.path.join(output_dir, "top_job_titles.csv")
    top_titles.to_csv(top_titles_path, index=False)
    print(f"Saved top job titles to: {top_titles_path}")

    # --------------------------------------------------
    # 3. TOP LOCATIONS
    # --------------------------------------------------
    print("\n[4/12] Analyzing Top Locations...")
    clean_locations = jobs["location"].fillna("Unknown").replace(r"^\s*$", "Unknown", regex=True)
    top_locations = clean_locations.value_counts().head(20).reset_index()
    top_locations.columns = ["Location", "Job_Count"]

    top_locations_path = os.path.join(output_dir, "top_locations.csv")
    top_locations.to_csv(top_locations_path, index=False)
    print(f"Saved top locations to: {top_locations_path}")

    # --------------------------------------------------
    # 4. TOP HIRING COMPANIES
    # --------------------------------------------------
    print("\n[5/12] Analyzing Top Companies...")
    # Handle missing company identifiers cleanly
    clean_companies = jobs["company_id"].dropna().astype("int64")
    top_companies = clean_companies.value_counts().head(20).reset_index()
    top_companies.columns = ["Company_ID", "Job_Count"]

    top_companies_path = os.path.join(output_dir, "top_companies.csv")
    top_companies.to_csv(top_companies_path, index=False)
    print(f"Saved top companies to: {top_companies_path}")

    # --------------------------------------------------
    # 5. EXPERIENCE LEVEL ANALYSIS
    # --------------------------------------------------
    print("\n[6/12] Analyzing Experience Levels...")
    clean_experience = (
        jobs["formatted_experience_level"]
        .fillna("Not Specified")
        .replace(r"^\s*$", "Not Specified", regex=True)
    )
    experience_levels = clean_experience.value_counts().reset_index()
    experience_levels.columns = ["Experience_Level", "Job_Count"]
    experience_levels["Percentage"] = (
        experience_levels["Job_Count"] / total_jobs * 100
    ).round(2)

    experience_path = os.path.join(output_dir, "experience_levels.csv")
    experience_levels.to_csv(experience_path, index=False)
    print(f"Saved experience level distribution to: {experience_path}")

    # --------------------------------------------------
    # 6. WORK TYPE ANALYSIS
    # --------------------------------------------------
    print("\n[7/12] Analyzing Work Types...")
    clean_work_type = (
        jobs["formatted_work_type"]
        .fillna("Not Specified")
        .replace(r"^\s*$", "Not Specified", regex=True)
    )
    work_type = clean_work_type.value_counts().reset_index()
    work_type.columns = ["Work_Type", "Job_Count"]
    work_type["Percentage"] = (work_type["Job_Count"] / total_jobs * 100).round(2)

    work_type_path = os.path.join(output_dir, "work_type.csv")
    work_type.to_csv(work_type_path, index=False)
    print(f"Saved work type breakdown to: {work_type_path}")

    # --------------------------------------------------
    # 7. REMOTE WORK ANALYSIS
    # --------------------------------------------------
    print("\n[8/12] Analyzing Remote Work...")
    clean_remote = (
        jobs["remote_status"]
        .fillna("Not Specified")
        .replace(r"^\s*$", "Not Specified", regex=True)
    )
    remote_jobs = clean_remote.value_counts().reset_index()
    remote_jobs.columns = ["Remote_Status", "Job_Count"]
    remote_jobs["Percentage"] = (remote_jobs["Job_Count"] / total_jobs * 100).round(2)

    remote_path = os.path.join(output_dir, "remote_jobs.csv")
    remote_jobs.to_csv(remote_path, index=False)
    print(f"Saved remote work breakdown to: {remote_path}")

    # --------------------------------------------------
    # 8. SALARY ANALYSIS
    # --------------------------------------------------
    print("\n[9/12] Analyzing Overall Salary Distribution...")
    # Filter strictly for valid, non-null, positive numerical salary values
    # Missing salaries are NEVER replaced with fake/imputed values
    valid_salary_mask = jobs["salary"].notna() & (jobs["salary"] > 0) & np.isfinite(jobs["salary"])
    salary_series = jobs.loc[valid_salary_mask, "salary"]

    if len(salary_series) > 0:
        salary_summary = pd.DataFrame({
            "Metric": [
                "Count",
                "Mean",
                "Median",
                "Minimum",
                "Maximum",
                "Standard Deviation",
            ],
            "Value": [
                int(salary_series.count()),
                round(float(salary_series.mean()), 2),
                round(float(salary_series.median()), 2),
                round(float(salary_series.min()), 2),
                round(float(salary_series.max()), 2),
                round(float(salary_series.std()), 2),
            ],
        })
    else:
        salary_summary = pd.DataFrame(columns=["Metric", "Value"])

    salary_summary_path = os.path.join(output_dir, "salary_summary.csv")
    salary_summary.to_csv(salary_summary_path, index=False)
    print(f"Saved salary descriptive statistics to: {salary_summary_path}")

    # --------------------------------------------------
    # 9. SALARY BY EXPERIENCE LEVEL
    # --------------------------------------------------
    print("\n[10/12] Analyzing Salary by Experience Level...")
    valid_salary_jobs = jobs[valid_salary_mask].copy()
    valid_salary_jobs["formatted_experience_level"] = (
        valid_salary_jobs["formatted_experience_level"]
        .fillna("Not Specified")
        .replace(r"^\s*$", "Not Specified", regex=True)
    )

    salary_by_exp = (
        valid_salary_jobs.groupby("formatted_experience_level")["salary"]
        .agg(
            Job_Count="count",
            Average_Salary=lambda s: round(s.mean(), 2),
            Median_Salary=lambda s: round(s.median(), 2),
        )
        .reset_index()
        .rename(columns={"formatted_experience_level": "Experience_Level"})
        .sort_values(by="Job_Count", ascending=False)
        .reset_index(drop=True)
    )

    salary_by_exp_path = os.path.join(output_dir, "salary_by_experience.csv")
    salary_by_exp.to_csv(salary_by_exp_path, index=False)
    print(f"Saved salary by experience level to: {salary_by_exp_path}")

    # --------------------------------------------------
    # 10. SALARY BY WORK TYPE
    # --------------------------------------------------
    print("\n[11/12] Analyzing Salary by Work Type...")
    valid_salary_jobs["formatted_work_type"] = (
        valid_salary_jobs["formatted_work_type"]
        .fillna("Not Specified")
        .replace(r"^\s*$", "Not Specified", regex=True)
    )

    salary_by_wt = (
        valid_salary_jobs.groupby("formatted_work_type")["salary"]
        .agg(
            Job_Count="count",
            Average_Salary=lambda s: round(s.mean(), 2),
            Median_Salary=lambda s: round(s.median(), 2),
        )
        .reset_index()
        .rename(columns={"formatted_work_type": "Work_Type"})
        .sort_values(by="Job_Count", ascending=False)
        .reset_index(drop=True)
    )

    salary_by_wt_path = os.path.join(output_dir, "salary_by_work_type.csv")
    salary_by_wt.to_csv(salary_by_wt_path, index=False)
    print(f"Saved salary by work type to: {salary_by_wt_path}")

    # --------------------------------------------------
    # 11. LOCATION ANALYSIS
    # --------------------------------------------------
    print("\n[12/12] Generating Location Summary...")
    location_counts = clean_locations.value_counts().head(20).reset_index()
    location_counts.columns = ["Location", "Job_Count"]
    location_counts["Percentage"] = (
        location_counts["Job_Count"] / total_jobs * 100
    ).round(2)

    location_summary_path = os.path.join(output_dir, "location_summary.csv")
    location_counts.to_csv(location_summary_path, index=False)
    print(f"Saved location summary to: {location_summary_path}")

    # --------------------------------------------------
    # 12. DATASET SUMMARY
    # --------------------------------------------------
    jobs_with_salary = int(valid_salary_mask.sum())
    jobs_without_salary = int(total_jobs - jobs_with_salary)
    remote_jobs_count = int((clean_remote == "Remote").sum())
    non_remote_jobs_count = int(total_jobs - remote_jobs_count)

    dataset_summary = pd.DataFrame({
        "Metric": [
            "Total Jobs",
            "Unique Job Titles",
            "Unique Locations",
            "Unique Companies",
            "Jobs With Salary",
            "Jobs Without Salary",
            "Remote Jobs",
            "Non-Remote Jobs",
        ],
        "Value": [
            total_jobs,
            clean_titles.nunique(),
            clean_locations.nunique(),
            clean_companies.nunique(),
            jobs_with_salary,
            jobs_without_salary,
            remote_jobs_count,
            non_remote_jobs_count,
        ],
    })

    dataset_summary_path = os.path.join(output_dir, "dataset_summary.csv")
    dataset_summary.to_csv(dataset_summary_path, index=False)
    print(f"Saved dataset summary to: {dataset_summary_path}")

    # --------------------------------------------------
    # TERMINAL DISPLAY OF KEY FINDINGS
    # --------------------------------------------------
    print("\n" + "=" * 60)
    print("KEY JOB MARKET FINDINGS")
    print("=" * 60)

    print("\n--- DATASET OVERVIEW ---")
    print(dataset_summary.to_string(index=False))

    print("\n--- TOP 10 TECHNICAL SKILLS ---")
    if len(top_skills) > 0:
        print(top_skills.head(10).to_string(index=False))

    print("\n--- TOP 10 JOB TITLES ---")
    print(top_titles.head(10).to_string(index=False))

    print("\n--- TOP 10 LOCATIONS ---")
    print(top_locations.head(10).to_string(index=False))

    print("\n--- EXPERIENCE LEVEL DISTRIBUTION ---")
    print(experience_levels.to_string(index=False))

    print("\n--- WORK TYPE DISTRIBUTION ---")
    print(work_type.to_string(index=False))

    print("\n--- REMOTE STATUS BREAKDOWN ---")
    print(remote_jobs.to_string(index=False))

    print("\n--- SALARY DESCRIPTIVE METRICS ---")
    print(salary_summary.to_string(index=False))

    print("\n--- SALARY BY EXPERIENCE LEVEL ---")
    print(salary_by_exp.to_string(index=False))

    print("\n--- SALARY BY WORK TYPE ---")
    print(salary_by_wt.to_string(index=False))

    print("\n" + "=" * 60)
    print("EDA COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print(f"All generated CSV artifacts are saved in: {output_dir}")

    return {
        "dataset_summary": dataset_summary,
        "top_skills": top_skills,
        "top_titles": top_titles,
        "top_locations": top_locations,
        "top_companies": top_companies,
        "experience_levels": experience_levels,
        "work_type": work_type,
        "remote_jobs": remote_jobs,
        "salary_summary": salary_summary,
        "salary_by_experience": salary_by_exp,
        "salary_by_work_type": salary_by_wt,
        "location_summary": location_counts,
    }


if __name__ == "__main__":
    run_analysis()