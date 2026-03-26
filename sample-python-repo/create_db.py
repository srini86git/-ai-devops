# create_db.py
import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
''')

# Insert test data
cursor.execute("INSERT INTO users (id, username, password) VALUES (1, 'admin', 'admin123')")
cursor.execute("INSERT INTO users (id, username, password) VALUES (2, 'user1', 'pass123')")

conn.commit()
conn.close()
print("Database created successfully!")