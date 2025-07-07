# core_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from utils import init_utils, login_required, admin_required, mysql, paginate, now_str
from functions import sende_email, pruefe_inaktivitaet
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

@core.route("/schalter-ui", strict_slashes=False)
@login_required
def schalter_ui(user):
    return render_template("schalter.html", benutzer=user["benutzername"])

@core.route("/schalter", methods=["POST"])
@login_required
def schalter_aktivieren(user):
    zeitpunkt = datetime.now()
    meldung = "Schalter aktiviert"

    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO logeintraege (zeitpunkt, benutzer_id, meldung) VALUES (%s, %s, %s)",
            (zeitpunkt, user["id"], meldung)
        )
        mysql.connection.commit()
        cursor.close()

        return jsonify({
            "erfolg": True,
            "meldung": f"Schalter aktiviert am {now_str()}"
        })
    except Exception as e:
        return jsonify({"erfolg": False, "fehler": str(e)})

@core.route("/api/pruefe-schalter", strict_slashes=False)
def pruefung_aus_browser():
    pruefe_inaktivitaet()
    return "", 204

# 📊 Systemstatus mit Pagination
@core.route("/status", strict_slashes=False)
@login_required
def status(user):
    try:
        seite = int(request.args.get("seite", 1))
        cursor = mysql.connection.cursor()

        # 📥 Eintragsmenge aus Einstellungen holen
        cursor.execute("SELECT anzahl_logeintraege FROM einstellungen WHERE id = 1")
        eintrag_config = cursor.fetchone()
        eintraege_pro_seite = eintrag_config[0] if eintrag_config else 20

        # ✅ Letzter Logeintrag (wird hervorgehoben)
        cursor.execute("SELECT zeitpunkt, benutzer_id FROM logeintraege ORDER BY zeitpunkt DESC LIMIT 1")
        letzter = cursor.fetchone()

        # 📄 Verlaufseinträge mit Pagination laden
        verlauf_query = """
            SELECT zeitpunkt, benutzer_id, meldung 
            FROM logeintraege 
            ORDER BY zeitpunkt DESC 
            LIMIT %s OFFSET %s
        """
        verlauf, seitenanzahl = paginate(
            query=verlauf_query,
            page=seite,
            per_page=eintraege_pro_seite,
            cursor=cursor,
            count_query="SELECT COUNT(*) FROM logeintraege"
        )
        cursor.close()

        # 🔄 Logeinträge um Benutzernamen erweitern
        logliste = []
        for zeitpunkt, benutzer_id, meldung in verlauf:
            benutzername = "System"
            if benutzer_id:
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT benutzername FROM benutzer WHERE id = %s", (benutzer_id,))
                result = cursor.fetchone()
                cursor.close()
                if result:
                    benutzername = result[0]

            logliste.append({
                "zeitpunkt": zeitpunkt.strftime("%d.%m.%Y %H:%M"),
                "benutzer": benutzername,
                "meldung": meldung,
                "typ": "fehler" if "nicht aktiviert" in meldung.lower() else "ok"
            })

        # 🕓 Letzter Eintrag (oben)
        letzter_zeitpunkt = letzter[0].strftime("%d.%m.%Y um %H:%M Uhr") if letzter else None
        letzter_benutzer = "Unbekannt"
        if letzter and letzter[1]:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT benutzername FROM benutzer WHERE id = %s", (letzter[1],))
            user_row = cursor.fetchone()
            cursor.close()
            if user_row:
                letzter_benutzer = user_row[0]

        return render_template("status.html",
            eintrag_vorhanden=bool(letzter),
            zeitpunkt=letzter_zeitpunkt,
            benutzer=letzter_benutzer,
            logliste=logliste,
            seite=seite,
            seitenanzahl=seitenanzahl
        )

    except Exception as e:
        return render_template("fehler.html", fehlermeldung=f"Fehler beim Laden der Statusseite: {e}"), 500


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

@core.route("/manuelle-pruefung", strict_slashes=False)
def manuelle_pruefung():
    pruefe_inaktivitaet()
    return render_template("success.html", titel="Manuelle Prüfung", nachricht="Intervallprüfung wurde durchgeführt.")

# 📬 Test-E-Mail Standard
@core.route("/test-mail-default", strict_slashes=False)
@admin_required
def test_mail_default(user):
    sende_email(
        template_name="mail_default.html",
        empfaenger=user["email"],
        daten={
            "nachricht": "Dies ist eine Testnachricht aus dem Standard-Template.",
            "absender": "system@example.com",
            "betreff": "Test-Standard-Mail",
            "timestamp": now_str()
        }
    )
    return render_template("success.html", titel="Testmail", nachricht="Standardmail wurde verschickt.")

# 📬 Test-E-Mail System
@core.route("/test-mail-system", strict_slashes=False)
@admin_required
def test_mail_system(user):
    sende_email(
        template_name="mail_system.html",
        empfaenger=user["email"],
        daten={
            "nachricht": "Es wurde ein kritischer Fehler erkannt!",
            "absender": "system@pixelpriest.de",
            "betreff": "Systemmeldung",
            "timestamp": now_str()
        }
    )
    return render_template("success.html", titel="Testmail", nachricht="Systemmail wurde verschickt.")

# 📬 Testversand der Warnungs-E-Mail
@core.route("/test-mail-warnung", strict_slashes=False)
@admin_required
def test_mail_warnung(user):
    sende_email(
        template_name="mail_warnung.html",
        empfaenger=user["email"],
        daten={
            "absender": "system@example.com",
            "betreff": "Warnung: Manuelle Aktivierung ausstehend",
            "nachricht": "Der Totmann-Schalter wurde seit mehr als 24 Stunden nicht betätigt.",
            "benutzername": user["benutzername"],
            "timestamp": now_str()
        }
    )
    return render_template(
        "success.html",
        titel="Testmail: Warnung",
        nachricht="mail_warnung.html wurde verarbeitet und an den aktuellen Benutzer gesendet.",
        debug_mode=True
    )
