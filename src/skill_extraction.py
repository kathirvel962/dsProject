import pandas as pd
import re
from collections import Counter
import os

# ============================================================
# SkillSight - Skill Extraction
# ============================================================

INPUT_FILE = "data/cleaned_jobs.csv"
OUTPUT_FILE = "outputs/results/skill_frequency.csv"

print("=" * 60)
print("SKILLSIGHT - SKILL EXTRACTION")
print("=" * 60)


# ============================================================
# 1. Load cleaned dataset
# ============================================================

print("\nLoading cleaned dataset...")

df = pd.read_csv(INPUT_FILE)

print("Total job postings:", len(df))


# ============================================================
# 2. Skill dictionary
# ============================================================

skills = {

    # Programming Languages
    "Python": [
        "python"
    ],

    "Java": [
        "java"
    ],

    "C++": [
        "c++"
    ],

    "C#": [
        "c#",
        "c sharp"
    ],

    "JavaScript": [
        "javascript",
        "java script"
    ],

    "TypeScript": [
        "typescript"
    ],

    "PHP": [
        "php"
    ],

    "Ruby": [
        "ruby"
    ],

    "Go": [
        "golang",
        "go programming",
        "go language"
    ],

    "R": [
        "r programming",
        "r language"
    ],


    # Database
    "SQL": [
        "sql"
    ],

    "MySQL": [
        "mysql"
    ],

    "PostgreSQL": [
        "postgresql",
        "postgres"
    ],

    "MongoDB": [
        "mongodb",
        "mongo db"
    ],

    "Oracle": [
        "oracle database",
        "oracle db"
    ],


    # Web Development
    "HTML": [
        "html",
        "html5"
    ],

    "CSS": [
        "css",
        "css3"
    ],

    "React": [
        "react",
        "react.js",
        "reactjs"
    ],

    "Angular": [
        "angular",
        "angular.js",
        "angularjs"
    ],

    "Vue.js": [
        "vue.js",
        "vuejs",
        "vue js"
    ],

    "Node.js": [
        "node.js",
        "nodejs",
        "node js"
    ],

    "Spring Boot": [
        "spring boot"
    ],

    "Django": [
        "django"
    ],

    "Flask": [
        "flask"
    ],


    # Data Science / AI
    "Machine Learning": [
        "machine learning",
        "machine-learning"
    ],

    "Deep Learning": [
        "deep learning",
        "deep-learning"
    ],

    "Artificial Intelligence": [
        "artificial intelligence"
    ],

    "Natural Language Processing": [
        "natural language processing",
        "nlp"
    ],

    "TensorFlow": [
        "tensorflow"
    ],

    "PyTorch": [
        "pytorch"
    ],

    "Pandas": [
        "pandas"
    ],

    "NumPy": [
        "numpy"
    ],

    "Scikit-learn": [
        "scikit-learn",
        "sklearn"
    ],

    "OpenCV": [
        "opencv"
    ],


    # Cloud
    "AWS": [
        "aws",
        "amazon web services"
    ],

    "Azure": [
        "azure",
        "microsoft azure"
    ],

    "Google Cloud": [
        "google cloud",
        "google cloud platform",
        "gcp"
    ],


    # DevOps
    "Docker": [
        "docker"
    ],

    "Kubernetes": [
        "kubernetes",
        "k8s"
    ],

    "Jenkins": [
        "jenkins"
    ],

    "Terraform": [
        "terraform"
    ],

    "Git": [
        "git"
    ],

    "GitHub": [
        "github"
    ],

    "Linux": [
        "linux"
    ],


    # Data / BI
    "Excel": [
        "excel",
        "microsoft excel"
    ],

    "Power BI": [
        "power bi"
    ],

    "Tableau": [
        "tableau"
    ],

    "Apache Spark": [
        "apache spark",
        "spark"
    ],

    "Hadoop": [
        "hadoop"
    ],

    "Databricks": [
        "databricks"
    ],

    "Kafka": [
        "apache kafka",
        "kafka"
    ],


    # APIs / Software
    "REST API": [
        "rest api",
        "restful api",
        "restful"
    ],

    "GraphQL": [
        "graphql"
    ],

    "Microservices": [
        "microservices",
        "microservices architecture"
    ]
}


# ============================================================
# 3. Prepare descriptions
# ============================================================

print("\nPreparing job descriptions...")

df["description"] = (
    df["description"]
    .fillna("")
    .astype(str)
    .str.lower()
)


# ============================================================
# 4. Extract skills
# ============================================================

print("Extracting skills from job descriptions...")
print("Please wait...\n")

skill_counter = Counter()


for description in df["description"]:

    # Skills found in this particular job
    found_skills = set()

    for skill, keywords in skills.items():

        for keyword in keywords:

            # Create safe search pattern
            pattern = (
                r"(?<!\w)"
                + re.escape(keyword.lower())
                + r"(?!\w)"
            )

            if re.search(pattern, description):

                found_skills.add(skill)

                # No need to check other keywords
                # for the same skill
                break

    # Count each skill only once per job
    for skill in found_skills:
        skill_counter[skill] += 1


# ============================================================
# 5. Create result dataframe
# ============================================================

skill_df = pd.DataFrame(
    skill_counter.items(),
    columns=[
        "Skill",
        "Job_Count"
    ]
)


# ============================================================
# 6. Sort by demand
# ============================================================

skill_df = skill_df.sort_values(
    by="Job_Count",
    ascending=False
).reset_index(drop=True)


# ============================================================
# 7. Calculate percentage
# ============================================================

total_jobs = len(df)

skill_df["Demand_Percentage"] = (
    skill_df["Job_Count"] / total_jobs * 100
).round(2)


# ============================================================
# 8. Create output directory
# ============================================================

os.makedirs(
    "outputs/results",
    exist_ok=True
)


# ============================================================
# 9. Save results
# ============================================================

skill_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 10. Display results
# ============================================================

print("=" * 60)
print("TOP 20 IN-DEMAND SKILLS")
print("=" * 60)

print(
    skill_df.head(20).to_string(index=False)
)


# ============================================================
# 11. Summary
# ============================================================

print("\n" + "=" * 60)
print("SKILL EXTRACTION COMPLETED")
print("=" * 60)

print("\nTotal jobs analyzed:", total_jobs)
print("Total skills detected:", len(skill_df))

print("\nResults saved to:")
print(OUTPUT_FILE)

print("\nTop 5 skills:")

for index, row in skill_df.head(5).iterrows():

    print(
        f"{index + 1}. "
        f"{row['Skill']} - "
        f"{row['Job_Count']} jobs "
        f"({row['Demand_Percentage']}%)"
    )