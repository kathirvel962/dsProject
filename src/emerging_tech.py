"""SkillSight - Emerging Technology Intelligence Module

Provides the "Market-Relevant Technology Radar", categorizing key industry
technologies with verified job-frequency evidence from the dataset, associated roles,
and explainable learning rationales.
"""

from typing import List, Dict, Any
from src.skill_gap import load_market_skill_demand

# Structured domain categories and technologies
RADAR_DOMAINS = {
    "AI & Machine Learning": [
        {
            "technology": "Machine Learning",
            "aliases": ["machine learning"],
            "related_roles": ["Data Scientist", "ML Engineer", "AI Engineer"],
            "related_skills": ["Python", "Scikit-learn", "Pandas", "Mathematics"],
            "why_learn": "Core paradigm shift in modern software, enabling autonomous decision systems and predictive analytics."
        },
        {
            "technology": "Deep Learning",
            "aliases": ["deep learning"],
            "related_roles": ["Computer Vision Engineer", "NLP Scientist", "AI Researcher"],
            "related_skills": ["PyTorch", "TensorFlow", "Neural Networks"],
            "why_learn": "Foundation for modern vision, natural language generation, and deep speech recognition."
        },
        {
            "technology": "Natural Language Processing",
            "aliases": ["natural language processing", "nlp"],
            "related_roles": ["AI Engineer", "Conversational AI Developer", "Data Scientist"],
            "related_skills": ["Python", "Transformers", "PyTorch"],
            "why_learn": "Rapidly expanding domain powering automated summarization, search, and intelligent assistants."
        },
        {
            "technology": "Artificial Intelligence",
            "aliases": ["artificial intelligence"],
            "related_roles": ["AI Solutions Architect", "Research Scientist"],
            "related_skills": ["Algorithms", "Python", "Cloud AI APIs"],
            "why_learn": "Broad strategic corporate focus area integrating intelligent automation across business operations."
        },
    ],
    "Cloud Computing & Infrastructure": [
        {
            "technology": "AWS",
            "aliases": ["aws", "amazon web services"],
            "related_roles": ["Cloud Engineer", "Solutions Architect", "DevOps Engineer"],
            "related_skills": ["Linux", "Terraform", "Docker", "Networking"],
            "why_learn": "The world's leading public cloud platform, present across enterprise infrastructure requirements."
        },
        {
            "technology": "Azure",
            "aliases": ["azure", "microsoft azure"],
            "related_roles": ["Cloud Architect", "Systems Administrator", "Enterprise Developer"],
            "related_skills": ["Active Directory", "C#", ".NET", "Terraform"],
            "why_learn": "Dominant in Fortune 500 corporate environments with seamless hybrid-cloud Microsoft integration."
        },
        {
            "technology": "Google Cloud",
            "aliases": ["google cloud", "gcp"],
            "related_roles": ["Data Engineer", "Cloud Engineer", "MLOps Engineer"],
            "related_skills": ["BigQuery", "Kubernetes", "Python"],
            "why_learn": "Premier cloud choice for advanced data analytics, Kubernetes management, and machine learning."
        },
    ],
    "DevOps & Containerization": [
        {
            "technology": "Docker",
            "aliases": ["docker"],
            "related_roles": ["DevOps Engineer", "Backend Developer", "Cloud Engineer"],
            "related_skills": ["Linux", "Kubernetes", "CI/CD"],
            "why_learn": "Industry standard containerization technology guaranteeing reproducible software deployments."
        },
        {
            "technology": "Kubernetes",
            "aliases": ["kubernetes", "k8s"],
            "related_roles": ["Site Reliability Engineer (SRE)", "Platform Engineer", "DevOps Engineer"],
            "related_skills": ["Docker", "Linux", "Cloud", "Helm"],
            "why_learn": "De-facto standard for container orchestration, autoscaling, and resilient microservice management."
        },
        {
            "technology": "Terraform",
            "aliases": ["terraform"],
            "related_roles": ["Infrastructure Engineer", "DevOps Engineer", "Cloud Architect"],
            "related_skills": ["AWS", "Azure", "Git", "HCL"],
            "why_learn": "Leading Infrastructure-as-Code (IaC) tool enabling reproducible declarative cloud provisioning."
        },
    ],
    "Data Engineering & Big Data": [
        {
            "technology": "Apache Spark",
            "aliases": ["apache spark", "spark"],
            "related_roles": ["Data Engineer", "Big Data Developer", "Analytics Engineer"],
            "related_skills": ["Python", "Scala", "SQL", "Hadoop"],
            "why_learn": "Premier distributed computing framework for high-throughput batch and streaming data pipelines."
        },
        {
            "technology": "Kafka",
            "aliases": ["apache kafka", "kafka"],
            "related_roles": ["Streaming Data Engineer", "Backend Architect", "Systems Engineer"],
            "related_skills": ["Java", "Python", "Microservices", "Event-driven Systems"],
            "why_learn": "High-throughput, fault-tolerant distributed event streaming platform powering real-time architectures."
        },
        {
            "technology": "Databricks",
            "aliases": ["databricks"],
            "related_roles": ["Data Platform Engineer", "Data Scientist", "MLOps Engineer"],
            "related_skills": ["Spark", "Delta Lake", "Python", "SQL"],
            "why_learn": "Unified lakehouse platform accelerating distributed analytics and machine learning operationalization."
        },
    ],
    "Modern Web & Distributed Systems": [
        {
            "technology": "React",
            "aliases": ["react", "react.js"],
            "related_roles": ["Frontend Developer", "Full Stack Developer", "UI Engineer"],
            "related_skills": ["JavaScript", "TypeScript", "HTML", "CSS"],
            "why_learn": "The preeminent frontend library for declarative, reactive, and component-based user experiences."
        },
        {
            "technology": "Microservices",
            "aliases": ["microservices"],
            "related_roles": ["Software Architect", "Senior Backend Engineer", "Lead Developer"],
            "related_skills": ["Docker", "REST API", "Kubernetes", "Kafka"],
            "why_learn": "Decoupled architecture pattern enabling independent scaling and agile feature velocity."
        },
        {
            "technology": "TypeScript",
            "aliases": ["typescript"],
            "related_roles": ["Full Stack Engineer", "Frontend Specialist", "Node.js Developer"],
            "related_skills": ["JavaScript", "React", "Node.js"],
            "why_learn": "Brings compile-time type safety to JavaScript, significantly reducing enterprise runtime bugs."
        },
    ]
}


def get_technology_radar_data() -> Dict[str, List[Dict[str, Any]]]:
    """Compile the Market-Relevant Technology Radar data with verified dataset statistics."""
    market_demand = load_market_skill_demand()
    radar_data = {}

    for domain, tech_list in RADAR_DOMAINS.items():
        domain_items = []
        for tech in tech_list:
            # Look up primary name or aliases
            stats = {"job_count": 0, "demand_percentage": 0.0}
            for alias in [tech["technology"].lower()] + tech.get("aliases", []):
                if alias in market_demand:
                    stats = market_demand[alias]
                    break

            domain_items.append({
                "technology": tech["technology"],
                "category": domain,
                "job_count": stats["job_count"],
                "demand_percentage": stats["demand_percentage"],
                "related_roles": tech["related_roles"],
                "related_skills": tech["related_skills"],
                "why_learn": tech["why_learn"],
                "evidence_label": "Market-Relevant Technology (Verified in LinkedIn Dataset)"
            })

        # Sort within domain by demand percentage descending
        domain_items.sort(key=lambda x: -x["demand_percentage"])
        radar_data[domain] = domain_items

    return radar_data
