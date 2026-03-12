from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import bcrypt

app = Flask(__name__)
app.secret_key = 'SUPER_SECRET_KEY'  # Change this!

# Connect to PostgreSQL
conn = psycopg2.connect("postgresql://postgres:63V$+a8y$EzeS2K@db.xhubmgybtaxmapqhjljb.supabase.co:5432/postgres")
cur = conn.cursor()

# Create users table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL
)
""")
conn.commit()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if "login" in request.form:
            username = request.form["username"]
            password = request.form["password"].encode('utf-8')
            cur.execute("SELECT password FROM users WHERE username=%s", (username,))
            user = cur.fetchone()
            if user and bcrypt.checkpw(password, user[0].encode("utf-8")):
                session["username"] = username
                return redirect(url_for('dashboard'))
            else:
                return render_template("login.html", error="Invalid login.")
        elif "signup" in request.form:
            username = request.form["username"]
            password = request.form["password"].encode('utf-8')
            hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")
            try:
                cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed))
                conn.commit()
                return render_template("login.html", message="Sign up successful! Please log in.")
            except psycopg2.IntegrityError:
                conn.rollback()
                return render_template("login.html", error="Username exists!")
        elif "guest" in request.form:
            return redirect(url_for("guest_registration"))
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return f"Welcome, {session['username']}! (User Home)"
    return redirect(url_for("login"))

@app.route("/guest_registration")
def guest_registration():
    # Implementation of guest registration page goes here
    return "Guest Registration Page (Implement form here)."

if __name__ == "__main__":
    app.run(debug=True)