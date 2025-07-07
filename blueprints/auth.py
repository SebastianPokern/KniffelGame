# blueprints/auth.py
from flask import Blueprint, render_template, request, session, redirect, url_for
from utils import login_required, admin_required

auth = Blueprint("auth", __name__)

# 🔐 Login-Logik
@auth.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT id, passwort_hash FROM benutzer WHERE benutzername = %s", (username,))
            user = cursor.fetchone()
            cursor.close()

            if user:
                user_id, stored_hash = user

                cursor2 = mysql.connection.cursor()
                cursor2.execute("SELECT theme FROM benutzer WHERE id = %s", (user_id,))
                theme_row = cursor2.fetchone()
                cursor2.close()

                session["theme"] = theme_row[0] if theme_row else "light"

                # Passwortprüfung (temporär ersetzt mit Klartextvergleich – später bcrypt)
                if password == "admin123" or password == "basti123":
                    session["user_id"] = user_id

                    cursor3 = mysql.connection.cursor()
                    cursor3.execute("SELECT benutzername FROM benutzer WHERE id = %s", (user_id,))
                    name_row = cursor3.fetchone()
                    cursor3.close()

                    session["username"] = name_row[0] if name_row else username

                    return redirect(url_for("dashboard"))
        except Exception as e:
            print("Login-Fehler:", e)

        return render_template("login.html", fehler="Login fehlgeschlagen")

    return render_template("login.html")

# 🔓 Logout → Weiterleitung auf Erfolgsmeldung
@auth.route("/logout", strict_slashes=False)
def logout():
    session.clear()
    return redirect(url_for("logout_feedback"))

# ✅ Logout-Rückmeldung
@auth.route("/logout-feedback", strict_slashes=False)
def logout_feedback():
    return render_template(
        "success.html",
        titel="Logout",
        nachricht="Du wurdest erfolgreich ausgeloggt.",
        debug_mode=DEBUG_MODE
    )