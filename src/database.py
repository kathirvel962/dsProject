"""SkillSight - Database Module (SQLite)

Provides lightweight, explainable, and zero-configuration local database storage
for user accounts, academic career profiles, technical skills with proficiency levels,
career preferences, and learning roadmap progress.
"""

import os
import sqlite3
from contextlib import contextmanager

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_DIR = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(DB_DIR, "skillsight.db")


def get_db_path() -> str:
    """Return the absolute path to the SQLite database file."""
    os.makedirs(DB_DIR, exist_ok=True)
    return DB_PATH


@contextmanager
def get_connection():
    """Context manager for obtaining a database connection with row factory."""
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    # Enable foreign key support
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db(db_path: str = None):
    """Initialize all required tables for the SkillSight personalization platform."""
    target_path = db_path if db_path else get_db_path()
    os.makedirs(os.path.dirname(target_path) if os.path.dirname(target_path) else ".", exist_ok=True)

    with sqlite3.connect(target_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        # 1. Users Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 2. User Profiles Table (Academic & Background)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            degree TEXT DEFAULT 'B.Tech',
            branch TEXT DEFAULT 'Computer Science',
            academic_year TEXT DEFAULT '3rd Year',
            graduation_year INTEGER DEFAULT 2026,
            cgpa REAL DEFAULT 8.5,
            education_level TEXT DEFAULT 'Undergraduate',
            certifications TEXT DEFAULT '',
            projects_summary TEXT DEFAULT '',
            portfolio_url TEXT DEFAULT '',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # 3. User Skills Table (with Proficiency Level)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            skill_name TEXT NOT NULL,
            category TEXT DEFAULT 'General',
            proficiency TEXT CHECK(proficiency IN ('Beginner', 'Intermediate', 'Advanced')) DEFAULT 'Intermediate',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, skill_name),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # 4. Career Preferences Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS career_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            preferred_role TEXT DEFAULT 'Data Scientist',
            preferred_location TEXT DEFAULT 'United States',
            work_mode TEXT DEFAULT 'Remote',
            expected_salary_min REAL DEFAULT 70000.0,
            expected_salary_max REAL DEFAULT 110000.0,
            preferred_industry TEXT DEFAULT 'Technology & Software',
            employment_type TEXT DEFAULT 'Full-time',
            experience_level TEXT DEFAULT 'Entry level',
            career_interests TEXT DEFAULT 'Machine Learning, Data Engineering, AI Systems',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # 5. Learning Progress Table (Roadmap & Projects Tracker)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            item_type TEXT CHECK(item_type IN ('Skill', 'Project')) DEFAULT 'Skill',
            phase TEXT DEFAULT 'Phase 1 - Foundation',
            status TEXT CHECK(status IN ('Not Started', 'In Progress', 'Completed')) DEFAULT 'Not Started',
            target_role TEXT DEFAULT 'Data Scientist',
            completed_at TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, item_name, item_type),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        conn.commit()

    # Seed demo user if no users exist
    _seed_demo_user(target_path)


def _seed_demo_user(target_path: str):
    """Seed an academic demo profile so evaluators can immediately test personalized features."""
    from src.auth import hash_password

    with sqlite3.connect(target_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as cnt FROM users;")
        row = cursor.fetchone()
        if row and row["cnt"] > 0:
            return  # Already seeded or users exist

        # Create Demo User: Alex Morgan
        demo_email = "demo@skillsight.edu"
        demo_password = "demo123"
        hashed = hash_password(demo_password)

        cursor.execute("""
        INSERT INTO users (name, email, password_hash)
        VALUES (?, ?, ?);
        """, ("Alex Morgan", demo_email, hashed))
        user_id = cursor.lastrowid

        # Profile
        cursor.execute("""
        INSERT INTO user_profiles (
            user_id, degree, branch, academic_year, graduation_year, cgpa,
            education_level, certifications, projects_summary, portfolio_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            user_id,
            "B.Tech",
            "Computer Science & Engineering",
            "3rd Year",
            2026,
            8.65,
            "Undergraduate",
            "AWS Certified Cloud Practitioner, IBM Data Science Certificate",
            "Built a Customer Churn Predictor using Scikit-Learn and an exploratory EDA Dashboard.",
            "https://github.com/alex-morgan-cs"
        ))

        # Initial Skills: Python, SQL, Pandas, Java, Git
        demo_skills = [
            ("Python", "Programming Languages", "Intermediate"),
            ("SQL", "Databases", "Intermediate"),
            ("Pandas", "AI / Data", "Intermediate"),
            ("NumPy", "AI / Data", "Beginner"),
            ("Java", "Programming Languages", "Intermediate"),
            ("Git", "DevOps & Tools", "Beginner"),
            ("Excel", "Data / BI", "Advanced"),
        ]
        for s_name, cat, prof in demo_skills:
            cursor.execute("""
            INSERT INTO user_skills (user_id, skill_name, category, proficiency)
            VALUES (?, ?, ?, ?);
            """, (user_id, s_name, cat, prof))

        # Career Preferences: Target = Data Scientist
        cursor.execute("""
        INSERT INTO career_preferences (
            user_id, preferred_role, preferred_location, work_mode,
            expected_salary_min, expected_salary_max, preferred_industry,
            employment_type, experience_level, career_interests
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            user_id,
            "Data Scientist",
            "New York, NY",
            "Hybrid",
            85000.0,
            125000.0,
            "Technology & Analytics",
            "Full-time",
            "Entry level",
            "Machine Learning, Big Data Analytics, Predictive Modeling"
        ))

        # Learning Progress Initial Seed
        demo_progress = [
            ("Python", "Skill", "Phase 1 - Foundation", "Completed"),
            ("SQL", "Skill", "Phase 1 - Foundation", "Completed"),
            ("Pandas", "Skill", "Phase 2 - Core Data Science", "Completed"),
            ("Scikit-learn", "Skill", "Phase 2 - Core Data Science", "In Progress"),
            ("Machine Learning", "Skill", "Phase 3 - Machine Learning", "In Progress"),
            ("Deep Learning", "Skill", "Phase 4 - Advanced Specialization", "Not Started"),
            ("AWS", "Skill", "Phase 4 - Cloud & Deployment", "Not Started"),
            ("Docker", "Skill", "Phase 4 - Cloud & Deployment", "Not Started"),
            ("Customer Churn Prediction", "Project", "Phase 5 - Portfolio Projects", "Completed"),
            ("Job Market Analysis Dashboard", "Project", "Phase 5 - Portfolio Projects", "In Progress"),
        ]
        for item, itype, ph, st in demo_progress:
            cursor.execute("""
            INSERT INTO learning_progress (user_id, item_name, item_type, phase, status, target_role)
            VALUES (?, ?, ?, ?, ?, ?);
            """, (user_id, item, itype, ph, st, "Data Scientist"))

        conn.commit()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)
