# core.py
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from utils import init_utils, login_required, admin_required, mysql, paginate, now_str
from datetime import datetime

core = Blueprint("core", __name__)

# 🏠 Startseite → Weiterleitung auf Dashboard
@core.route("/", strict_slashes=False)
def home_redirect():
    return redirect(url_for("core.dashboard"))

@core.route("/dashboard", strict_slashes=False)
@login_required
def dashboard(user):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT zeitpunkt 
            FROM logeintraege 
            WHERE meldung = 'Schalter aktiviert' 
            ORDER BY zeitpunkt DESC LIMIT 1
        """)
        result = cursor.fetchone()
        cursor.close()

        letzter_status = result[0].strftime("%d.%m.%Y um %H:%M Uhr") if result else None
        return render_template("home.html", benutzer=user["benutzername"], letzter_status=letzter_status)

    except Exception as e:
        return render_template("fehler.html", fehlermeldung=f"Fehler beim Dashboard: {e}"), 500

# 👤 Profil anzeigen
@core.route("/profil", strict_slashes=False)
@login_required
def profil(user):
    return render_template("profil.html",
        benutzername=user["benutzername"],
        email=user["email"],
        theme=user["theme"])


# 🎨 Theme speichern
@core.route("/theme", methods=["POST"])
@login_required
def theme(user):
    neues_theme = request.form.get("theme", "light")
    session["theme"] = neues_theme
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE benutzer SET theme = %s WHERE id = %s", (neues_theme, user["id"]))
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        return render_template("fehler.html", fehlermeldung=f"Fehler beim Speichern des Themes: {e}"), 500
    return redirect(request.referrer or url_for("core.dashboard"))