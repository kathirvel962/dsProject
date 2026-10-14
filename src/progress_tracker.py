"""SkillSight - Learning Progress Tracker Module

Synchronizes, stores, and tracks progress across roadmap skills and portfolio projects
in SQLite, computing completion percentages and milestones.
"""

from typing import Dict, List, Any
from src.database import get_connection


def sync_roadmap_with_db(user_id: int, target_role: str, roadmap_data: Dict[str, Any]):
    """Ensure all generated roadmap items exist in the user's learning_progress table."""
    with get_connection() as conn:
        cursor = conn.cursor()
        for phase in roadmap_data.get("phases", []):
            phase_name = phase["title"]
            for item in phase.get("items", []):
                item_name = item["name"]
                item_type = item.get("type", "Skill")
                if item_type not in ("Skill", "Project"):
                    item_type = "Skill"
                
                # Check if item already tracked
                cursor.execute("""
                SELECT id FROM learning_progress
                WHERE user_id = ? AND item_name = ? AND item_type = ?;
                """, (user_id, item_name, item_type))
                if not cursor.fetchone():
                    cursor.execute("""
                    INSERT INTO learning_progress (user_id, item_name, item_type, phase, status, target_role)
                    VALUES (?, ?, ?, ?, 'Not Started', ?);
                    """, (user_id, item_name, item_type, phase_name, target_role))


def get_user_progress_summary(user_id: int) -> Dict[str, Any]:
    """Calculate aggregate completion statistics for a user's roadmap."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT item_type, status, COUNT(*) as cnt
        FROM learning_progress
        WHERE user_id = ?
        GROUP BY item_type, status;
        """, (user_id,))
        rows = cursor.fetchall()

        total_items = 0
        completed_items = 0
        in_progress_items = 0
        not_started_items = 0
        completed_skills = 0
        completed_projects = 0

        for r in rows:
            itype = r["item_type"]
            stat = r["status"]
            count = r["cnt"]

            total_items += count
            if stat == "Completed":
                completed_items += count
                if itype == "Skill":
                    completed_skills += count
                elif itype == "Project":
                    completed_projects += count
            elif stat == "In Progress":
                in_progress_items += count
            else:
                not_started_items += count

        progress_pct = round((completed_items / total_items * 100.0), 1) if total_items > 0 else 0.0

        return {
            "total_items": total_items,
            "completed_items": completed_items,
            "in_progress_items": in_progress_items,
            "not_started_items": not_started_items,
            "completed_skills": completed_skills,
            "completed_projects": completed_projects,
            "progress_percentage": progress_pct
        }


def get_user_progress_items(user_id: int) -> List[Dict[str, Any]]:
    """Retrieve all tracked roadmap items for a user ordered by phase and name."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, item_name, item_type, phase, status, target_role, completed_at, updated_at
        FROM learning_progress
        WHERE user_id = ?
        ORDER BY phase ASC, id ASC;
        """, (user_id,))
        rows = cursor.fetchall()
        return [
            {
                "id": r["id"],
                "item_name": r["item_name"],
                "item_type": r["item_type"],
                "phase": r["phase"],
                "status": r["status"],
                "target_role": r["target_role"],
                "completed_at": str(r["completed_at"]) if r["completed_at"] else None
            }
            for r in rows
        ]


def update_item_status(user_id: int, item_name: str, item_type: str, new_status: str) -> bool:
    """Update the status of a specific roadmap item in SQLite."""
    if new_status not in ("Not Started", "In Progress", "Completed"):
        return False

    with get_connection() as conn:
        cursor = conn.cursor()
        if new_status == "Completed":
            cursor.execute("""
            UPDATE learning_progress
            SET status = ?, completed_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ? AND item_name = ? AND item_type = ?;
            """, (new_status, user_id, item_name, item_type))
        else:
            cursor.execute("""
            UPDATE learning_progress
            SET status = ?, completed_at = NULL, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ? AND item_name = ? AND item_type = ?;
            """, (new_status, user_id, item_name, item_type))
    return True
