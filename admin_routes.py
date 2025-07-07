# admin_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from utils import admin_required, mysql

admin = Blueprint("admin", __name__)

@admin.route("/einstellungen", methods=["GET", "POST"])
@admin_required
def einstellungen(user):
    try:
        if request.method == "POST":
            intervall = int(request.form.get("intervall_stunden"))
            max_tage = int(request.form.get("max_inaktiv_tage"))
            email = request.form.get("email_empfaenger")
            anzahl = int(request.form.get("anzahl_logeintraege"))
            client_interval = int(request.form.get("intervall_check_client"))
            server_interval = int(request.form.get("intervall_check_server"))

            cursor = mysql.connection.cursor()
            cursor.execute("""
                UPDATE einstellungen SET 
                intervall_stunden = %s,
                max_inaktiv_tage = %s
                email_empfaenger = %s,
                anzahl_logeintraege = %s,
                intervall_check_client = %s,
                intervall_check_server = %s,
                WHERE id = 1
            """, (intervall, max_tage, email, anzahl))
            mysql.connection.commit()
            cursor.close()

            return render_template("success.html", titel="Einstellungen", nachricht="Gespeichert")

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT intervall_stunden, max_inaktiv_tage, email_empfaenger, anzahl_logeintraege, intervall_check_client, intervall_check_server FROM einstellungen WHERE id = 1")
        daten = cursor.fetchone()
        cursor.close()

        if daten:
            intervall, max_tage, email, anzahl, intervall_check_client, intervall_check_server = daten
            return render_template("einstellungen.html",
                intervall=intervall,
                max_tage=max_tage,
                email=email,
                anzahl_logeintraege=anzahl,
                intervall_check_client=intervall_check_client,
                intervall_check_server=intervall_check_server
            )

        return render_template("fehler.html", fehlermeldung="Einstellungen konnten nicht geladen werden."), 500

    except Exception as e:
        return render_template("fehler.html", fehlermeldung=f"Fehler: {e}"), 500