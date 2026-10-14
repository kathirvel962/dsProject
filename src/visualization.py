"""SkillSight - Module 5: Data Visualization.

Generates professional visual charts based on EDA outputs:
1. Top 15 Technical Skills (Horizontal Bar Chart)
2. Top 15 Job Titles (Horizontal Bar Chart)
3. Top 15 Locations (Horizontal Bar Chart)
4. Experience Level Distribution (Bar Chart)
5. Work Type Distribution (Bar Chart)
6. Remote Work Distribution (Bar Chart)
7. Salary Distribution (Histogram with 99th Percentile Clipping)
8. Salary by Experience Level (Bar Chart)
9. Salary by Work Type (Bar Chart)
10. Top Skills Demand (Horizontal Bar Chart with Count and Percentage)
"""

import os
import sys

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless execution
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Paths configuration
RESULTS_DIR = "outputs/results"
CHARTS_DIR = "outputs/charts"
CLEANED_JOBS_FILE = "data/cleaned_jobs.csv"

# Global visual style settings
PRIMARY_COLOR = "#2b5c8f"
SECONDARY_COLOR = "#4a86b8"
ACCENT_COLOR = "#d95f02"


def setup_chart_style(ax, grid_axis="y"):
    """Apply consistent, professional styling across all charts."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#cccccc")
    ax.spines["bottom"].set_color("#cccccc")
    ax.set_axisbelow(True)
    if grid_axis:
        ax.grid(True, linestyle="--", alpha=0.5, axis=grid_axis)


def plot_top_skills(input_path: str, output_path: str):
    """1. Top 15 Technical Skills horizontal bar chart."""
    df = pd.read_csv(input_path).head(15).iloc[::-1]  # Highest at top

    fig, ax = plt.subplots(figsize=(10, 7))
    bars = ax.barh(df["Skill"], df["Job_Count"], color=PRIMARY_COLOR, edgecolor="none", height=0.65)

    # Add data labels
    for bar, pct in zip(bars, df["Demand_Percentage"]):
        width = bar.get_width()
        ax.text(
            width + 25,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width):,} ({pct:.1f}%)",
            va="center",
            ha="left",
            fontsize=9,
            color="#333333",
        )

    ax.set_xlim(0, df["Job_Count"].max() * 1.15)
    ax.set_title("Top 15 Most In-Demand Technical Skills", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Number of Job Postings", fontsize=11, labelpad=10)
    ax.set_ylabel("Technical Skill", fontsize=11, labelpad=10)
    setup_chart_style(ax, grid_axis="x")

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Generated: {output_path}")


def plot_top_job_titles(input_path: str, output_path: str):
    """2. Top 15 Job Titles horizontal bar chart."""
    df = pd.read_csv(input_path).head(15).iloc[::-1]

    fig, ax = plt.subplots(figsize=(11, 7))
    bars = ax.barh(df["Job_Title"], df["Job_Count"], color=PRIMARY_COLOR, edgecolor="none", height=0.65)

    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 1.0,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width):,}",
            va="center",
            ha="left",
            fontsize=9,
            color="#333333",
        )

    ax.set_xlim(0, df["Job_Count"].max() * 1.12)
    ax.set_title("Top 15 Most Frequent Job Titles", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Number of Job Postings", fontsize=11, labelpad=10)
    ax.set_ylabel("Job Title", fontsize=11, labelpad=10)
    setup_chart_style(ax, grid_axis="x")

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Generated: {output_path}")


def plot_top_locations(input_path: str, output_path: str):
    """3. Top 15 Locations horizontal bar chart."""
    df = pd.read_csv(input_path).head(15).iloc[::-1]

    fig, ax = plt.subplots(figsize=(10, 7))
    bars = ax.barh(df["Location"], df["Job_Count"], color=PRIMARY_COLOR, edgecolor="none", height=0.65)

    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 15,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width):,}",
            va="center",
            ha="left",
            fontsize=9,
            color="#333333",
        )

    ax.set_xlim(0, df["Job_Count"].max() * 1.12)
    ax.set_title("Top 15 Job Posting Locations", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Number of Job Postings", fontsize=11, labelpad=10)
    ax.set_ylabel("Location", fontsize=11, labelpad=10)
    setup_chart_style(ax, grid_axis="x")

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Generated: {output_path}")


def plot_experience_levels(input_path: str, output_path: str):
    """4. Experience Level Distribution bar chart."""
    df = pd.read_csv(input_path)

    fig, ax = plt.subplots(figsize=(9, 6))
    bars = ax.bar(df["Experience_Level"], df["Job_Count"], color=PRIMARY_COLOR, edgecolor="none", width=0.6)

    for bar, pct in zip(bars, df["Percentage"]):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 80,
            f"{int(height):,}\n({pct:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#333333",
        )

    ax.set_ylim(0, df["Job_Count"].max() * 1.18)
    ax.set_title("Job Postings by Experience Level", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Experience Level", fontsize=11, labelpad=10)
    ax.set_ylabel("Number of Job Postings", fontsize=11, labelpad=10)
    ax.tick_params(axis="x", rotation=25)
    setup_chart_style(ax, grid_axis="y")

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Generated: {output_path}")


def plot_work_type(input_path: str, output_path: str):
    """5. Work Type Distribution bar chart."""
    df = pd.read_csv(input_path)

    fig, ax = plt.subplots(figsize=(9, 6))
    bars = ax.bar(df["Work_Type"], df["Job_Count"], color=PRIMARY_COLOR, edgecolor="none", width=0.6)

    for bar, pct in zip(bars, df["Percentage"]):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 150,
            f"{int(height):,}\n({pct:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#333333",
        )

    ax.set_ylim(0, df["Job_Count"].max() * 1.15)
    ax.set_title("Distribution of Employment Work Types", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Work Type", fontsize=11, labelpad=10)
    ax.set_ylabel("Number of Job Postings", fontsize=11, labelpad=10)
    ax.tick_params(axis="x", rotation=25)
    setup_chart_style(ax, grid_axis="y")

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Generated: {output_path}")


def plot_remote_jobs(input_path: str, output_path: str):
    """6. Remote Work Distribution bar chart."""
    df = pd.read_csv(input_path)

    fig, ax = plt.subplots(figsize=(7, 6))
    colors = [PRIMARY_COLOR, SECONDARY_COLOR]
    bars = ax.bar(df["Remote_Status"], df["Job_Count"], color=colors[: len(df)], edgecolor="none", width=0.5)

    for bar, pct in zip(bars, df["Percentage"]):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 200,
            f"{int(height):,} ({pct:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color="#333333",
        )

    ax.set_ylim(0, df["Job_Count"].max() * 1.15)
    ax.set_title("Remote vs. Non-Remote Work Distribution", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Remote Status", fontsize=11, labelpad=10)
    ax.set_ylabel("Number of Job Postings", fontsize=11, labelpad=10)
    setup_chart_style(ax, grid_axis="y")

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Generated: {output_path}")


def plot_salary_distribution(cleaned_jobs_path: str, output_path: str):
    """7. Salary Distribution histogram with percentile-based visualization clipping.
    
    Extreme salary values (> 99th percentile, ~$275,000 up to $1,050,000) are clipped
    strictly for plotting readability so the distribution shape is clearly visible.
    The original salary data remains unaltered.
    """
    df = pd.read_csv(cleaned_jobs_path, usecols=["salary"])
    valid_salary = df["salary"].dropna()
    valid_salary = valid_salary[(valid_salary > 0) & np.isfinite(valid_salary)]

    # Compute descriptive metrics on valid data
    mean_val = valid_salary.mean()
    median_val = valid_salary.median()
    p99 = valid_salary.quantile(0.99)

    # Filter for visualization range
    vis_salary = valid_salary[valid_salary <= p99]

    fig, ax = plt.subplots(figsize=(10, 6))
    n, bins, patches = ax.hist(
        vis_salary,
        bins=40,
        color=PRIMARY_COLOR,
        edgecolor="#ffffff",
        linewidth=0.5,
        alpha=0.85,
    )

    # Add vertical reference lines for mean and median
    ax.axvline(
        median_val,
        color="#e41a1c",
        linestyle="--",
        linewidth=2,
        label=f"Median: ${median_val:,.0f}",
    )
    ax.axvline(
        mean_val,
        color="#ff7f00",
        linestyle=":",
        linewidth=2,
        label=f"Mean: ${mean_val:,.0f}",
    )

    ax.set_title(
        "Salary Distribution (Clipped at 99th Percentile for Visualization)",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    ax.set_xlabel("Salary (USD)", fontsize=11, labelpad=10)
    ax.set_ylabel("Number of Job Postings", fontsize=11, labelpad=10)
    ax.legend(frameon=True, facecolor="white", edgecolor="#cccccc", fontsize=10)
    setup_chart_style(ax, grid_axis="y")

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Generated: {output_path}")


def plot_salary_by_experience(input_path: str, output_path: str):
    """8. Salary by Experience Level bar chart."""
    df = pd.read_csv(input_path)

    # Sort logically by salary ascending to illustrate seniority progression
    df = df.sort_values(by="Average_Salary", ascending=True).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(
        df["Experience_Level"],
        df["Average_Salary"],
        color=PRIMARY_COLOR,
        edgecolor="none",
        width=0.6,
    )

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 2500,
            f"${int(height):,}",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color="#333333",
        )

    ax.set_ylim(0, df["Average_Salary"].max() * 1.15)
    ax.set_title("Average Salary by Experience Level", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Experience Level", fontsize=11, labelpad=10)
    ax.set_ylabel("Average Salary (USD)", fontsize=11, labelpad=10)
    ax.tick_params(axis="x", rotation=25)
    setup_chart_style(ax, grid_axis="y")

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Generated: {output_path}")


def plot_salary_by_work_type(input_path: str, output_path: str):
    """9. Salary by Work Type bar chart."""
    df = pd.read_csv(input_path)
    df = df.sort_values(by="Average_Salary", ascending=True).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(9, 6))
    bars = ax.bar(
        df["Work_Type"],
        df["Average_Salary"],
        color=PRIMARY_COLOR,
        edgecolor="none",
        width=0.6,
    )

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1500,
            f"${int(height):,}",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color="#333333",
        )

    ax.set_ylim(0, df["Average_Salary"].max() * 1.15)
    ax.set_title("Average Salary by Work Type", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Work Type", fontsize=11, labelpad=10)
    ax.set_ylabel("Average Salary (USD)", fontsize=11, labelpad=10)
    ax.tick_params(axis="x", rotation=25)
    setup_chart_style(ax, grid_axis="y")

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Generated: {output_path}")


def plot_skill_demand(input_path: str, output_path: str):
    """10. Technical Skill Demand visualization."""
    df = pd.read_csv(input_path).head(15).iloc[::-1]

    fig, ax = plt.subplots(figsize=(10, 7))
    bars = ax.barh(df["Skill"], df["Job_Count"], color=SECONDARY_COLOR, edgecolor="none", height=0.65)

    for bar, pct in zip(bars, df["Demand_Percentage"]):
        width = bar.get_width()
        ax.text(
            width + 25,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width):,} postings ({pct:.1f}% demand)",
            va="center",
            ha="left",
            fontsize=9,
            color="#333333",
        )

    ax.set_xlim(0, df["Job_Count"].max() * 1.25)
    ax.set_title("Technical Skill Market Demand & Share", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Job Count (Demand Volume)", fontsize=11, labelpad=10)
    ax.set_ylabel("Technical Skill", fontsize=11, labelpad=10)
    setup_chart_style(ax, grid_axis="x")

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Generated: {output_path}")


def generate_all_charts():
    """Execute complete chart generation pipeline."""
    os.makedirs(CHARTS_DIR, exist_ok=True)

    charts = [
        ("Top 15 Technical Skills", "top_skills.png", lambda: plot_top_skills(os.path.join(RESULTS_DIR, "top_skills.csv"), os.path.join(CHARTS_DIR, "top_skills.png"))),
        ("Top 15 Job Titles", "top_job_titles.png", lambda: plot_top_job_titles(os.path.join(RESULTS_DIR, "top_job_titles.csv"), os.path.join(CHARTS_DIR, "top_job_titles.png"))),
        ("Top 15 Locations", "top_locations.png", lambda: plot_top_locations(os.path.join(RESULTS_DIR, "top_locations.csv"), os.path.join(CHARTS_DIR, "top_locations.png"))),
        ("Experience Level Distribution", "experience_levels.png", lambda: plot_experience_levels(os.path.join(RESULTS_DIR, "experience_levels.csv"), os.path.join(CHARTS_DIR, "experience_levels.png"))),
        ("Work Type Distribution", "work_type.png", lambda: plot_work_type(os.path.join(RESULTS_DIR, "work_type.csv"), os.path.join(CHARTS_DIR, "work_type.png"))),
        ("Remote Work Distribution", "remote_jobs.png", lambda: plot_remote_jobs(os.path.join(RESULTS_DIR, "remote_jobs.csv"), os.path.join(CHARTS_DIR, "remote_jobs.png"))),
        ("Salary Distribution", "salary_distribution.png", lambda: plot_salary_distribution(CLEANED_JOBS_FILE, os.path.join(CHARTS_DIR, "salary_distribution.png"))),
        ("Salary by Experience Level", "salary_by_experience.png", lambda: plot_salary_by_experience(os.path.join(RESULTS_DIR, "salary_by_experience.csv"), os.path.join(CHARTS_DIR, "salary_by_experience.png"))),
        ("Salary by Work Type", "salary_by_work_type.png", lambda: plot_salary_by_work_type(os.path.join(RESULTS_DIR, "salary_by_work_type.csv"), os.path.join(CHARTS_DIR, "salary_by_work_type.png"))),
        ("Top Skills Demand", "skill_demand.png", lambda: plot_skill_demand(os.path.join(RESULTS_DIR, "top_skills.csv"), os.path.join(CHARTS_DIR, "skill_demand.png"))),
    ]

    print("=" * 60)
    print("SKILLSIGHT - DATA VISUALIZATION PIPELINE (MODULE 5)")
    print("=" * 60)
    print(f"\nSource EDA results: {RESULTS_DIR}")
    print(f"Target charts folder: {CHARTS_DIR}\n")

    generated = []
    for idx, (name, filename, func) in enumerate(charts, 1):
        print(f"[{idx}/{len(charts)}] Generating {name}...")
        func()
        generated.append(filename)

    print("\n" + "=" * 60)
    print("VISUALIZATION COMPLETED")
    print("=" * 60)
    print("\nCharts generated:")
    for i, chart in enumerate(generated, 1):
        print(f"{i}. {chart}")

    print(f"\nTotal charts generated: {len(generated)}")

    print("\nComplete visualization workflow:")
    print("EDA CSV Results")
    print("       ↓")
    print("     Pandas")
    print("       ↓")
    print("   Matplotlib")
    print("       ↓")
    print("   PNG Charts")
    print("       ↓")
    print("outputs/charts/")


if __name__ == "__main__":
    generate_all_charts()
