# admin.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from utils import admin_required, mysql

admin = Blueprint("admin", __name__)

@admin.route("/einstellungen", methods=["GET", "POST"])
@admin_required
def einstellungen(user):
    try:
        if request.method == "POST":
            email = request.form.get("email_empfaenger")
            anzahl = int(request.form.get("anzahl_logeintraege"))

            cursor = mysql.connection.cursor()
            cursor.execute("""
                UPDATE einstellungen SET 
                email_empfaenger = %s,
                anzahl_logeintraege = %s,
                WHERE id = 1
            """, (email, anzahl))
            mysql.connection.commit()
            cursor.close()

            return render_template("success.html", titel="Einstellungen", nachricht="Gespeichert")

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT email_empfaenger, anzahl_logeintraege FROM einstellungen WHERE id = 1")
        daten = cursor.fetchone()
        cursor.close()

        if daten:
            email, anzahl = daten
            return render_template("einstellungen.html",
                email=email,
                anzahl_logeintraege=anzahl
            )

        return render_template("fehler.html", fehlermeldung="Einstellungen konnten nicht geladen werden."), 500

    except Exception as e:
        return render_template("fehler.html", fehlermeldung=f"Fehler: {e}"), 500