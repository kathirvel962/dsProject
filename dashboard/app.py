"""SkillSight - Module 16 & 17: Personalized Career Intelligence & Skill Roadmap Platform

Interactive Streamlit Application featuring:
- User Authentication (Register, Login, Demo Session)
- Academic Career Profile & Skill Proficiency Management
- Personalized Skill Gap Analyzer
- Market-Relevant Technology Radar
- Career Role Matching (Skill Alignment)
- Personalized 5-Phase Career Roadmap
- Skill-Gap Based Project Recommendations
- Real-Time SQLite Learning Progress Tracker
- Supervised ML Salary Prediction (RandomForestRegressor)
- Comprehensive Job Market Macro Analytics
"""

import os
import sys

# Ensure project root is on sys.path regardless of execution working directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import joblib
import pandas as pd
import streamlit as st

# Configure wide page layout and branding
st.set_page_config(
    page_title="SkillSight | Personalized Career Intelligence",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import backend modules
from src.database import init_db
from src.auth import login_user, register_user, get_user_by_id
from src.user_profile import (
    get_user_profile,
    update_academic_profile,
    update_user_skills,
    update_career_preferences,
    SKILL_TAXONOMY,
    ALL_TAXONOMY_SKILLS,
    PREDEFINED_ROLES
)
from src.skill_gap import analyze_skill_gap
from src.career_matching import match_career_roles
from src.emerging_tech import get_technology_radar_data
from src.roadmap import generate_career_roadmap
from src.project_recommender import recommend_projects
from src.progress_tracker import (
    sync_roadmap_with_db,
    get_user_progress_summary,
    get_user_progress_items,
    update_item_status
)
from src.personalization import (
    calculate_career_readiness,
    get_what_to_learn_next,
    get_career_market_alerts
)

# Initialize SQLite database schema
init_db()

# File paths for analytical results and charts
RESULTS_DIR = os.path.join(PROJECT_ROOT, "outputs", "results")
CHARTS_DIR = os.path.join(PROJECT_ROOT, "outputs", "charts")
DATASET_SUMMARY_PATH = os.path.join(RESULTS_DIR, "dataset_summary.csv")
TOP_SKILLS_PATH = os.path.join(RESULTS_DIR, "top_skills.csv")
TOP_TITLES_PATH = os.path.join(RESULTS_DIR, "top_job_titles.csv")
TOP_LOCATIONS_PATH = os.path.join(RESULTS_DIR, "top_locations.csv")
EXPERIENCE_PATH = os.path.join(RESULTS_DIR, "experience_levels.csv")
WORK_TYPE_PATH = os.path.join(RESULTS_DIR, "work_type.csv")
REMOTE_PATH = os.path.join(RESULTS_DIR, "remote_jobs.csv")
SALARY_SUMMARY_PATH = os.path.join(RESULTS_DIR, "salary_summary.csv")
SALARY_BY_EXP_PATH = os.path.join(RESULTS_DIR, "salary_by_experience.csv")
SALARY_BY_WT_PATH = os.path.join(RESULTS_DIR, "salary_by_work_type.csv")
ML_RESULTS_PATH = os.path.join(RESULTS_DIR, "ml_results.csv")
SALARY_MODEL_PATH = os.path.join(RESULTS_DIR, "salary_model.pkl")


# --------------------------------------------------
# CACHED LOADERS
# --------------------------------------------------
@st.cache_data
def load_csv_data(filepath: str) -> pd.DataFrame | None:
    if os.path.exists(filepath):
        try:
            return pd.read_csv(filepath)
        except Exception:
            return None
    return None


@st.cache_resource
def load_salary_model():
    if os.path.exists(SALARY_MODEL_PATH):
        try:
            return joblib.load(SALARY_MODEL_PATH)
        except Exception:
            return None
    return None


def show_chart(chart_name: str, caption: str = ""):
    path = os.path.join(CHARTS_DIR, chart_name)
    if os.path.exists(path):
        st.image(path, caption=caption, use_container_width=True)
    else:
        st.warning(f"Chart file `{chart_name}` not found.")


# --------------------------------------------------
# SESSION STATE MANAGEMENT
# --------------------------------------------------
if "user" not in st.session_state:
    st.session_state["user"] = None

if "nav_choice" not in st.session_state:
    st.session_state["nav_choice"] = "Home"


def logout():
    st.session_state["user"] = None
    st.session_state["nav_choice"] = "Home"
    st.rerun()


# --------------------------------------------------
# AUTHENTICATION SCREEN (IF NOT LOGGED IN)
# --------------------------------------------------
def render_auth_page():
    st.markdown(
        """
        <div style="text-align: center; padding: 25px 0 15px 0;">
            <h1 style="font-size: 2.8rem; margin-bottom: 0.2rem;">💼 SkillSight</h1>
            <p style="font-size: 1.25rem; color: #3B82F6; font-weight: 600; margin-bottom: 0.5rem;">
                Personalized Career Intelligence & Skill Roadmap Platform
            </p>
            <p style="font-size: 1.0rem; color: #64748B; max-width: 750px; margin: 0 auto 1.5rem auto;">
                Bridge your academic background with real-world job-market data. Discover skill gaps,
                track verified technology demand, and unlock your personalized career development roadmap.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_box_l, col_box_m, col_box_r = st.columns([1, 1.8, 1])
    with col_box_m:
        tab_login, tab_register, tab_demo = st.tabs(["🔑 Sign In", "📝 Create Account", "⚡ One-Click Demo Mode"])

        # Tab 1: Login
        with tab_login:
            st.markdown("### Welcome Back")
            st.caption("Sign in to access your saved career profile, roadmap, and progress tracking.")
            login_email = st.text_input("Email Address", key="login_email_input", placeholder="student@university.edu")
            login_pass = st.text_input("Password", type="password", key="login_pass_input", placeholder="••••••••")

            if st.button("Sign In to SkillSight", type="primary", use_container_width=True):
                ok, msg, user_data = login_user(login_email, login_pass)
                if ok:
                    st.session_state["user"] = user_data
                    st.success(f"Welcome, {user_data['name']}!")
                    st.rerun()
                else:
                    st.error(msg)

        # Tab 2: Register
        with tab_register:
            st.markdown("### Create Your Profile")
            st.caption("Register to generate an explainable, personalized career roadmap.")
            reg_name = st.text_input("Full Name", key="reg_name_input", placeholder="Alex Morgan")
            reg_email = st.text_input("Email Address", key="reg_email_input", placeholder="alex@university.edu")
            reg_pass = st.text_input("Choose Password", type="password", key="reg_pass_input", placeholder="••••••••")

            if st.button("Register & Get Started", type="primary", use_container_width=True):
                ok, msg, uid = register_user(reg_name, reg_email, reg_pass)
                if ok:
                    # Auto login
                    _, _, user_data = login_user(reg_email, reg_pass)
                    st.session_state["user"] = user_data
                    st.success("Account created successfully! Welcome to SkillSight.")
                    st.rerun()
                else:
                    st.error(msg)

        # Tab 3: One-Click Demo Login
        with tab_demo:
            st.markdown("### Academic Evaluator / Viva Demo Mode")
            st.info(
                "**Pre-configured Academic Profile:**\n\n"
                "- **Student**: Alex Morgan (3rd Year B.Tech Computer Science)\n"
                "- **Target Career Role**: Data Scientist\n"
                "- **Current Skills**: Python, SQL, Pandas, NumPy, Java, Git, Excel\n"
                "- **Pre-seeded Roadmap**: 10 skills and capstones actively tracked."
            )
            if st.button("🚀 Launch Instant Demo Session (Alex Morgan)", type="secondary", use_container_width=True):
                ok, _, user_data = login_user("demo@skillsight.edu", "demo123")
                if ok:
                    st.session_state["user"] = user_data
                    st.rerun()
                else:
                    st.error("Demo profile not initialized. Please try logging in with demo@skillsight.edu / demo123.")

    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #94A3B8; font-size: 0.85rem;">
            SkillSight Platform • Grounded in 15,886 LinkedIn Job Postings • Explainable Data Science Methodology
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# TOP PERSONALIZED HEADER (FOR LOGGED IN USERS)
# --------------------------------------------------
def render_personalized_banner(user_profile: dict, readiness_data: dict, progress_data: dict):
    user_name = user_profile["personal"]["name"]
    target_role = user_profile["preferences"]["preferred_role"]
    degree = user_profile["personal"]["degree"]
    branch = user_profile["personal"]["branch"]
    year = user_profile["personal"]["academic_year"]
    skills = [s["skill_name"] for s in user_profile["skills"]]
    readiness_score = readiness_data["readiness_score"]
    status_label = readiness_data["status_label"]
    progress_pct = progress_data["progress_percentage"]

    # Render clean summary banner
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); padding: 18px 24px; border-radius: 12px; color: white; margin-bottom: 20px; border-left: 5px solid #3B82F6;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <h2 style="margin: 0; color: #F8FAFC; font-size: 1.6rem;">Welcome, {user_name} 👋</h2>
                    <p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 0.95rem;">
                        <strong>Career Goal:</strong> <span style="color: #60A5FA;">{target_role}</span> &nbsp;|&nbsp;
                        <strong>Academic:</strong> {degree} {branch} ({year})
                    </p>
                </div>
                <div style="display: flex; gap: 20px; margin-top: 8px;">
                    <div style="text-align: center; background: rgba(255,255,255,0.06); padding: 8px 16px; border-radius: 8px;">
                        <span style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Career Readiness</span><br>
                        <span style="font-size: 1.3rem; font-weight: 700; color: #38BDF8;">{readiness_score}</span> <span style="font-size: 0.8rem; color: #94A3B8;">/ 100 ({status_label})</span>
                    </div>
                    <div style="text-align: center; background: rgba(255,255,255,0.06); padding: 8px 16px; border-radius: 8px;">
                        <span style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Roadmap Progress</span><br>
                        <span style="font-size: 1.3rem; font-weight: 700; color: #34D399;">{progress_pct}%</span>
                    </div>
                </div>
            </div>
            <div style="margin-top: 12px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 0.85rem; color: #CBD5E1;">
                <strong>Current Skills:</strong> {" | ".join(skills[:8]) if skills else "No skills added yet"} {"..." if len(skills) > 8 else ""}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# PAGE 1: HOME (PERSONALIZED OVERVIEW & READINESS)
# --------------------------------------------------
def render_home_page(user_profile: dict, readiness_data: dict, progress_data: dict):
    user_skills = user_profile["skills"]
    target_role = user_profile["preferences"]["preferred_role"]

    st.subheader("🎯 Executive Career Telemetry")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Career Readiness Score", f"{readiness_data['readiness_score']} / 100", readiness_data["status_label"])
    col2.metric("Roadmap Completion", f"{progress_data['progress_percentage']}%", f"{progress_data['completed_items']} / {progress_data['total_items']} items")
    col3.metric("Skills Acquired", f"{len(user_skills)} skills", f"{progress_data['completed_skills']} verified")
    col4.metric("Target Role", target_role, user_profile["preferences"]["work_mode"])

    st.markdown("---")

    # Readiness breakdown
    col_score_l, col_score_r = st.columns([1.1, 0.9])
    with col_score_l:
        st.subheader("📊 Career Readiness Decomposition")
        st.caption("Analytical evaluation of candidate competitiveness against target role benchmarks.")
        
        factors = readiness_data["factors"]
        for f_name, f_data in [
            ("Required Skill Coverage", factors["skill_coverage"]),
            ("Skill Proficiency Depth", factors["proficiency_depth"]),
            ("Academic & Degree Alignment", factors["academic_alignment"]),
            ("Experience Level Match", factors["experience_alignment"]),
            ("Portfolio & Certifications", factors["projects_and_certs"])
        ]:
            c_label, c_bar, c_val = st.columns([1.5, 2, 1])
            c_label.markdown(f"**{f_name}**")
            c_bar.progress(f_data["percentage"] / 100.0)
            c_val.markdown(f"{f_data['score']} / {f_data['max']} pts ({f_data['percentage']}%)")

        st.caption(f"📌 *{readiness_data['disclaimer']}*")

    with col_score_r:
        st.subheader("💡 What Should I Learn Next?")
        st.caption("Top 3 priority skill recommendations derived from target role gaps & market demand.")
        next_skills = get_what_to_learn_next(user_skills, target_role)
        
        if next_skills:
            for idx, rec in enumerate(next_skills, 1):
                priority_color = "#EF4444" if rec["priority"] == "HIGH" else "#F59E0B"
                st.markdown(
                    f"""
                    <div style="background: #F8FAFC; border-left: 4px solid {priority_color}; padding: 12px; border-radius: 6px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between;">
                            <strong style="font-size: 1.05rem;">{idx}. {rec['skill']}</strong>
                            <span style="background: {priority_color}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">{rec['priority']} PRIORITY</span>
                        </div>
                        <p style="margin: 6px 0 4px 0; font-size: 0.88rem; color: #334155;">{rec['reason']}</p>
                        <span style="font-size: 0.8rem; color: #2563EB; font-weight: 500;">Action: {rec['suggested_action']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.success("🎉 You have covered all primary benchmarks for your target role!")

    st.markdown("---")

    # Career Market Alerts
    st.subheader("📢 Career Market Alerts")
    alerts = get_career_market_alerts(user_skills, target_role)
    for alert in alerts:
        if alert["type"] == "warning":
            st.warning(f"**{alert['title']}**: {alert['message']} — *{alert['source']}*")
        elif alert["type"] == "success":
            st.success(f"**{alert['title']}**: {alert['message']} — *{alert['source']}*")
        else:
            st.info(f"**{alert['title']}**: {alert['message']} — *{alert['source']}*")


# --------------------------------------------------
# PAGE 2: MY PROFILE (ACADEMIC & SKILL EDITOR)
# --------------------------------------------------
def render_profile_page(user_id: int, user_profile: dict):
    st.subheader("👤 Candidate Profile & Competency Manager")
    st.caption("Keep your academic credentials, technical skills, and career preferences up to date.")

    tab1, tab2, tab3 = st.tabs(["🎓 Academic & Personal", "💻 Technical Skills & Proficiency", "🎯 Career Preferences"])

    # Tab 1: Academic & Personal
    with tab1:
        st.markdown("#### Personal & Academic Background")
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            name_val = st.text_input("Full Name", value=user_profile["personal"]["name"])
            degree_val = st.selectbox(
                "Degree Program",
                options=["B.Tech", "B.E.", "B.Sc", "BCA", "M.Tech", "M.Sc", "MCA", "MBA", "Other"],
                index=0 if user_profile["personal"]["degree"] not in ["B.Tech", "B.E.", "B.Sc", "BCA", "M.Tech", "M.Sc", "MCA", "MBA", "Other"] else ["B.Tech", "B.E.", "B.Sc", "BCA", "M.Tech", "M.Sc", "MCA", "MBA", "Other"].index(user_profile["personal"]["degree"])
            )
            branch_val = st.text_input("Branch / Specialization", value=user_profile["personal"]["branch"])
            year_val = st.selectbox(
                "Current Academic Year",
                options=["1st Year", "2nd Year", "3rd Year", "4th Year", "Graduated / Professional"],
                index=2 if user_profile["personal"]["academic_year"] not in ["1st Year", "2nd Year", "3rd Year", "4th Year", "Graduated / Professional"] else ["1st Year", "2nd Year", "3rd Year", "4th Year", "Graduated / Professional"].index(user_profile["personal"]["academic_year"])
            )

        with col_a2:
            grad_val = st.number_input("Expected Graduation Year", min_value=2020, max_value=2032, value=int(user_profile["personal"]["graduation_year"]))
            cgpa_val = st.number_input("Current CGPA / Percentage", min_value=0.0, max_value=10.0, value=float(user_profile["personal"]["cgpa"]), step=0.1)
            edu_level = st.selectbox(
                "Education Level",
                options=["Undergraduate", "Postgraduate", "High School", "Doctorate"],
                index=0
            )
            port_val = st.text_input("GitHub / Portfolio URL", value=user_profile["personal"]["portfolio_url"])

        certs_val = st.text_area("Certifications & Credentials (optional)", value=user_profile["personal"]["certifications"], height=80)
        proj_val = st.text_area("Summary of Completed Projects (optional)", value=user_profile["personal"]["projects_summary"], height=80)

        if st.button("Save Academic Background", type="primary", key="save_academic_btn"):
            update_academic_profile(user_id, {
                "name": name_val,
                "degree": degree_val,
                "branch": branch_val,
                "academic_year": year_val,
                "graduation_year": grad_val,
                "cgpa": cgpa_val,
                "education_level": edu_level,
                "certifications": certs_val,
                "projects_summary": proj_val,
                "portfolio_url": port_val
            })
            st.success("Academic profile successfully updated!")
            st.rerun()

    # Tab 2: Technical Skills & Proficiency
    with tab2:
        st.markdown("#### Known Technical Skills & Proficiency Levels")
        st.caption("Select technologies you have learned, and indicate your self-assessed proficiency level.")

        existing_skills_dict = {s["skill_name"]: s["proficiency"] for s in user_profile["skills"]}
        
        # Categorized multi-select
        st.markdown("##### 1. Select Skills by Category")
        all_selected = set(existing_skills_dict.keys())
        
        for category, cat_skills in SKILL_TAXONOMY.items():
            pre_selected_in_cat = [s for s in cat_skills if s in all_selected]
            chosen = st.multiselect(
                f"**{category}**",
                options=cat_skills,
                default=pre_selected_in_cat,
                key=f"cat_select_{category}"
            )
            # Update set
            for s in cat_skills:
                if s in chosen:
                    all_selected.add(s)
                else:
                    all_selected.discard(s)

        # Custom skill entry
        st.markdown("##### 2. Add Custom or Unlisted Skills")
        c_skill1, c_skill2 = st.columns([3, 1])
        new_custom_skill = c_skill1.text_input("Custom Skill Name", placeholder="e.g. Next.js, Rust, Solidity")
        if c_skill2.button("Add Skill", key="add_custom_btn"):
            if new_custom_skill.strip():
                all_selected.add(new_custom_skill.strip())
                st.rerun()

        st.markdown("---")
        st.markdown("##### 3. Specify Skill Proficiency Levels")
        st.caption("Select your proficiency for each active skill (Beginner, Intermediate, Advanced):")

        updated_skills_list = []
        if all_selected:
            cols = st.columns(3)
            for idx, skill in enumerate(sorted(all_selected)):
                col = cols[idx % 3]
                current_prof = existing_skills_dict.get(skill, "Intermediate")
                p_choice = col.selectbox(
                    f"{skill}",
                    options=["Beginner", "Intermediate", "Advanced"],
                    index=["Beginner", "Intermediate", "Advanced"].index(current_prof),
                    key=f"prof_picker_{skill}"
                )
                updated_skills_list.append({
                    "skill_name": skill,
                    "category": "General",
                    "proficiency": p_choice
                })
        else:
            st.info("No skills selected yet. Select skills from the categories above.")

        if st.button("Save Skills & Proficiencies", type="primary", key="save_skills_btn"):
            update_user_skills(user_id, updated_skills_list)
            st.success("Technical skill profile successfully saved!")
            st.rerun()

    # Tab 3: Career Preferences
    with tab3:
        st.markdown("#### Target Career Preferences")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            pref_role = st.selectbox(
                "Preferred Career Role",
                options=PREDEFINED_ROLES + ["Custom Role..."],
                index=PREDEFINED_ROLES.index(user_profile["preferences"]["preferred_role"]) if user_profile["preferences"]["preferred_role"] in PREDEFINED_ROLES else 0
            )
            if pref_role == "Custom Role...":
                pref_role = st.text_input("Specify Custom Role", value=user_profile["preferences"]["preferred_role"])

            pref_loc = st.selectbox(
                "Preferred Location",
                options=["United States", "New York, NY", "San Francisco, CA", "Austin, TX", "Chicago, IL", "Seattle, WA", "Boston, MA", "Atlanta, GA", "Remote"],
                index=0
            )
            work_mode = st.selectbox(
                "Workplace Mode",
                options=["Remote", "Hybrid", "On-site", "Any"],
                index=["Remote", "Hybrid", "On-site", "Any"].index(user_profile["preferences"]["work_mode"]) if user_profile["preferences"]["work_mode"] in ["Remote", "Hybrid", "On-site", "Any"] else 0
            )

        with col_p2:
            exp_pref = st.selectbox(
                "Target Experience Level",
                options=["Entry level", "Associate", "Mid-Senior level", "Director", "Executive"],
                index=0
            )
            emp_type = st.selectbox(
                "Employment Type",
                options=["Full-time", "Internship", "Contract", "Part-time"],
                index=0
            )
            sal_min = st.number_input("Expected Annual Salary Min ($ USD)", min_value=10000.0, max_value=300000.0, value=float(user_profile["preferences"]["expected_salary_min"]), step=5000.0)
            sal_max = st.number_input("Expected Annual Salary Max ($ USD)", min_value=20000.0, max_value=500000.0, value=float(user_profile["preferences"]["expected_salary_max"]), step=5000.0)

        interests = st.text_input("Career Interests & Focus Domains", value=user_profile["preferences"]["career_interests"])

        if st.button("Save Career Preferences", type="primary", key="save_pref_btn"):
            update_career_preferences(user_id, {
                "preferred_role": pref_role,
                "preferred_location": pref_loc,
                "work_mode": work_mode,
                "experience_level": exp_pref,
                "employment_type": emp_type,
                "expected_salary_min": sal_min,
                "expected_salary_max": sal_max,
                "preferred_industry": "Technology & Analytics",
                "career_interests": interests
            })
            st.success("Career preferences updated successfully!")
            st.rerun()


# --------------------------------------------------
# PAGE 3: SKILL ANALYSIS
# --------------------------------------------------
def render_skill_analysis_page(user_profile: dict):
    st.subheader("💻 Personalized Skill Intelligence")
    st.caption("Deep-dive comparative evaluation of your personal competencies against job-market demand.")

    user_skills = user_profile["skills"]
    target_role = user_profile["preferences"]["preferred_role"]

    if not user_skills:
        st.warning("You have not added any skills to your profile yet. Visit the 'My Profile' page to add your skills.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Total User Skills", f"{len(user_skills)} skills")
    advanced_count = sum(1 for s in user_skills if s["proficiency"] == "Advanced")
    inter_count = sum(1 for s in user_skills if s["proficiency"] == "Intermediate")
    col2.metric("Advanced Proficiency", f"{advanced_count} skills")
    col3.metric("Intermediate Proficiency", f"{inter_count} skills")

    st.markdown("---")

    col_l, col_r = st.columns([1.1, 0.9])
    with col_l:
        st.subheader("Your Technical Skills Inventory")
        df_user_skills = pd.DataFrame(user_skills)
        st.dataframe(df_user_skills, use_container_width=True)

    with col_r:
        st.subheader("Top In-Demand Market Skills (LinkedIn Dataset)")
        show_chart("top_skills.png", caption="Top 15 Technical Skills Ranked by Job Postings")


# --------------------------------------------------
# PAGE 4: SKILL GAP ANALYZER
# --------------------------------------------------
def render_skill_gap_page(user_profile: dict):
    target_role = user_profile["preferences"]["preferred_role"]
    user_skills = user_profile["skills"]

    st.subheader(f"🔍 Skill Gap Analyzer: {target_role}")
    st.caption(f"Rigorous evaluation comparing your current competencies against {target_role} hiring requirements.")

    gap_data = analyze_skill_gap(user_skills, target_role)

    col1, col2, col3 = st.columns(3)
    col1.metric("Role Skill Coverage", f"{gap_data['coverage_percentage']}%")
    col2.metric("Acquired Benchmark Skills", f"{gap_data['matched_skills_count']} / {gap_data['total_target_skills_count']}")
    col3.metric("Skills To Develop", f"{gap_data['missing_skills_count']} skills")

    st.progress(gap_data["coverage_percentage"] / 100.0)
    st.markdown("---")

    col_have, col_need = st.columns(2)

    with col_have:
        st.markdown(f"#### ✅ Already Acquired ({len(gap_data['already_have'])})")
        st.caption("Skills you possess that align with this career track:")
        if gap_data["already_have"]:
            for item in gap_data["already_have"]:
                core_badge = "★ Core Skill" if item["is_core"] else "Supporting"
                st.markdown(
                    f"""
                    <div style="background: #F0FDF4; border: 1px solid #BBF7D0; padding: 10px 14px; border-radius: 8px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between;">
                            <strong style="color: #166534; font-size: 1.0rem;">✓ {item['skill']}</strong>
                            <span style="background: #DCFCE7; color: #15803D; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; font-weight: 600;">{item['proficiency']}</span>
                        </div>
                        <span style="font-size: 0.8rem; color: #64748B;">{core_badge} &nbsp;|&nbsp; Dataset Demand: {item['demand_percentage']:.2f}% ({item['job_count']:,} jobs)</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No matching benchmark skills found. Review 'Skills To Develop' to begin learning.")

    with col_need:
        st.markdown(f"#### 🎯 Skills To Develop ({len(gap_data['skills_to_develop'])})")
        st.caption("Missing high-impact skills ranked by priority and job-market demand:")
        if gap_data["skills_to_develop"]:
            for item in gap_data["skills_to_develop"]:
                p_color = "#EF4444" if item["priority"] == "HIGH" else ("#F59E0B" if item["priority"] == "MEDIUM" else "#6B7280")
                st.markdown(
                    f"""
                    <div style="background: #FEF2F2 if item['priority']=='HIGH' else '#FFFBEB'; border-left: 4px solid {p_color}; padding: 10px 14px; border-radius: 6px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between;">
                            <strong style="font-size: 1.0rem;">→ #{item['learning_order']}: {item['skill']}</strong>
                            <span style="background: {p_color}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; font-weight: 600;">{item['priority']} PRIORITY</span>
                        </div>
                        <p style="margin: 4px 0; font-size: 0.85rem; color: #475569;">{item['why_it_matters']}</p>
                        <span style="font-size: 0.8rem; color: #2563EB; font-weight: 500;">Market Demand: {item['demand_percentage']:.2f}% ({item['job_count']:,} postings)</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.success("🎉 Outstanding! You have acquired all core and recommended skills for this role.")


# --------------------------------------------------
# PAGE 5: JOB MARKET (MACRO ANALYTICS)
# --------------------------------------------------
def render_job_market_page():
    st.subheader("📈 Macro Job Market Telemetry")
    st.caption("Comprehensive exploratory findings across 15,886 LinkedIn job listings.")

    df_summary = load_csv_data(DATASET_SUMMARY_PATH)
    if df_summary is not None:
        metrics = dict(zip(df_summary["Metric"], df_summary["Value"]))
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Postings", f"{int(metrics.get('Total Jobs', 0)):,}")
        c2.metric("Unique Roles", f"{int(metrics.get('Unique Job Titles', 0)):,}")
        c3.metric("Locations", f"{int(metrics.get('Unique Locations', 0)):,}")
        c4.metric("Salary Transparent", f"{int(metrics.get('Jobs With Salary', 0)):,}")
        c5.metric("Remote Roles", f"{int(metrics.get('Remote Jobs', 0)):,}")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("A. Top In-Demand Job Titles")
        show_chart("top_job_titles.png")
    with col2:
        st.subheader("B. Geographic Employment Hubs")
        show_chart("top_locations.png")

    st.markdown("---")

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("C. Seniority & Experience Levels")
        show_chart("experience_levels.png")
    with col4:
        st.subheader("D. Employment Work Types")
        show_chart("work_type.png")


# --------------------------------------------------
# PAGE 6: EMERGING TECHNOLOGIES RADAR
# --------------------------------------------------
def render_emerging_tech_page():
    st.subheader("🚀 Market-Relevant Technology Radar")
    st.info(
        "📌 **Analytical Notice**: Technologies are designated as 'Market-Relevant' based on explicit "
        "verified frequency in the 15,886 job-posting dataset. SkillSight does not fabricate unverified 'growth trends'."
    )

    radar_data = get_technology_radar_data()

    for domain, tech_items in radar_data.items():
        st.markdown(f"### 🌐 {domain}")
        cols = st.columns(len(tech_items))
        for idx, tech in enumerate(tech_items):
            with cols[idx]:
                st.markdown(
                    f"""
                    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 14px; border-radius: 10px; height: 100%;">
                        <h4 style="margin: 0 0 6px 0; color: #1E293B;">{tech['technology']}</h4>
                        <span style="background: #DBEAFE; color: #1E40AF; padding: 2px 8px; border-radius: 8px; font-size: 0.78rem; font-weight: 600;">
                            {tech['demand_percentage']:.2f}% Market Demand
                        </span>
                        <p style="margin: 10px 0 6px 0; font-size: 0.85rem; color: #475569;">{tech['why_learn']}</p>
                        <hr style="margin: 8px 0; border: none; border-top: 1px solid #E2E8F0;">
                        <span style="font-size: 0.78rem; color: #64748B;"><strong>Related Roles:</strong> {', '.join(tech['related_roles'][:2])}</span><br>
                        <span style="font-size: 0.78rem; color: #64748B;"><strong>Key Stacks:</strong> {', '.join(tech['related_skills'][:2])}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        st.markdown("<br>", unsafe_allow_html=True)


# --------------------------------------------------
# PAGE 7: CAREER ROLE MATCHING (SKILL ALIGNMENT)
# --------------------------------------------------
def render_career_roles_page(user_profile: dict):
    user_skills = user_profile["skills"]
    st.subheader("🎯 Career Role Compatibility & Skill Alignment")
    st.caption("Evaluates your competency portfolio against 14 benchmark career tracks to identify high-compatibility alternative pathways.")

    if not user_skills:
        st.warning("Please add skills to your profile first to compute role compatibility.")
        return

    matches = match_career_roles(user_skills)

    for m in matches:
        score = m["alignment_percentage"]
        bar_color = "#10B981" if score >= 60 else ("#3B82F6" if score >= 40 else "#F59E0B")
        
        with st.expander(f"**{m['role']}** — {score}% Skill Alignment", expanded=(score >= 50)):
            st.markdown(f"*{m['description']}*")
            st.progress(score / 100.0)

            c_have, c_miss = st.columns(2)
            with c_have:
                st.markdown(f"**Matched Competencies ({m['matched_count']}):**")
                if m["matched_skills"]:
                    st.write(", ".join([f"✓ {s}" for s in m["matched_skills"]]))
                else:
                    st.caption("No overlapping skills currently acquired.")

            with c_miss:
                st.markdown(f"**Skills To Learn ({m['missing_count']}):**")
                st.write(", ".join([f"→ {s}" for s in m["missing_skills"][:6]]))


# --------------------------------------------------
# PAGE 8: SALARY INSIGHTS & ML PREDICTION
# --------------------------------------------------
def render_salary_page(user_profile: dict):
    st.subheader("💵 Personalized Compensation & Salary Insights")
    st.caption("Estimates compensation using a supervised Machine Learning Random Forest pipeline trained on verified annual salary postings.")

    # 1. Macro Summary Cards
    df_sal_summary = load_csv_data(SALARY_SUMMARY_PATH)
    if df_sal_summary is not None:
        sal_dict = dict(zip(df_sal_summary["Metric"], df_sal_summary["Value"]))
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Dataset Mean Salary", f"${float(sal_dict.get('Mean', 0)):,.0f}")
        c2.metric("Dataset Median Salary", f"${float(sal_dict.get('Median', 0)):,.0f}")
        c3.metric("Postings with Salary", f"{int(float(sal_dict.get('Count', 0))):,}")
        c4.metric("Standard Deviation", f"${float(sal_dict.get('Standard Deviation', 0)):,.0f}")

    st.markdown("---")

    # 2. Interactive ML Estimator
    st.subheader("🤖 Live Machine Learning Salary Estimator")
    st.caption("Pre-populated with your career preferences:")

    pref = user_profile["preferences"]
    pipeline = load_salary_model()

    col_in1, col_in2 = st.columns(2)
    with col_in1:
        exp_opt = st.selectbox(
            "Experience Level",
            options=["Mid-Senior level", "Entry level", "Associate", "Director", "Executive", "Internship", "Not Specified"],
            index=1 if "entry" in pref.get("experience_level", "").lower() else 0
        )
        wt_opt = st.selectbox(
            "Work Type",
            options=["Full-time", "Contract", "Part-time", "Temporary", "Internship", "Other"],
            index=0
        )
        rem_opt = st.selectbox(
            "Remote Status",
            options=["Remote", "Not Specified"],
            index=0 if pref.get("work_mode") == "Remote" else 1
        )

    with col_in2:
        loc_opt = st.selectbox(
            "Metro Region",
            options=["United States", "New York, NY", "San Francisco, CA", "Austin, TX", "Chicago, IL", "Seattle, WA", "Boston, MA", "Atlanta, GA", "Other"],
            index=1
        )
        cat_opt = st.selectbox(
            "Discipline Category",
            options=["Data & Analytics", "Software & Engineering", "Management & Leadership", "Sales & Account Management", "Finance & Accounting", "Other"],
            index=0 if "data" in pref.get("preferred_role", "").lower() else 1
        )

    if st.button("Predict Annual Compensation", type="primary", use_container_width=True):
        if pipeline is not None:
            input_df = pd.DataFrame([{
                "formatted_experience_level": exp_opt,
                "formatted_work_type": wt_opt,
                "remote_status": rem_opt,
                "clean_location": loc_opt,
                "job_category": cat_opt
            }])
            try:
                pred_sal = pipeline.predict(input_df)[0]
                st.success(f"### 💼 Estimated Annual Salary: **${pred_sal:,.2f} USD**")
                st.caption("Prediction generated by Scikit-learn RandomForestRegressor pipeline (MAE: $35,525.24, R²: 0.2699).")
            except Exception as e:
                st.error(f"Prediction error: {e}")
        else:
            st.error("Model file not loaded.")

    st.markdown("---")
    st.subheader("Salary Distribution (Clipped at 99th Percentile for Visual Clarity)")
    show_chart("salary_distribution.png")


# --------------------------------------------------
# PAGE 9: CAREER ROADMAP
# --------------------------------------------------
def render_roadmap_page(user_id: int, user_profile: dict):
    target_role = user_profile["preferences"]["preferred_role"]
    user_skills = user_profile["skills"]

    st.subheader(f"🗺️ Your Career Roadmap: {target_role}")
    st.caption("A dynamic, multi-phase technical curriculum engineered specifically around your identified skill gaps.")

    roadmap_data = generate_career_roadmap(user_skills, target_role)
    sync_roadmap_with_db(user_id, target_role, roadmap_data)

    st.info(f"📌 **Curriculum Summary**: {roadmap_data['summary']}")

    for phase in roadmap_data["phases"]:
        with st.expander(f"**{phase['title']}** ({phase['estimated_weeks']} — {phase['item_count']} Milestones)", expanded=True):
            st.markdown(f"*{phase['focus']}*")
            for item in phase["items"]:
                p_color = "#EF4444" if item["priority"] == "HIGH" else "#F59E0B"
                st.markdown(
                    f"""
                    <div style="background: #F8FAFC; border-left: 4px solid {p_color}; padding: 8px 12px; border-radius: 6px; margin-bottom: 6px;">
                        <div style="display: flex; justify-content: space-between;">
                            <strong>• {item['name']}</strong>
                            <span style="color: {p_color}; font-weight: 600; font-size: 0.8rem;">{item['priority']} PRIORITY</span>
                        </div>
                        <span style="font-size: 0.82rem; color: #475569;">{item['why']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# --------------------------------------------------
# PAGE 10: RECOMMENDED PROJECTS
# --------------------------------------------------
def render_projects_page(user_profile: dict):
    target_role = user_profile["preferences"]["preferred_role"]
    user_skills = user_profile["skills"]

    st.subheader("💡 Recommended Capstone & Portfolio Projects")
    st.caption(f"Rule-based portfolio deliverables specifically selected to resolve your skill gaps in {target_role}.")

    projects = recommend_projects(user_skills, target_role)

    for p in projects:
        diff_color = "#10B981" if "Beginner" in p["difficulty"] else ("#3B82F6" if "Intermediate" in p["difficulty"] else "#8B5CF6")
        with st.container():
            st.markdown(
                f"""
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 16px; border-radius: 10px; margin-bottom: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0; color: #0F172A;">📁 {p['title']}</h4>
                        <span style="background: {diff_color}; color: white; padding: 2px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">{p['difficulty']}</span>
                    </div>
                    <p style="margin: 8px 0 6px 0; font-size: 0.9rem; color: #334155;">{p['outcome']}</p>
                    <div style="font-size: 0.82rem; color: #2563EB; margin-bottom: 4px;">
                        <strong>Target Skills Developed:</strong> {', '.join(p['skills_developed'])}
                    </div>
                    <div style="font-size: 0.82rem; color: #64748B;">
                        <strong>Tech Stack:</strong> {p['tech_stack']} &nbsp;|&nbsp; <strong>Expected Deliverable:</strong> {p['deliverable']}
                    </div>
                    <p style="margin: 8px 0 0 0; font-size: 0.82rem; color: #059669; font-style: italic;">
                        <strong>Why Recommended:</strong> {p['why_recommended']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )


# --------------------------------------------------
# PAGE 11: PROGRESS TRACKER
# --------------------------------------------------
def render_progress_page(user_id: int):
    st.subheader("📊 Roadmap Progress & Milestone Tracker")
    st.caption("Update your status across roadmap competencies. Your progress is saved in real-time to SQLite.")

    summary = get_user_progress_summary(user_id)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Overall Progress", f"{summary['progress_percentage']}%")
    c2.metric("Completed Items", f"{summary['completed_items']} / {summary['total_items']}")
    c3.metric("Skills Mastered", f"{summary['completed_skills']}")
    c4.metric("Projects Finished", f"{summary['completed_projects']}")

    st.progress(summary["progress_percentage"] / 100.0)
    st.markdown("---")

    items = get_user_progress_items(user_id)
    if not items:
        st.info("No roadmap items currently tracked. Visit the 'Career Roadmap' page to generate your personalized path.")
        return

    # Group by phase
    phases = {}
    for itm in items:
        phases.setdefault(itm["phase"], []).append(itm)

    for phase_name, phase_items in phases.items():
        st.markdown(f"#### {phase_name}")
        for itm in phase_items:
            c_name, c_stat, c_btn = st.columns([3, 1.5, 1])
            c_name.markdown(f"**{itm['item_name']}** ({itm['item_type']})")
            new_stat = c_stat.selectbox(
                "Status",
                options=["Not Started", "In Progress", "Completed"],
                index=["Not Started", "In Progress", "Completed"].index(itm["status"]),
                key=f"status_select_{itm['id']}",
                label_visibility="collapsed"
            )
            if new_stat != itm["status"]:
                update_item_status(user_id, itm["item_name"], itm["item_type"], new_stat)
                st.rerun()

            if itm["status"] == "Completed":
                c_btn.markdown("✅ *Done*")
            elif itm["status"] == "In Progress":
                c_btn.markdown("⏳ *Active*")
            else:
                c_btn.markdown("⚪ *Pending*")
        st.markdown("<br>", unsafe_allow_html=True)


# --------------------------------------------------
# PAGE 12: ABOUT & ARCHITECTURE
# --------------------------------------------------
def render_about_page():
    st.subheader("ℹ️ About SkillSight V2")
    st.markdown(
        """
        ### System Vision & Academic Positioning
        **SkillSight** is a personalized career intelligence and skill roadmap platform that analyzes job-market data
        against an individual's academic background, technical competencies, career interests, and preferences to:
        - Identify transparent, data-grounded skill gaps.
        - Highlight market-relevant technologies with verified job posting evidence.
        - Generate explainable, multi-phase learning roadmaps.
        - Recommends tailored hands-on portfolio projects.

        ### What the System Is NOT
        - It is **NOT** a recruitment agency or job-placement guarantee.
        - It is **NOT** a replacement for professional human mentorship.
        - It does **NOT** invent ungrounded future growth predictions.

        ### Platform Architecture
        ```
                            SKILLSIGHT
                                |
                +---------------+---------------+
                |                               |
           JOB MARKET DATA                 USER PROFILE
           (15,886 Postings)               (SQLite DB)
                |                               |
                ↓                               ↓
        Skill Extraction                Academic Profile
                |                       Skills & Proficiency
                ↓                       Career Preferences
        Market Analysis                         |
                |                               |
                +---------------+---------------+
                                ↓
                         PERSONALIZATION
                                |
                +---------------+---------------+
                |               |               |
            Skill Gap       Role Match     Tech Radar
                |               |               |
                +---------------+---------------+
                                ↓
                       CAREER INTELLIGENCE
                                |
                +---------------+---------------+
                |               |               |
             Roadmap        Projects         Salary
                |
                ↓
           Progress Tracking
        ```
        """
    )


# --------------------------------------------------
# MAIN APPLICATION ROUTING
# --------------------------------------------------
def main():
    user = st.session_state.get("user")

    if not user:
        render_auth_page()
        return

    user_id = user["id"]
    user_profile = get_user_profile(user_id)
    target_role = user_profile["preferences"]["preferred_role"]
    user_skills = user_profile["skills"]

    # Compute live personalization metrics
    readiness_data = calculate_career_readiness(user_profile, user_skills, target_role)
    progress_data = get_user_progress_summary(user_id)

    # Sidebar Navigation
    st.sidebar.markdown(
        """
        <div style="padding-bottom: 10px;">
            <h2 style="margin: 0; color: #1E293B;">💼 SkillSight</h2>
            <span style="color: #2563EB; font-weight: 600; font-size: 0.85rem;">Career Intelligence Platform</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    pages = [
        "Home",
        "My Profile",
        "Skill Analysis",
        "Skill Gap",
        "Job Market",
        "Emerging Technologies",
        "Career Roles",
        "Salary Insights",
        "Career Roadmap",
        "Recommended Projects",
        "Progress Tracker",
        "About"
    ]

    selected_page = st.sidebar.radio(
        "Navigation",
        pages,
        index=pages.index(st.session_state["nav_choice"]) if st.session_state["nav_choice"] in pages else 0,
        label_visibility="collapsed"
    )
    st.session_state["nav_choice"] = selected_page

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Logged in as:**\n{user['name']}\n`{user['email']}`")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        logout()

    # Render top banner
    render_personalized_banner(user_profile, readiness_data, progress_data)

    # Route pages
    if selected_page == "Home":
        render_home_page(user_profile, readiness_data, progress_data)
    elif selected_page == "My Profile":
        render_profile_page(user_id, user_profile)
    elif selected_page == "Skill Analysis":
        render_skill_analysis_page(user_profile)
    elif selected_page == "Skill Gap":
        render_skill_gap_page(user_profile)
    elif selected_page == "Job Market":
        render_job_market_page()
    elif selected_page == "Emerging Technologies":
        render_emerging_tech_page()
    elif selected_page == "Career Roles":
        render_career_roles_page(user_profile)
    elif selected_page == "Salary Insights":
        render_salary_page(user_profile)
    elif selected_page == "Career Roadmap":
        render_roadmap_page(user_id, user_profile)
    elif selected_page == "Recommended Projects":
        render_projects_page(user_profile)
    elif selected_page == "Progress Tracker":
        render_progress_page(user_id)
    elif selected_page == "About":
        render_about_page()


if __name__ == "__main__":
    main()
