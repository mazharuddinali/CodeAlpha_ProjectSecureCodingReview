# CodeAlpha_ProjectSecureCodingReview

Vulnerable Lines & Their Risks
1. SQL Injection (Critical Risk)
Vulnerable Line:

python
Copy
cursor.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
Why It’s Bad:

Directly embeds user input (username, password) into an SQL query.

Attackers can inject malicious SQL (e.g., ' OR '1'='1 to bypass login).

Fix: Use parameterized queries:

python
Copy
cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
2. Hardcoded Debug Mode (Medium Risk)
Vulnerable Line:

python
Copy
app.run(debug=True)
Why It’s Bad:

Enables debug mode in production, exposing:

Stack traces (leaks sensitive info).

Arbitrary code execution via debug console.

Fix: Disable debug mode or use environment variables:

python
Copy
app.run(debug=False)  # Disable in production
# OR better:
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False') == 'True'
3. Missing Input Validation (Low Risk)
Vulnerable Lines:

python
Copy
username = request.form['username']  # No default/validation
password = request.form['password']  # No length/format checks
Why It’s Bad:

No checks for empty inputs, long strings (DoS risk), or malicious payloads.

Fix: Add validation:

python
Copy
username = request.form.get('username', '').strip()  # Basic sanitization
password = request.form.get('password', '').strip()
if not username or not password:
    return "Username/password missing!", 400
4. Plaintext Passwords (Critical Risk)
Vulnerable Line:

python
Copy
cursor.execute("... password=?", (password,))  # Storing/checking plaintext passwords
Why It’s Bad:

Passwords should never be stored/compared in plaintext.

Fix: Use password hashing (e.g., bcrypt):

python
Copy
import bcrypt
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
# Compare later with:
bcrypt.checkpw(input_password.encode(), stored_hashed_password)
Other Potential Vulnerabilities
No HTTPS (Man-in-the-Middle Attacks)

Flask’s app.run() serves HTTP by default. Use HTTPS in production (e.g., nginx reverse proxy).

No Rate Limiting (Brute-Force Attacks)

Attackers can spam /login. Fix: Use flask-limiter.

No CSRF Protection

Missing CSRF tokens in forms. Fix: Enable Flask-WTF.
