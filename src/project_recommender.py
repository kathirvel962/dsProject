"""SkillSight - Project Recommender Module

Recommends structured, explainable hands-on portfolio projects specifically designed
to bridge the user's identified skill gaps and demonstrate target role competency.
"""

from typing import List, Dict, Any
from src.skill_gap import analyze_skill_gap

# Catalog of curated hands-on portfolio projects mapped to target roles and skills
PROJECT_CATALOG = [
    {
        "title": "Customer Churn Prediction & Retention System",
        "roles": ["Data Scientist", "Machine Learning Engineer", "Data Analyst"],
        "target_skills": ["Python", "Pandas", "Scikit-learn", "Machine Learning", "SQL"],
        "difficulty": "Intermediate",
        "tech_stack": "Python, Scikit-learn, Pandas, Matplotlib, Streamlit",
        "outcome": "Build an end-to-end binary classification pipeline with feature engineering, hyperparameter tuning, ROC-AUC evaluation, and an interactive predictor.",
        "deliverable": "GitHub repository with documented notebook, model pickle, and live web demo."
    },
    {
        "title": "Enterprise Sales & Revenue Analytics Dashboard",
        "roles": ["Data Analyst", "Business Analyst", "Data Scientist"],
        "target_skills": ["SQL", "Excel", "Power BI", "Tableau", "Python"],
        "difficulty": "Beginner to Intermediate",
        "tech_stack": "PostgreSQL, SQL queries, Power BI / Tableau, Excel",
        "outcome": "Transform multi-table relational sales schemas into executive KPI dashboards tracking customer lifetime value, monthly recurring revenue, and regional trends.",
        "deliverable": "Interactive dashboard file (.pbix or Tableau Public link) and analytical insights slide deck."
    },
    {
        "title": "Job Market Intelligence & Salary Prediction Platform",
        "roles": ["Data Scientist", "Machine Learning Engineer", "Full Stack Developer", "Software Developer"],
        "target_skills": ["Python", "Machine Learning", "Pandas", "Streamlit", "SQL", "Docker"],
        "difficulty": "Intermediate to Advanced",
        "tech_stack": "Python, Pandas, Scikit-learn, Streamlit, Docker, Git",
        "outcome": "Architect an explainable data science system featuring text skill extraction, exploratory market analysis, Random Forest regression, and a live user dashboard.",
        "deliverable": "Containerized multi-page web platform deployed with automated AppTest testing."
    },
    {
        "title": "Scalable E-Commerce RESTful Microservices API",
        "roles": ["Java Developer", "Backend Developer", "Software Developer"],
        "target_skills": ["Java", "Spring Boot", "REST API", "Microservices", "Docker", "SQL"],
        "difficulty": "Intermediate to Advanced",
        "tech_stack": "Java 17, Spring Boot, Spring Data JPA, PostgreSQL, Docker, Swagger",
        "outcome": "Develop decoupled microservices handling product catalog, shopping cart, and order checkout with JWT authentication, database migrations, and RESTful documentation.",
        "deliverable": "Production-ready Spring Boot backend with Postman test collection and Docker Compose file."
    },
    {
        "title": "Modern Task & Project Management Web Application",
        "roles": ["Frontend Developer", "Full Stack Developer", "Software Developer"],
        "target_skills": ["JavaScript", "TypeScript", "React", "HTML", "CSS", "Node.js", "Git"],
        "difficulty": "Intermediate",
        "tech_stack": "React 18, TypeScript, Tailwind CSS, Node.js, Express, MongoDB",
        "outcome": "Create a responsive Kanban-style task tracker featuring drag-and-drop state, optimistic UI updates, dark mode theme toggle, and authenticated user workspaces.",
        "deliverable": "Deployed full-stack web application hosted on Vercel/Render with CI/CD GitHub Actions."
    },
    {
        "title": "Automated Cloud CI/CD Pipeline & Infrastructure as Code",
        "roles": ["DevOps Engineer", "Cloud Engineer", "Backend Developer"],
        "target_skills": ["Docker", "Kubernetes", "AWS", "Terraform", "Linux", "Jenkins", "Git"],
        "difficulty": "Advanced",
        "tech_stack": "Docker, Kubernetes (EKS), Terraform, AWS (S3, EC2), GitHub Actions",
        "outcome": "Write declarative Terraform configurations to provision secure VPC networking and compute, automated with a zero-downtime GitHub Actions deployment pipeline.",
        "deliverable": "Clean infrastructure repository with modular Terraform scripts and pipeline architecture diagram."
    },
    {
        "title": "Conversational Document AI & Semantic Search System",
        "roles": ["AI Engineer", "Machine Learning Engineer", "Data Scientist"],
        "target_skills": ["Artificial Intelligence", "Deep Learning", "Natural Language Processing", "Python", "REST API"],
        "difficulty": "Advanced",
        "tech_stack": "Python, PyTorch / HuggingFace Transformers, ChromaDB / FAISS, FastAPI",
        "outcome": "Implement Retrieval-Augmented Generation (RAG) allowing users to upload technical PDFs and query domain knowledge with context-grounded citations.",
        "deliverable": "FastAPI service with vectorized similarity search and benchmark evaluation report."
    }
]


def recommend_projects(user_skills: List[Dict[str, str]], target_role: str) -> List[Dict[str, Any]]:
    """Recommend 3-4 tailored projects based on user's target role and skill gaps."""
    gap_result = analyze_skill_gap(user_skills, target_role)
    missing_skill_names = {item["skill"].lower() for item in gap_result["skills_to_develop"]}

    scored_projects = []

    for proj in PROJECT_CATALOG:
        # Score relevance based on target role match and missing skill overlap
        role_match_score = 3.0 if target_role in proj["roles"] else 1.0
        
        # Count how many of the project's target skills address the user's missing skills
        addressed_skills = [
            skill for skill in proj["target_skills"]
            if skill.lower() in missing_skill_names
        ]
        
        gap_score = len(addressed_skills) * 2.0
        total_score = role_match_score + gap_score

        scored_projects.append({
            "title": proj["title"],
            "target_roles": proj["roles"],
            "difficulty": proj["difficulty"],
            "tech_stack": proj["tech_stack"],
            "outcome": proj["outcome"],
            "deliverable": proj["deliverable"],
            "all_project_skills": proj["target_skills"],
            "skills_developed": addressed_skills if addressed_skills else proj["target_skills"][:3],
            "relevance_score": total_score,
            "why_recommended": (
                f"Directly targets your missing competencies in {', '.join(addressed_skills[:3])} "
                f"while building a demonstrable portfolio asset for {target_role} roles."
                if addressed_skills else
                f"Reinforces core engineering principles and domain deliverables for {target_role} applications."
            )
        })

    # Sort descending by relevance score
    scored_projects.sort(key=lambda x: -x["relevance_score"])
    return scored_projects[:4]
