"""SkillSight - Career Role Matching Module

Evaluates user competencies across multiple career tracks to compute
Skill Alignment percentages and identify alternative compatible career pathways.
"""

from typing import List, Dict, Any
from src.user_profile import ROLE_SKILL_BENCHMARKS


def match_career_roles(user_skills: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Compare user's current skills against all benchmark career roles.
    
    Args:
        user_skills: List of dicts with 'skill_name', 'proficiency'
        
    Returns:
        Sorted list of dicts with 'role', 'alignment_percentage', 'matched_skills',
        'missing_skills', 'total_required', 'description'.
    """
    user_skill_set = {
        s.get("skill_name", "").strip().lower()
        for s in user_skills
        if s.get("skill_name")
    }

    results = []

    for role_name, benchmark in ROLE_SKILL_BENCHMARKS.items():
        all_role_skills = benchmark["core_skills"] + benchmark["recommended_skills"]
        total_count = len(all_role_skills)

        matched = []
        missing = []

        for skill in all_role_skills:
            if skill.lower() in user_skill_set:
                matched.append(skill)
            else:
                missing.append(skill)

        alignment_pct = round((len(matched) / total_count * 100.0), 1) if total_count > 0 else 0.0

        results.append({
            "role": role_name,
            "alignment_percentage": alignment_pct,
            "matched_skills": matched,
            "missing_skills": missing,
            "matched_count": len(matched),
            "missing_count": len(missing),
            "total_count": total_count,
            "core_skills": benchmark["core_skills"],
            "description": benchmark.get("description", "")
        })

    # Sort descending by alignment percentage
    results.sort(key=lambda x: -x["alignment_percentage"])
    return results
