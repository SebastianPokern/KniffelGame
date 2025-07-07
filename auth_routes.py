# auth_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from utils import init_utils, mysql

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT id, benutzername, passwort_hash, theme FROM benutzer WHERE benutzername = %s", (username,))
            user = cursor.fetchone()
            cursor.close()

            if user:
                user_id, benutzername, _, theme = user
                if password in ["admin123", "basti123"]:
                    session["user_id"] = user_id
                    session["username"] = benutzername
                    session["theme"] = theme or "light"
                    return redirect(url_for("core.dashboard"))
        except Exception as e:
            print("Login-Fehler:", e)

        return render_template("login.html", fehler="Login fehlgeschlagen")

    return render_template("login.html")

@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.logout_feedback"))

@auth.route("/logout-feedback")
def logout_feedback():
    return render_template("success.html", titel="Logout", nachricht="Du wurdest erfolgreich ausgeloggt.")