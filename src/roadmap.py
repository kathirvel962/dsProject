"""SkillSight - Personalized Career Roadmap Module

Generates a structured, 5-phase personalized learning roadmap based on the user's
current competencies, target career role, skill gaps, and verified market demand.
"""

from typing import List, Dict, Any
from src.skill_gap import analyze_skill_gap, load_market_skill_demand


def generate_career_roadmap(user_skills: List[Dict[str, str]], target_role: str) -> Dict[str, Any]:
    """Generate a personalized 5-phase career roadmap tailored to user skill gaps.
    
    Phases:
      - Phase 1: Foundation (Core language & baseline tools)
      - Phase 2: Core Domain Competencies (Target role essentials)
      - Phase 3: Specialization & Advanced Architecture
      - Phase 4: Cloud, DevOps & Deployment
      - Phase 5: Capstone Projects & Job Readiness
    """
    gap_result = analyze_skill_gap(user_skills, target_role)
    acquired_skills = {item["skill"].lower() for item in gap_result["already_have"]}
    missing_skills = gap_result["skills_to_develop"]
    market_demand = load_market_skill_demand()

    # Predefined skill phase mapping heuristics
    foundation_pool = {"python", "java", "c++", "c#", "javascript", "sql", "excel", "html", "css", "git"}
    core_pool = {
        "pandas", "numpy", "scikit-learn", "machine learning", "spring boot",
        "django", "flask", "react", "node.js", "power bi", "tableau", "mysql", "postgresql"
    }
    specialization_pool = {
        "deep learning", "artificial intelligence", "natural language processing",
        "computer vision", "tensorflow", "pytorch", "microservices", "graphql",
        "typescript", "angular", "vue.js", "mongodb"
    }
    cloud_devops_pool = {
        "aws", "azure", "google cloud", "docker", "kubernetes", "jenkins",
        "terraform", "linux", "rest api", "apache spark", "kafka", "databricks"
    }

    # Initialize Phase buckets
    phases = {
        "Phase 1 - Foundation": {
            "title": "Phase 1: Foundation & Prerequisite Mastery",
            "focus": "Establish strong syntactic fluency and core data manipulation foundations.",
            "items": [],
            "estimated_weeks": "3–5 Weeks"
        },
        "Phase 2 - Core Domain Competencies": {
            "title": "Phase 2: Core Domain & Role Competencies",
            "focus": f"Master the primary day-to-day libraries and tools expected of a professional {target_role}.",
            "items": [],
            "estimated_weeks": "6–8 Weeks"
        },
        "Phase 3 - Specialization & Advanced Topics": {
            "title": "Phase 3: Advanced Architecture & Specialization",
            "focus": "Deepen technical rigor through domain-specific frameworks and architectural patterns.",
            "items": [],
            "estimated_weeks": "5–7 Weeks"
        },
        "Phase 4 - Cloud, DevOps & Deployment": {
            "title": "Phase 4: Cloud Infrastructure & Production Readiness",
            "focus": "Package, containerize, and deploy applications to scalable cloud environments.",
            "items": [],
            "estimated_weeks": "4–6 Weeks"
        },
        "Phase 5 - Job Readiness & Capstone Portfolio": {
            "title": "Phase 5: Job Readiness, Capstones & Interview Prep",
            "focus": "Build verified end-to-end portfolio projects, optimize resume, and practice technical assessments.",
            "items": [],
            "estimated_weeks": "3–4 Weeks"
        }
    }

    # Distribute missing skills into appropriate phases
    for item in missing_skills:
        s_lower = item["skill"].lower()
        priority = item["priority"]
        demand_pct = item["demand_percentage"]

        item_entry = {
            "name": item["skill"],
            "type": "Skill",
            "priority": priority,
            "demand_percentage": demand_pct,
            "status": "Not Started",
            "why": item["why_it_matters"]
        }

        if s_lower in foundation_pool:
            phases["Phase 1 - Foundation"]["items"].append(item_entry)
        elif s_lower in core_pool:
            phases["Phase 2 - Core Domain Competencies"]["items"].append(item_entry)
        elif s_lower in specialization_pool:
            phases["Phase 3 - Specialization & Advanced Topics"]["items"].append(item_entry)
        elif s_lower in cloud_devops_pool:
            phases["Phase 4 - Cloud, DevOps & Deployment"]["items"].append(item_entry)
        else:
            # Fallback based on priority
            if priority == "HIGH":
                phases["Phase 2 - Core Domain Competencies"]["items"].append(item_entry)
            else:
                phases["Phase 4 - Cloud, DevOps & Deployment"]["items"].append(item_entry)

    # If any phase is empty (e.g. user already has foundation skills), add an acquired badge note
    # And ensure Phase 5 has standardized job-readiness deliverables
    phase5_items = [
        {
            "name": f"Build 2-3 Production Capstone Projects ({target_role})",
            "type": "Project",
            "priority": "HIGH",
            "demand_percentage": 100.0,
            "status": "In Progress",
            "why": "Tangible proof of technical execution on GitHub/portfolio."
        },
        {
            "name": "Target Role Resume & Technical Portfolio Optimization",
            "type": "Milestone",
            "priority": "HIGH",
            "demand_percentage": 100.0,
            "status": "Not Started",
            "why": "Showcase verified competencies aligned with ATS parsing standards."
        },
        {
            "name": "Technical Problem Solving & System Design Mock Interviews",
            "type": "Milestone",
            "priority": "MEDIUM",
            "demand_percentage": 85.0,
            "status": "Not Started",
            "why": "Prepare for live coding, system architecture, and behavioral rounds."
        }
    ]
    phases["Phase 5 - Job Readiness & Capstone Portfolio"]["items"].extend(phase5_items)

    # Convert phases to ordered list
    ordered_phases = []
    total_roadmap_items = 0
    for phase_key, phase_data in phases.items():
        ordered_phases.append({
            "phase_key": phase_key,
            "title": phase_data["title"],
            "focus": phase_data["focus"],
            "estimated_weeks": phase_data["estimated_weeks"],
            "items": phase_data["items"],
            "item_count": len(phase_data["items"])
        })
        total_roadmap_items += len(phase_data["items"])

    return {
        "target_role": target_role,
        "total_phases": len(ordered_phases),
        "total_items": total_roadmap_items,
        "phases": ordered_phases,
        "summary": (
            f"Personalized 5-Phase Roadmap engineered for {target_role}. "
            f"Prioritizes {len(missing_skills)} missing skills while acknowledging "
            f"{len(acquired_skills)} competencies you have already acquired."
        )
    }
