from flask import Flask, render_template, request, redirect, session, jsonify
import subprocess

app = Flask(__name__)
app.secret_key = "super_secret_key_123"   # Change this for security

# Dummy Login Credentials
USERNAME = "admin"
PASSWORD = "1234"

gesture_process = None

@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")


# ---------- LOGIN ----------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        if user.strip() == "" or pwd.strip() == "":
            return render_template("signup.html", error="All fields required")

        # Save user (basic example)
        with open("users.txt", "a") as f:
            f.write(f"{user}:{pwd}\n")

        return redirect("/login")

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        if user == USERNAME and pwd == PASSWORD:
            session["user"] = user
            return redirect("/dashboard")

        return render_template("login.html", error="Invalid Username or Password")

    return render_template("login.html")


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html")


# ---------- API: Start Gesture System ----------
@app.route("/start")
def start_system():
    global gesture_process
    if gesture_process is None:
        gesture_process = subprocess.Popen(["python", "final.py"])
        return jsonify({"status": "started"})
    return jsonify({"status": "already running"})


# ---------- API: Stop Gesture System ----------
@app.route("/stop")
def stop_system():
    global gesture_process
    if gesture_process is not None:
        gesture_process.terminate()
        gesture_process = None
        return jsonify({"status": "stopped"})
    return jsonify({"status": "not running"})


@app.route("/status")
def get_status():
    return jsonify({"running": gesture_process is not None})


if __name__ == "__main__":
    app.run(debug=True)
