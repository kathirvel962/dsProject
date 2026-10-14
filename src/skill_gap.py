"""SkillSight - Skill Gap Analyzer Module

Evaluates user competencies against target career requirements and verified
job-market demand metrics from the LinkedIn postings dataset.
"""

import os
from typing import Dict, List, Any
import pandas as pd
from src.user_profile import ROLE_SKILL_BENCHMARKS

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILL_FREQ_PATH = os.path.join(PROJECT_ROOT, "outputs", "results", "skill_frequency.csv")


def load_market_skill_demand() -> Dict[str, Dict[str, float]]:
    """Load precomputed dataset skill demand frequencies.
    
    Returns a dictionary mapping skill_name -> {'Job_Count': int, 'Demand_Percentage': float}
    """
    if not os.path.exists(SKILL_FREQ_PATH):
        return {}

    try:
        df = pd.read_csv(SKILL_FREQ_PATH)
        # Normalize keys for robust case-insensitive lookup
        demand_map = {}
        for _, row in df.iterrows():
            skill = str(row["Skill"]).strip()
            demand_map[skill.lower()] = {
                "skill": skill,
                "job_count": int(row.get("Job_Count", 0)),
                "demand_percentage": float(row.get("Demand_Percentage", 0.0))
            }
        return demand_map
    except Exception:
        return {}


def analyze_skill_gap(user_skills: List[Dict[str, str]], target_role: str) -> Dict[str, Any]:
    """Perform deterministic, explainable skill-gap analysis.
    
    Args:
        user_skills: List of dicts, each with keys 'skill_name', 'proficiency'
        target_role: Name of preferred career role
        
    Returns:
        Structured dictionary with 'already_have', 'skills_to_develop',
        'coverage_percentage', 'target_role_info'.
    """
    market_demand = load_market_skill_demand()

    # Retrieve benchmark definition for target role
    role_info = ROLE_SKILL_BENCHMARKS.get(
        target_role,
        {
            "core_skills": ["Python", "SQL", "Git", "REST API"],
            "recommended_skills": ["Docker", "Linux", "AWS", "Cloud"],
            "description": "Technical software and engineering role."
        }
    )

    core_skills = role_info["core_skills"]
    recommended_skills = role_info["recommended_skills"]
    all_target_skills = list(dict.fromkeys(core_skills + recommended_skills))

    # User skill lookup
    user_skill_map = {}
    for s in user_skills:
        s_name = s.get("skill_name", "").strip()
        if s_name:
            user_skill_map[s_name.lower()] = {
                "name": s_name,
                "proficiency": s.get("proficiency", "Intermediate")
            }

    already_have = []
    skills_to_develop = []

    # 1. Identify skills user already has that match the target role
    for skill in all_target_skills:
        lower_skill = skill.lower()
        market_stats = market_demand.get(lower_skill, {"job_count": 0, "demand_percentage": 0.0})

        if lower_skill in user_skill_map:
            user_prof = user_skill_map[lower_skill]["proficiency"]
            already_have.append({
                "skill": skill,
                "proficiency": user_prof,
                "is_core": skill in core_skills,
                "job_count": market_stats["job_count"],
                "demand_percentage": market_stats["demand_percentage"],
                "status": "Acquired"
            })
        else:
            is_core = skill in core_skills
            # Determine priority based on core status and market demand
            pct = market_stats["demand_percentage"]
            if is_core and pct >= 2.0:
                priority = "HIGH"
            elif is_core or pct >= 2.0:
                priority = "MEDIUM"
            else:
                priority = "LOW"

            # Explainable rationale
            if is_core:
                why = f"Foundational competency for {target_role} roles across industry job postings."
            else:
                why = f"Highly sought-after complementary technology frequently paired with {target_role} requirements."

            skills_to_develop.append({
                "skill": skill,
                "is_core": is_core,
                "job_count": market_stats["job_count"],
                "demand_percentage": market_stats["demand_percentage"],
                "priority": priority,
                "why_it_matters": why,
            })

    # Also capture user's other skills not in target benchmark
    additional_user_skills = []
    for lower_skill, info in user_skill_map.items():
        if lower_skill not in [s.lower() for s in all_target_skills]:
            market_stats = market_demand.get(lower_skill, {"job_count": 0, "demand_percentage": 0.0})
            additional_user_skills.append({
                "skill": info["name"],
                "proficiency": info["proficiency"],
                "is_core": False,
                "job_count": market_stats["job_count"],
                "demand_percentage": market_stats["demand_percentage"],
                "status": "Transferable"
            })

    # Sort missing skills: Core first, then by demand percentage descending
    skills_to_develop.sort(
        key=lambda x: (1 if x["priority"] == "HIGH" else (2 if x["priority"] == "MEDIUM" else 3), -x["demand_percentage"])
    )

    # Assign suggested learning sequence
    for idx, item in enumerate(skills_to_develop, start=1):
        item["learning_order"] = idx

    # Calculate skill coverage percentage
    total_target = len(all_target_skills)
    matched_target = len(already_have)
    coverage_pct = round((matched_target / total_target * 100.0), 1) if total_target > 0 else 0.0

    return {
        "target_role": target_role,
        "target_role_description": role_info.get("description", ""),
        "coverage_percentage": coverage_pct,
        "already_have": already_have,
        "skills_to_develop": skills_to_develop,
        "additional_user_skills": additional_user_skills,
        "total_target_skills_count": total_target,
        "matched_skills_count": matched_target,
        "missing_skills_count": len(skills_to_develop)
    }
