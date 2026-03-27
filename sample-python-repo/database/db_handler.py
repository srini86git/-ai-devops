import sqlite3
from typing import Optional

def execute_query(query: str, params: tuple = ()) -> list:
    # FIX: Always uses parameterized queries, consistent return type
    conn = sqlite3.connect('app.db')
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        raise  # FIX: Re-raise instead of swallowing or returning string
    finally:
        conn.close()

def get_user_by_id(user_id: int) -> Optional[tuple]:
    # FIX: Parameterized, consistent return â€” tuple or None only
    result = execute_query("SELECT * FROM users WHERE id = ?", (user_id,))
    return result[0] if result else None