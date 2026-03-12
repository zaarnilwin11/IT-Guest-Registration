from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client
import config

app = Flask(__name__)
app.secret_key = "SUPER_SECRET_KEY"

supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_ANON_KEY)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if "login" in request.form:
            email = request.form["email"]
            password = request.form["password"]
            result = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if result.user:
                session["user_id"] = result.user.id
                return redirect(url_for('dashboard'))
            else:
                return render_template("login.html", error="Invalid login.")
        elif "signup" in request.form:
            email = request.form["email"]
            password = request.form["password"]
            result = supabase.auth.sign_up({"email": email, "password": password})
            if result.user:
                return render_template("login.html", message="Check your email to confirm registration.")
            else:
                return render_template("login.html", error="Sign up failed.")
        elif "guest" in request.form:
            return redirect(url_for("guest_registration"))
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" in session:
        return "Welcome to the Dashboard!"
    return redirect(url_for("login"))

@app.route("/guest_registration")
def guest_registration():
    return "Guest Registration Page."

if __name__ == "__main__":
    app.run(debug=True)