"""SkillSight - Module 6: Machine Learning (Salary Prediction).

Implements an explainable Random Forest regression pipeline to predict job salaries:
1. Data Inspection & Quality Filtering (distinguishing Analysis Data from ML Data)
2. Feature Engineering & Selection (Experience, Work Type, Remote Status, Location, Job Category)
3. Categorical Encoding via ColumnTransformer (OneHotEncoder with handle_unknown='ignore')
4. Train/Test Split (80/20 with fixed random state)
5. Model Training (RandomForestRegressor)
6. Model Evaluation (MAE, RMSE, R²)
7. Complete Pipeline Serialization (joblib) for Streamlit Dashboard Integration
8. Summary Artifacts Generation (ml_results.csv, ml_summary.csv)
"""

import os
import sys

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import re
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# Paths configuration
DATA_FILE = "data/cleaned_jobs.csv"
OUTPUT_DIR = "outputs/results"
MODEL_FILE = os.path.join(OUTPUT_DIR, "salary_model.pkl")
RESULTS_FILE = os.path.join(OUTPUT_DIR, "ml_results.csv")
SUMMARY_FILE = os.path.join(OUTPUT_DIR, "ml_summary.csv")


def categorize_title(title: str) -> str:
    """Extract a simple, explainable high-level job category from the raw job title."""
    t = str(title).lower()
    if re.search(r"data|analytics|machine learning|ai\b|scientist|bi\b|analyst", t):
        return "Data & Analytics"
    elif re.search(
        r"software|developer|engineer|programmer|tech|architect|devops|cloud|backend|frontend|fullstack",
        t,
    ):
        return "Software & Engineering"
    elif re.search(r"sales|account|retail|business development", t):
        return "Sales & Account Management"
    elif re.search(r"manager|director|lead|head|supervisor|executive|vp|president", t):
        return "Management & Leadership"
    elif re.search(r"finance|accounting|accountant|audit|tax", t):
        return "Finance & Accounting"
    elif re.search(r"hr|human resources|recruiter|talent", t):
        return "Human Resources"
    elif re.search(r"admin|assistant|coordinator|clerk|customer", t):
        return "Operations & Administrative"
    else:
        return "Other"


def prepare_ml_data(df: pd.DataFrame):
    """Inspect and filter salary data specifically for Machine Learning.
    
    DATA USED FOR ANALYSIS vs. DATA USED FOR ML:
    - Analysis Data: All 6,502 non-null salary records in cleaned_jobs.csv, including
      hourly wages ($10 - $225) and extreme multi-million dollar outliers.
    - ML Training Data: Validated annual salary postings ($10,000 - $500,000). Hourly
      wages (< $1,000) are excluded to avoid scale contamination, and extreme outliers
      (> $500,000) are trimmed to ensure robust generalization.
    """
    print("=" * 60)
    print("SKILLSIGHT - MACHINE LEARNING PIPELINE (MODULE 6)")
    print("=" * 60)

    total_records = len(df)
    raw_salary_count = df["salary"].notna().sum()
    print(f"\n[Step 1] Inspecting Data Quality:")
    print(f"- Total job records: {total_records:,}")
    print(f"- Non-null salary records (Analysis Data): {raw_salary_count:,}")

    # Explicit filtering criteria for ML dataset
    min_annual_salary = 10000.0
    max_annual_salary = 500000.0

    ml_mask = (
        df["salary"].notna()
        & (df["salary"] >= min_annual_salary)
        & (df["salary"] <= max_annual_salary)
        & np.isfinite(df["salary"])
    )
    df_ml = df[ml_mask].copy()

    excluded_low = (df["salary"].notna() & (df["salary"] < min_annual_salary)).sum()
    excluded_high = (df["salary"].notna() & (df["salary"] > max_annual_salary)).sum()

    print(f"- ML Filtering Criteria:")
    print(f"  * Minimum Annual Salary threshold: ${min_annual_salary:,.0f} (filters out hourly wages < $1,000)")
    print(f"  * Maximum Annual Salary threshold: ${max_annual_salary:,.0f} (filters extreme executive outliers)")
    print(f"  * Excluded hourly / low wages: {excluded_low:,}")
    print(f"  * Excluded extreme outliers: {excluded_high:,}")
    print(f"- Total Valid ML Samples: {len(df_ml):,}")

    # Feature Engineering
    print("\n[Step 2] Feature Engineering & Selection:")
    df_ml["job_category"] = df_ml["title"].apply(categorize_title)

    # Impute missing categorical values cleanly
    df_ml["formatted_experience_level"] = (
        df_ml["formatted_experience_level"]
        .fillna("Not Specified")
        .replace(r"^\s*$", "Not Specified", regex=True)
    )
    df_ml["formatted_work_type"] = (
        df_ml["formatted_work_type"]
        .fillna("Not Specified")
        .replace(r"^\s*$", "Not Specified", regex=True)
    )
    df_ml["remote_status"] = (
        df_ml["remote_status"]
        .fillna("Not Specified")
        .replace(r"^\s*$", "Not Specified", regex=True)
    )

    # Handle location cardinality by preserving top regional employment hubs
    top_locations = df_ml["location"].value_counts().head(30).index.tolist()
    df_ml["clean_location"] = df_ml["location"].apply(
        lambda loc: loc if loc in top_locations else "Other"
    )

    feature_cols = [
        "formatted_experience_level",
        "formatted_work_type",
        "remote_status",
        "clean_location",
        "job_category",
    ]

    X = df_ml[feature_cols]
    y = df_ml["salary"]

    print(f"- Features Selected ({len(feature_cols)}): {', '.join(feature_cols)}")
    print(f"- Target: salary (Annual USD)")

    return X, y, feature_cols, top_locations


def build_and_train_model(X: pd.DataFrame, y: pd.Series, feature_cols: list):
    """Build preprocessing + RandomForestRegressor pipeline, train and evaluate."""
    print("\n[Step 3] Splitting Dataset into Train/Test Sets (80/20):")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    print(f"- Training samples: {len(X_train):,}")
    print(f"- Testing samples:  {len(X_test):,}")

    # Build One-Hot Encoder pipeline that handles unseen categories gracefully
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                feature_cols,
            )
        ]
    )

    # Scikit-learn Pipeline encapsulating preprocessing and regressor
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=100,
                    random_state=42,
                    max_depth=12,
                    min_samples_leaf=2,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    print("\n[Step 4] Training RandomForestRegressor Model...")
    pipeline.fit(X_train, y_train)
    print("Model training completed successfully.")

    print("\n[Step 5] Evaluating Model on Test Dataset:")
    predictions = pipeline.predict(X_test)

    mae = float(mean_absolute_error(y_test, predictions))
    rmse = float(np.sqrt(mean_squared_error(y_test, predictions)))
    r2 = float(r2_score(y_test, predictions))

    print(f"- Mean Absolute Error (MAE):     ${mae:,.2f}")
    print(f"- Root Mean Squared Error (RMSE): ${rmse:,.2f}")
    print(f"- R-squared (R²):                {r2:.4f}")

    return pipeline, len(X_train), len(X_test), mae, rmse, r2


def save_artifacts(pipeline, train_count: int, test_count: int, feature_cols: list, mae: float, rmse: float, r2: float):
    """Save serialized model pipeline and evaluation CSV artifacts."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Save complete pipeline with joblib
    joblib.dump(pipeline, MODEL_FILE)
    print(f"\n[Step 6] Saved complete model pipeline to: {MODEL_FILE}")

    # 2. Save ml_results.csv
    features_str = ", ".join(feature_cols)
    results_df = pd.DataFrame({
        "Metric": [
            "Model",
            "Training Samples",
            "Testing Samples",
            "Features Used",
            "MAE",
            "RMSE",
            "R2",
        ],
        "Value": [
            "RandomForestRegressor",
            str(train_count),
            str(test_count),
            features_str,
            f"{mae:.2f}",
            f"{rmse:.2f}",
            f"{r2:.4f}",
        ],
    })
    results_df.to_csv(RESULTS_FILE, index=False)
    print(f"Saved evaluation metrics to: {RESULTS_FILE}")

    # 3. Save ml_summary.csv
    summary_df = pd.DataFrame({
        "Metric": [
            "Problem",
            "Target",
            "Model",
            "Features",
            "Training Samples",
            "Testing Samples",
            "MAE",
            "RMSE",
            "R2",
        ],
        "Value": [
            "Salary Prediction",
            "salary",
            "RandomForestRegressor",
            features_str,
            str(train_count),
            str(test_count),
            f"{mae:.2f}",
            f"{rmse:.2f}",
            f"{r2:.4f}",
        ],
    })
    summary_df.to_csv(SUMMARY_FILE, index=False)
    print(f"Saved model summary to: {SUMMARY_FILE}")


def run_ml_pipeline():
    """Main execution entrypoint for Module 6."""
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Input file '{DATA_FILE}' not found.")

    df = pd.read_csv(DATA_FILE)
    X, y, feature_cols, top_locations = prepare_ml_data(df)

    pipeline, train_count, test_count, mae, rmse, r2 = build_and_train_model(
        X, y, feature_cols
    )

    save_artifacts(pipeline, train_count, test_count, feature_cols, mae, rmse, r2)

    features_formatted = ", ".join(feature_cols)

    # Final summary display
    print("\n" + "=" * 60)
    print("MACHINE LEARNING COMPLETED")
    print("=" * 60)
    print("\nProblem:\nSalary Prediction\n")
    print("Model:\nRandomForestRegressor\n")
    print(f"Training samples:\n{train_count:,}\n")
    print(f"Testing samples:\n{test_count:,}\n")
    print(f"Features:\n{features_formatted}\n")
    print(f"MAE:\n${mae:,.2f}\n")
    print(f"RMSE:\n${rmse:,.2f}\n")
    print(f"R²:\n{r2:.4f}\n")
    print(f"Model:\n{MODEL_FILE}\n")
    print(f"Results:\n{RESULTS_FILE}\n")

    print("Also show the workflow:\n")
    print("Cleaned Dataset")
    print("       ↓")
    print("Valid Salary Data")
    print("       ↓")
    print("Feature Selection")
    print("       ↓")
    print("Categorical Encoding")
    print("       ↓")
    print("Train/Test Split")
    print("       ↓")
    print("Random Forest")
    print("       ↓")
    print("Prediction")
    print("       ↓")
    print("MAE / RMSE / R²")


if __name__ == "__main__":
    run_ml_pipeline()
