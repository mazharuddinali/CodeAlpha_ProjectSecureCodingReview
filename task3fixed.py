from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False') == 'True'  # Env-based debug

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    # Input validation
    if not username or not password:
        return "Username/password missing!", 400
    
    # Parameterized query
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    
    if user:
        return "Login successful!"
    else:
        return "Invalid credentials!", 401

if __name__ == '__main__':
    app.run()