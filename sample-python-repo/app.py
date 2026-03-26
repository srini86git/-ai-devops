import os
import sqlite3
from flask import Flask, request, jsonify
from utils.auth import verify_token
from database.db_handler import execute_query

app = Flask(__name__)

# SECURITY ISSUE: Hardcoded secret key (should be in environment variable)
SECRET_KEY = "hardcoded-super-secret-key-12345"

# SECURITY ISSUE: Debug mode enabled in production
app.config['DEBUG'] = True

# INSECURE PASSWORD HANDLING
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # SECURITY ISSUE: Storing/checking plaintext passwords
    # SECURITY ISSUE: No rate limiting
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({"status": "success", "token": SECRET_KEY})
    return jsonify({"status": "failed"}), 401

# SQL INJECTION VULNERABILITY
@app.route('/user/<username>')
def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # DANGEROUS: String concatenation instead of parameterized query
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return jsonify(user)

# DEPRECATED/INSECURE FUNCTION USAGE
@app.route('/data')
def get_data():
    import pickle
    data = request.args.get('payload')
    # SECURITY ISSUE: Pickle deserialization from user input
    return pickle.loads(data.encode())  # RCE vulnerability

# CODE QUALITY ISSUE: Bare except clause
@app.route('/admin/delete')
def delete_user():
    try:
        user_id = request.args.get('id')
        execute_query(f"DELETE FROM users WHERE id = {user_id}")
    except:  # BUG: Bare except hides all errors
        pass
    
    return jsonify({"status": "deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # SECURITY ISSUE: Binding to all interfaces