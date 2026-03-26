import sqlite3

# SECURITY ISSUE: No connection pooling, raw SQL execution
def execute_query(query, params=None):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    if params:
        # BUG: Still vulnerable to injection if query has placeholders
        cursor.execute(query, params)
    else:
        cursor.execute(query)  # Direct execution
    
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

# CODE QUALITY ISSUE: Inconsistent return types
def get_user_by_id(user_id):
    try:
        # SQL INJECTION: Direct string formatting
        result = execute_query(f"SELECT * FROM users WHERE id = {user_id}")
        if result:
            return result[0]
        return None
    except Exception as e:
        # CODE QUALITY ISSUE: Returning exception as string
        return str(e)