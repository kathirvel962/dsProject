"""SkillSight - Authentication Module

Implements secure, explainable password hashing using Python's standard library
hashlib (PBKDF2-HMAC-SHA256 with 100,000 rounds and unique salt per user)
along with user registration, login verification, and profile loading.
"""

import hashlib
import os
import secrets
import sqlite3
from typing import Optional, Tuple, Dict, Any


def hash_password(password: str) -> str:
    """Hash a plaintext password using PBKDF2-HMAC-SHA256 with a unique random salt."""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100_000,
    )
    return f"{salt}${key.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify a plaintext password against the stored salt$hash string."""
    try:
        if not stored_hash or "$" not in stored_hash:
            return False
        salt, key_hex = stored_hash.split("$", 1)
        new_key = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100_000,
        )
        return secrets.compare_digest(new_key.hex(), key_hex)
    except Exception:
        return False


def register_user(name: str, email: str, password: str) -> Tuple[bool, str, Optional[int]]:
    """Register a new user account and initialize their career profile.
    
    Returns:
        (success: bool, message: str, user_id: Optional[int])
    """
    from src.database import get_connection

    name = name.strip()
    email = email.strip().lower()

    if not name:
        return False, "Please enter your full name.", None
    if not email or "@" not in email:
        return False, "Please provide a valid email address.", None
    if not password or len(password) < 4:
        return False, "Password must be at least 4 characters long.", None

    pwd_hash = hash_password(password)

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            # Check for existing email
            cursor.execute("SELECT id FROM users WHERE email = ?;", (email,))
            if cursor.fetchone():
                return False, "An account with this email already exists. Please log in.", None

            cursor.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?);",
                (name, email, pwd_hash),
            )
            user_id = cursor.lastrowid

            # Initialize empty/default user profile
            cursor.execute(
                """
                INSERT INTO user_profiles (user_id, degree, branch, academic_year, graduation_year, cgpa, education_level)
                VALUES (?, 'B.Tech', 'Computer Science', '3rd Year', 2026, 8.0, 'Undergraduate');
                """,
                (user_id,),
            )

            # Initialize default career preference
            cursor.execute(
                """
                INSERT INTO career_preferences (user_id, preferred_role, preferred_location, work_mode)
                VALUES (?, 'Software Developer', 'United States', 'Remote');
                """,
                (user_id,),
            )

            return True, "Account registered successfully!", user_id

    except sqlite3.IntegrityError:
        return False, "An account with this email already exists.", None
    except Exception as err:
        return False, f"Database error during registration: {err}", None


def login_user(email: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """Authenticate an existing user and return their account information.
    
    Returns:
        (success: bool, message: str, user_dict: Optional[dict])
    """
    from src.database import get_connection

    email = email.strip().lower()
    if not email or not password:
        return False, "Please provide both email and password.", None

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, email, password_hash, created_at FROM users WHERE email = ?;",
                (email,),
            )
            row = cursor.fetchone()
            if not row:
                return False, "No account found with this email. Please register.", None

            if not verify_password(password, row["password_hash"]):
                return False, "Incorrect password. Please try again.", None

            user_data = {
                "id": row["id"],
                "name": row["name"],
                "email": row["email"],
                "created_at": str(row["created_at"]),
            }
            return True, "Login successful!", user_data

    except Exception as err:
        return False, f"Database error during login: {err}", None


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve user account information by user_id."""
    from src.database import get_connection

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, email, created_at FROM users WHERE id = ?;",
                (user_id,),
            )
            row = cursor.fetchone()
            if row:
                return {
                    "id": row["id"],
                    "name": row["name"],
                    "email": row["email"],
                    "created_at": str(row["created_at"]),
                }
    except Exception:
        pass
    return None
