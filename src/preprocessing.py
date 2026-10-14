import os
import pandas as pd

# ============================================================
# SkillSight - Data Preprocessing
# ============================================================

INPUT_FILE = "data/job_postings.csv" if os.path.exists("data/job_postings.csv") else "data/raw_jobs.csv"
OUTPUT_FILE = "data/cleaned_jobs.csv"
SUMMARY_FILE = "outputs/results/preprocessing_summary.csv"

# Relevant columns to retain in cleaned dataset
COLUMNS = [
    "job_id",
    "company_id",
    "title",
    "description",
    "min_salary",
    "med_salary",
    "max_salary",
    "salary",
    "has_salary",
    "pay_period",
    "formatted_work_type",
    "location",
    "applies",
    "views",
    "remote_allowed",
    "remote_status",
    "is_remote",
    "formatted_experience_level",
    "skills_desc",
    "application_type",
    "work_type",
    "currency",
    "compensation_type",
]


def clean_job_data(df: pd.DataFrame) -> pd.DataFrame:
    """Core preprocessing function for job postings data.
    
    Can be called directly from Python scripts or Jupyter notebooks.
    """
    # 1. Deduplicate by job_id
    df = df.drop_duplicates(subset="job_id").copy()

    # 2. Handle missing text & categorical fields
    df["description"] = df["description"].fillna("")
    df["title"] = df["title"].fillna("Unknown")
    df["location"] = df["location"].fillna("Unknown")
    df["formatted_experience_level"] = df["formatted_experience_level"].fillna("Not Specified")

    # 3. Handle engagement metrics
    if "views" in df.columns:
        df["views"] = df["views"].fillna(0)
    if "applies" in df.columns:
        df["applies"] = df["applies"].fillna(0)

    # 4. Clean text fields
    df["title"] = df["title"].astype(str).str.strip()
    df["description"] = (
        df["description"]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )
    df["location"] = df["location"].astype(str).str.strip()

    # 5. Process salary information & create unified salary
    df["salary"] = df["med_salary"]
    df["salary"] = df["salary"].fillna(
        (df["min_salary"] + df["max_salary"]) / 2
    )
    # Derived field: boolean indicator for salary presence
    df["has_salary"] = df["salary"].notna()

    # 6. Process remote-work information
    df["remote_status"] = df["remote_allowed"].map({
        1: "Remote",
        0: "On-site",
    })
    df["remote_status"] = df["remote_status"].fillna("Not Specified")
    # Derived field: boolean indicator for remote jobs
    df["is_remote"] = df["remote_status"] == "Remote"

    # 7. Select relevant columns
    available_cols = [col for col in COLUMNS if col in df.columns]
    df = df[available_cols]

    return df


def run_preprocessing(input_file: str = INPUT_FILE, output_file: str = OUTPUT_FILE, summary_file: str = SUMMARY_FILE):
    """Execute complete preprocessing pipeline from raw file to cleaned CSV and summary."""
    print("=" * 60)
    print("SKILLSIGHT - DATA PREPROCESSING PIPELINE")
    print("=" * 60)

    # 1. Load raw dataset
    print(f"\nLoading raw dataset from: {input_file}")
    df_raw = pd.read_csv(input_file)
    before_rows, before_cols = df_raw.shape
    print(f"Original dataset shape: {before_rows:,} rows, {before_cols} columns")

    # Record before stats
    before_dup_count = df_raw.duplicated(subset="job_id").sum()
    before_missing_desc = df_raw["description"].isnull().sum()
    before_missing_title = df_raw["title"].isnull().sum()
    before_missing_loc = df_raw["location"].isnull().sum()
    before_missing_exp = df_raw["formatted_experience_level"].isnull().sum()
    raw_salary_calc = df_raw["med_salary"].fillna((df_raw["min_salary"] + df_raw["max_salary"]) / 2)
    before_has_salary = raw_salary_calc.notna().sum()
    before_remote_jobs = (df_raw["remote_allowed"] == 1).sum()

    # 2. Run cleaning
    print("\nRunning cleaning & transformations...")
    df_cleaned = clean_job_data(df_raw)
    after_rows, after_cols = df_cleaned.shape

    # 3. Save cleaned dataset
    print(f"\nSaving cleaned dataset to: {output_file}")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df_cleaned.to_csv(output_file, index=False)

    # 4. Generate before/after summary
    print(f"Generating preprocessing summary to: {summary_file}")
    os.makedirs(os.path.dirname(summary_file), exist_ok=True)

    summary_data = {
        "Metric": [
            "Total Rows",
            "Total Columns",
            "Duplicate Job IDs",
            "Missing (Null) Descriptions",
            "Missing (Null) Job Titles",
            "Missing (Null) Locations",
            "Missing (Null) Experience Levels",
            "Missing (Null) Views",
            "Missing (Null) Applies",
            "Jobs With Calculated Salary",
            "Remote Jobs Identified",
        ],
        "Before_Preprocessing": [
            before_rows,
            before_cols,
            before_dup_count,
            before_missing_desc,
            before_missing_title,
            before_missing_loc,
            before_missing_exp,
            df_raw["views"].isnull().sum() if "views" in df_raw.columns else 0,
            df_raw["applies"].isnull().sum() if "applies" in df_raw.columns else 0,
            before_has_salary,
            before_remote_jobs,
        ],
        "After_Preprocessing": [
            after_rows,
            after_cols,
            df_cleaned.duplicated(subset="job_id").sum(),
            df_cleaned["description"].isnull().sum(),
            df_cleaned["title"].isnull().sum(),
            df_cleaned["location"].isnull().sum(),
            df_cleaned["formatted_experience_level"].isnull().sum(),
            df_cleaned["views"].isnull().sum(),
            df_cleaned["applies"].isnull().sum(),
            df_cleaned["has_salary"].sum(),
            df_cleaned["is_remote"].sum(),
        ],
    }
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(summary_file, index=False)

    # 5. Display verification results
    print("\n" + "=" * 60)
    print("PREPROCESSING VERIFICATION")
    print("=" * 60)
    print(f"Row count             : {after_rows:,}")
    print(f"Column count          : {after_cols}")
    print(f"Duplicates removed    : {before_rows - after_rows}")
    print(f"Jobs with salary info : {df_cleaned['has_salary'].sum():,} ({df_cleaned['has_salary'].mean()*100:.2f}%)")
    print(f"Remote jobs identified: {df_cleaned['is_remote'].sum():,} ({df_cleaned['is_remote'].mean()*100:.2f}%)")
    print(f"Cleaned output file   : {output_file}")
    print(f"Summary output file   : {summary_file}")

    print("\nMissing values in cleaned dataset:")
    print(df_cleaned.isnull().sum())

    print("\nPreprocessing summary table:")
    print(summary_df.to_string(index=False))

    return df_cleaned


if __name__ == "__main__":
    run_preprocessing()