"""SkillSight - User Profile & Career Benchmark Module

Manages academic credentials, categorized technical skills with proficiency levels,
career preferences, and standard job-market role benchmarks.
"""

from typing import Dict, List, Any, Optional
from src.database import get_connection

# Comprehensive categorized taxonomy of technical skills
SKILL_TAXONOMY = {
    "Programming Languages": [
        "Python", "Java", "C", "C++", "C#", "JavaScript", "TypeScript",
        "Go", "R", "PHP", "Ruby", "SQL"
    ],
    "Databases": [
        "MySQL", "PostgreSQL", "MongoDB", "Oracle", "SQL Server", "Redis"
    ],
    "Frameworks & Web": [
        "React", "Angular", "Vue.js", "Node.js", "Spring Boot", "Django",
        "Flask", "HTML", "CSS", "Express.js", "FastAPI"
    ],
    "AI & Data Science": [
        "Machine Learning", "Deep Learning", "Artificial Intelligence",
        "Natural Language Processing", "Computer Vision", "Pandas",
        "NumPy", "Scikit-learn", "TensorFlow", "PyTorch"
    ],
    "Cloud Computing": [
        "AWS", "Azure", "Google Cloud"
    ],
    "DevOps & Infrastructure": [
        "Docker", "Kubernetes", "Jenkins", "GitHub Actions", "Terraform",
        "Git", "GitHub", "Linux"
    ],
    "Analytics, BI & Architecture": [
        "Excel", "Power BI", "Tableau", "Apache Spark", "Hadoop",
        "Databricks", "Kafka", "REST API", "GraphQL", "Microservices"
    ]
}

ALL_TAXONOMY_SKILLS = sorted({
    skill for cat_skills in SKILL_TAXONOMY.values() for skill in cat_skills
})

# Predefined standard career roles
PREDEFINED_ROLES = [
    "Data Scientist",
    "Data Analyst",
    "Machine Learning Engineer",
    "AI Engineer",
    "Java Developer",
    "Python Developer",
    "Backend Developer",
    "Frontend Developer",
    "Full Stack Developer",
    "Cloud Engineer",
    "DevOps Engineer",
    "Cybersecurity Analyst",
    "Business Analyst",
    "Software Developer"
]

# Benchmark skill profiles for major career roles
ROLE_SKILL_BENCHMARKS: Dict[str, Dict[str, Any]] = {
    "Data Scientist": {
        "core_skills": ["Python", "SQL", "Pandas", "NumPy", "Scikit-learn", "Machine Learning"],
        "recommended_skills": ["Deep Learning", "Natural Language Processing", "TensorFlow", "AWS", "Tableau", "Docker"],
        "description": "Designs statistical models, develops predictive ML pipelines, and extracts insights from complex datasets."
    },
    "Data Analyst": {
        "core_skills": ["SQL", "Excel", "Tableau", "Power BI", "Python", "Pandas"],
        "recommended_skills": ["R", "MySQL", "PostgreSQL", "Statistics", "Google Cloud"],
        "description": "Transforms raw transactional records into actionable business intelligence and automated dashboard reports."
    },
    "Machine Learning Engineer": {
        "core_skills": ["Python", "Machine Learning", "Deep Learning", "PyTorch", "TensorFlow", "Scikit-learn", "Docker"],
        "recommended_skills": ["Kubernetes", "AWS", "Linux", "Git", "REST API", "Microservices"],
        "description": "Deploys, monitors, and optimizes scalable machine learning and deep neural network models in production."
    },
    "AI Engineer": {
        "core_skills": ["Python", "Artificial Intelligence", "Machine Learning", "Deep Learning", "Natural Language Processing", "PyTorch"],
        "recommended_skills": ["TensorFlow", "Docker", "REST API", "Cloud", "Git", "Computer Vision"],
        "description": "Builds intelligent systems utilizing generative AI, foundational models, LLMs, and cognitive vision pipelines."
    },
    "Java Developer": {
        "core_skills": ["Java", "Spring Boot", "SQL", "REST API", "Git"],
        "recommended_skills": ["Microservices", "Docker", "MySQL", "PostgreSQL", "Kafka", "Linux", "AWS"],
        "description": "Architects robust enterprise services, transactional applications, and backend systems utilizing the JVM."
    },
    "Python Developer": {
        "core_skills": ["Python", "Django", "Flask", "SQL", "REST API", "Git"],
        "recommended_skills": ["FastAPI", "Docker", "PostgreSQL", "Redis", "Linux", "AWS"],
        "description": "Develops modern web applications, microservices, automation scripts, and server-side logic."
    },
    "Backend Developer": {
        "core_skills": ["Python", "Java", "SQL", "REST API", "Microservices", "Git", "Node.js"],
        "recommended_skills": ["Docker", "PostgreSQL", "MySQL", "Redis", "Linux", "AWS"],
        "description": "Engineers scalable server architectures, robust database schemas, authentication layers, and API endpoints."
    },
    "Frontend Developer": {
        "core_skills": ["JavaScript", "TypeScript", "React", "HTML", "CSS", "Git"],
        "recommended_skills": ["Angular", "Vue.js", "Node.js", "REST API", "Tailwind CSS"],
        "description": "Creates responsive, aesthetic, and accessible user interfaces with dynamic web application state."
    },
    "Full Stack Developer": {
        "core_skills": ["JavaScript", "TypeScript", "React", "Node.js", "SQL", "HTML", "CSS", "Git", "REST API"],
        "recommended_skills": ["Docker", "Python", "MongoDB", "PostgreSQL", "AWS", "Microservices"],
        "description": "Masters end-to-end development, unifying rich frontend user experiences with performant backend APIs."
    },
    "Cloud Engineer": {
        "core_skills": ["AWS", "Azure", "Google Cloud", "Linux", "Terraform", "Git"],
        "recommended_skills": ["Docker", "Kubernetes", "Python", "Networking", "Jenkins", "Security"],
        "description": "Provisions, maintains, and secures elastic cloud compute, storage, and networking architectures."
    },
    "DevOps Engineer": {
        "core_skills": ["Docker", "Kubernetes", "Linux", "Git", "Jenkins", "AWS", "Terraform"],
        "recommended_skills": ["GitHub Actions", "Python", "Azure", "Microservices", "Kafka"],
        "description": "Automates continuous integration and continuous delivery (CI/CD) pipelines, infrastructure as code, and cluster orchestration."
    },
    "Cybersecurity Analyst": {
        "core_skills": ["Linux", "Python", "Git", "SQL"],
        "recommended_skills": ["AWS", "Azure", "Networking", "Docker", "Security"],
        "description": "Monitors network telemetry, audits access controls, evaluates security postures, and responds to vulnerabilities."
    },
    "Business Analyst": {
        "core_skills": ["Excel", "SQL", "Power BI", "Tableau"],
        "recommended_skills": ["Python", "Pandas", "Agile", "Requirements Analysis"],
        "description": "Bridges corporate strategy and technical execution through process mapping, metric KPIs, and requirement specs."
    },
    "Software Developer": {
        "core_skills": ["Python", "Java", "SQL", "Git", "REST API", "Linux"],
        "recommended_skills": ["Docker", "C++", "C#", "React", "AWS", "Microservices"],
        "description": "Writes clean, modular, and maintainable software code across desktop, cloud, and distributed architectures."
    }
}


def get_user_profile(user_id: int) -> Dict[str, Any]:
    """Retrieve full personal, academic, skill, and career preference details for a user."""
    profile_data = {
        "personal": {},
        "skills": [],
        "preferences": {}
    }

    with get_connection() as conn:
        cursor = conn.cursor()

        # Academic profile
        cursor.execute("""
        SELECT u.name, u.email, p.degree, p.branch, p.academic_year, p.graduation_year,
               p.cgpa, p.education_level, p.certifications, p.projects_summary, p.portfolio_url
        FROM users u
        LEFT JOIN user_profiles p ON u.id = p.user_id
        WHERE u.id = ?;
        """, (user_id,))
        row = cursor.fetchone()
        if row:
            profile_data["personal"] = {
                "name": row["name"],
                "email": row["email"],
                "degree": row["degree"] or "B.Tech",
                "branch": row["branch"] or "Computer Science",
                "academic_year": row["academic_year"] or "3rd Year",
                "graduation_year": row["graduation_year"] or 2026,
                "cgpa": row["cgpa"] if row["cgpa"] is not None else 8.0,
                "education_level": row["education_level"] or "Undergraduate",
                "certifications": row["certifications"] or "",
                "projects_summary": row["projects_summary"] or "",
                "portfolio_url": row["portfolio_url"] or ""
            }

        # Skills with proficiency
        cursor.execute("""
        SELECT skill_name, category, proficiency
        FROM user_skills
        WHERE user_id = ?
        ORDER BY skill_name ASC;
        """, (user_id,))
        rows = cursor.fetchall()
        profile_data["skills"] = [
            {
                "skill_name": r["skill_name"],
                "category": r["category"],
                "proficiency": r["proficiency"]
            }
            for r in rows
        ]

        # Career preferences
        cursor.execute("""
        SELECT preferred_role, preferred_location, work_mode,
               expected_salary_min, expected_salary_max, preferred_industry,
               employment_type, experience_level, career_interests
        FROM career_preferences
        WHERE user_id = ?;
        """, (user_id,))
        p_row = cursor.fetchone()
        if p_row:
            profile_data["preferences"] = {
                "preferred_role": p_row["preferred_role"] or "Data Scientist",
                "preferred_location": p_row["preferred_location"] or "United States",
                "work_mode": p_row["work_mode"] or "Remote",
                "expected_salary_min": p_row["expected_salary_min"] or 70000.0,
                "expected_salary_max": p_row["expected_salary_max"] or 110000.0,
                "preferred_industry": p_row["preferred_industry"] or "Technology & Software",
                "employment_type": p_row["employment_type"] or "Full-time",
                "experience_level": p_row["experience_level"] or "Entry level",
                "career_interests": p_row["career_interests"] or "Machine Learning, Analytics"
            }
        else:
            profile_data["preferences"] = {
                "preferred_role": "Data Scientist",
                "preferred_location": "United States",
                "work_mode": "Remote",
                "expected_salary_min": 70000.0,
                "expected_salary_max": 110000.0,
                "preferred_industry": "Technology & Software",
                "employment_type": "Full-time",
                "experience_level": "Entry level",
                "career_interests": "Machine Learning, Analytics"
            }

    return profile_data


def update_academic_profile(user_id: int, data: Dict[str, Any]) -> bool:
    """Update user's personal and academic records."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Update user name if given
        if "name" in data and data["name"].strip():
            cursor.execute("UPDATE users SET name = ? WHERE id = ?;", (data["name"].strip(), user_id))

        cursor.execute("""
        INSERT INTO user_profiles (
            user_id, degree, branch, academic_year, graduation_year, cgpa,
            education_level, certifications, projects_summary, portfolio_url, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id) DO UPDATE SET
            degree = excluded.degree,
            branch = excluded.branch,
            academic_year = excluded.academic_year,
            graduation_year = excluded.graduation_year,
            cgpa = excluded.cgpa,
            education_level = excluded.education_level,
            certifications = excluded.certifications,
            projects_summary = excluded.projects_summary,
            portfolio_url = excluded.portfolio_url,
            updated_at = CURRENT_TIMESTAMP;
        """, (
            user_id,
            data.get("degree", "B.Tech"),
            data.get("branch", "Computer Science"),
            data.get("academic_year", "3rd Year"),
            int(data.get("graduation_year", 2026)),
            float(data.get("cgpa", 8.0)),
            data.get("education_level", "Undergraduate"),
            data.get("certifications", ""),
            data.get("projects_summary", ""),
            data.get("portfolio_url", "")
        ))
    return True


def update_user_skills(user_id: int, skills_list: List[Dict[str, str]]) -> bool:
    """Replace and update the complete set of skills for a user with proficiency levels."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_skills WHERE user_id = ?;", (user_id,))
        for s in skills_list:
            s_name = s.get("skill_name", "").strip()
            if not s_name:
                continue
            cat = s.get("category", "General")
            prof = s.get("proficiency", "Intermediate")
            if prof not in ("Beginner", "Intermediate", "Advanced"):
                prof = "Intermediate"
            cursor.execute("""
            INSERT INTO user_skills (user_id, skill_name, category, proficiency)
            VALUES (?, ?, ?, ?);
            """, (user_id, s_name, cat, prof))
    return True


def update_career_preferences(user_id: int, data: Dict[str, Any]) -> bool:
    """Update user's career preferences and targets."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO career_preferences (
            user_id, preferred_role, preferred_location, work_mode,
            expected_salary_min, expected_salary_max, preferred_industry,
            employment_type, experience_level, career_interests, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id) DO UPDATE SET
            preferred_role = excluded.preferred_role,
            preferred_location = excluded.preferred_location,
            work_mode = excluded.work_mode,
            expected_salary_min = excluded.expected_salary_min,
            expected_salary_max = excluded.expected_salary_max,
            preferred_industry = excluded.preferred_industry,
            employment_type = excluded.employment_type,
            experience_level = excluded.experience_level,
            career_interests = excluded.career_interests,
            updated_at = CURRENT_TIMESTAMP;
        """, (
            user_id,
            data.get("preferred_role", "Data Scientist"),
            data.get("preferred_location", "United States"),
            data.get("work_mode", "Remote"),
            float(data.get("expected_salary_min", 70000.0)),
            float(data.get("expected_salary_max", 110000.0)),
            data.get("preferred_industry", "Technology & Software"),
            data.get("employment_type", "Full-time"),
            data.get("experience_level", "Entry level"),
            data.get("career_interests", "Machine Learning, Data Systems")
        ))
    return True
