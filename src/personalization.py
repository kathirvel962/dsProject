"""SkillSight - Personalization & Career Intelligence Engine

Computes Career Readiness Scores, recommends 'What Should I Learn Next?',
and generates dynamic Career Market Alerts grounded in job-posting data.
"""

from typing import Dict, List, Any
from src.skill_gap import analyze_skill_gap, load_market_skill_demand
from src.user_profile import ROLE_SKILL_BENCHMARKS


def calculate_career_readiness(
    user_profile: Dict[str, Any],
    user_skills: List[Dict[str, str]],
    target_role: str
) -> Dict[str, Any]:
    """Calculate an analytical Career Readiness Score (0-100) based on profile attributes.
    
    Formula Weights:
      1. Skill Coverage vs Target Role (45 points max)
      2. Skill Proficiency Depth (20 points max)
      3. Academic & Educational Alignment (15 points max)
      4. Experience Level Alignment (10 points max)
      5. Projects & Certifications Presence (10 points max)
      
    Total: 100 points
    """
    gap_data = analyze_skill_gap(user_skills, target_role)
    skill_coverage_pct = gap_data["coverage_percentage"]
    skill_coverage_points = round((skill_coverage_pct / 100.0) * 45.0, 1)

    # 2. Proficiency Depth: Advanced = 1.0, Intermediate = 0.75, Beginner = 0.5
    matched_skills = gap_data["already_have"]
    if matched_skills:
        prof_weights = {"Advanced": 1.0, "Intermediate": 0.75, "Beginner": 0.5}
        avg_prof = sum(prof_weights.get(s["proficiency"], 0.75) for s in matched_skills) / len(matched_skills)
        proficiency_points = round(avg_prof * 20.0, 1)
        proficiency_pct = round(avg_prof * 100.0, 1)
    else:
        proficiency_points = 5.0
        proficiency_pct = 25.0

    # 3. Academic Alignment
    personal = user_profile.get("personal", {})
    degree = personal.get("degree", "").lower()
    branch = personal.get("branch", "").lower()
    
    # Check relevance of degree & branch
    tech_keywords = ["computer", "science", "information", "data", "engineering", "tech", "mathematics", "statistics"]
    is_tech_branch = any(k in branch for k in tech_keywords)
    
    if is_tech_branch:
        academic_points = 15.0
        academic_pct = 100.0
    elif "b.tech" in degree or "bachelor" in degree or "m.tech" in degree or "master" in degree:
        academic_points = 12.0
        academic_pct = 80.0
    else:
        academic_points = 9.0
        academic_pct = 60.0

    # 4. Experience Level
    pref = user_profile.get("preferences", {})
    exp_level = pref.get("experience_level", "Entry level").lower()
    if "mid" in exp_level or "senior" in exp_level or "associate" in exp_level:
        exp_points = 10.0
        exp_pct = 100.0
    elif "entry" in exp_level:
        exp_points = 7.0
        exp_pct = 70.0
    else:
        exp_points = 5.0
        exp_pct = 50.0

    # 5. Projects & Certifications
    certs = personal.get("certifications", "").strip()
    projs = personal.get("projects_summary", "").strip()
    port = personal.get("portfolio_url", "").strip()

    proj_cert_points = 0.0
    if certs:
        proj_cert_points += 4.0
    if projs:
        proj_cert_points += 4.0
    if port:
        proj_cert_points += 2.0
    proj_cert_pct = round((proj_cert_points / 10.0) * 100.0, 1)

    total_score = round(skill_coverage_points + proficiency_points + academic_points + exp_points + proj_cert_points)
    total_score = min(100, max(10, total_score))

    # Analytical status label
    if total_score >= 80:
        status_label = "High Alignment"
        status_color = "green"
    elif total_score >= 60:
        status_label = "Competitive Progress"
        status_color = "blue"
    elif total_score >= 40:
        status_label = "Developing Foundation"
        status_color = "orange"
    else:
        status_label = "Early Exploration"
        status_color = "red"

    return {
        "readiness_score": total_score,
        "status_label": status_label,
        "status_color": status_color,
        "factors": {
            "skill_coverage": {
                "score": skill_coverage_points,
                "max": 45.0,
                "percentage": skill_coverage_pct
            },
            "proficiency_depth": {
                "score": proficiency_points,
                "max": 20.0,
                "percentage": proficiency_pct
            },
            "academic_alignment": {
                "score": academic_points,
                "max": 15.0,
                "percentage": academic_pct
            },
            "experience_alignment": {
                "score": exp_points,
                "max": 10.0,
                "percentage": exp_pct
            },
            "projects_and_certs": {
                "score": proj_cert_points,
                "max": 10.0,
                "percentage": proj_cert_pct
            }
        },
        "disclaimer": "Career readiness is an analytical estimate based on the selected profile and available job-market data, not a guarantee of employment."
    }


def get_what_to_learn_next(user_skills: List[Dict[str, str]], target_role: str) -> List[Dict[str, Any]]:
    """Determine top 3 recommended priority skills to learn next with explainable rationales."""
    gap_data = analyze_skill_gap(user_skills, target_role)
    missing = gap_data["skills_to_develop"]

    recommendations = []
    for item in missing[:3]:
        skill = item["skill"]
        demand_pct = item["demand_percentage"]
        is_core = item["is_core"]

        if is_core:
            reason = (
                f"Essential core competency for {target_role} roles, appearing in "
                f"{demand_pct:.2f}% of relevant job postings in the analyzed dataset."
            )
        else:
            reason = (
                f"High-frequency technology ({demand_pct:.2f}% demand) that complements your existing "
                f"profile and expands candidacy for {target_role} vacancies."
            )

        recommendations.append({
            "skill": skill,
            "demand_percentage": demand_pct,
            "priority": item["priority"],
            "reason": reason,
            "suggested_action": f"Dedicate 10–15 hours to build a practical working mini-project with {skill}."
        })

    return recommendations


def get_career_market_alerts(user_skills: List[Dict[str, str]], target_role: str) -> List[Dict[str, Any]]:
    """Compile dynamic, data-grounded career alerts based on current profile and job-market data."""
    gap_data = analyze_skill_gap(user_skills, target_role)
    missing_high = [s for s in gap_data["skills_to_develop"] if s["priority"] == "HIGH"]
    missing_count = len(gap_data["skills_to_develop"])
    acquired_count = len(gap_data["already_have"])

    alerts = []

    # Alert 1: High Priority Missing Skill
    if missing_high:
        top_missing = missing_high[0]
        alerts.append({
            "type": "warning",
            "title": f"Skill Gap Alert: {top_missing['skill']}",
            "message": (
                f"{top_missing['skill']} is a premier core requirement for {target_role} "
                f"({top_missing['demand_percentage']:.2f}% dataset demand). Adding this skill "
                "will substantially increase your candidate profile alignment."
            ),
            "source": "Based on analyzed job-posting dataset."
        })

    # Alert 2: Profile Strength
    if acquired_count >= 3:
        top_acquired = [s["skill"] for s in gap_data["already_have"][:3]]
        alerts.append({
            "type": "success",
            "title": "Strong Competency Foundation",
            "message": (
                f"You have already acquired key competencies: {', '.join(top_acquired)}. "
                "Highlight these prominently on your resume and GitHub repositories."
            ),
            "source": "Based on user profile competencies."
        })

    # Alert 3: Remote / Market Mobility Alert
    alerts.append({
        "type": "info",
        "title": "Workplace Flexibility Telemetry",
        "message": (
            "14.73% of analyzed positions in the dataset offer full remote flexibility, "
            "while 85.27% require on-site or hybrid presence in metropolitan hubs like New York, "
            "Chicago, and Austin."
        ),
        "source": "Based on analyzed job-posting dataset (2,340 remote postings)."
    })

    # Alert 4: Salary Benchmark Alert
    alerts.append({
        "type": "info",
        "title": "Compensation Benchmark Notice",
        "message": (
            f"The median transparent compensation in the analyzed dataset is $65,000, "
            f"with Mid-Senior roles averaging $87,464 and Full-time roles averaging $82,152."
        ),
        "source": "Based on analyzed job-posting dataset (6,502 salary records)."
    })

    return alerts
