# ✅ functions.py – Globale Hilfsfunktionen

from flask import render_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os

def sende_email(template_name, empfaenger, daten={}):
    try:
        from_address = daten.get("absender", os.getenv("MAIL_FROM", "noreply@example.com"))
        betreff = daten.get("betreff", "Systemnachricht")
        html_body = render_template(template_name, **daten)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = betreff
        msg["From"] = from_address
        msg["To"] = empfaenger
        msg.attach(MIMEText(html_body, "html"))

        if os.getenv("DEBUG_MODE", "false").lower() == "true":
            print(f"[DEBUG] E-Mail an {empfaenger} (nicht gesendet):\n{html_body}")
            return

        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT", 465))
        smtp_user = os.getenv("SMTP_USER")
        smtp_pass = os.getenv("SMTP_PASSWORD")

        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

        print(f"E-Mail an {empfaenger} gesendet.")
    except Exception as e:
        print(f"Fehler beim E-Mail-Versand an {empfaenger}: {e}")

from datetime import datetime, timedelta
from utils import mysql

# 🕵️‍♂️ Totmann-Prüfung: Sendet eine Warnmail bei Inaktivität über das definierte Intervall hinaus
def pruefe_inaktivitaet():
    try:
        cursor = mysql.connection.cursor()

        # 📥 Einstellungen abrufen
        cursor.execute("SELECT intervall_stunden, max_inaktiv_tage, email_empfaenger, letzte_warnung_am FROM einstellungen WHERE id = 1")
        daten = cursor.fetchone()

        if not daten:
            print("❌ Einstellungen nicht gefunden.")
            return

        intervall_stunden, max_tage, empfaenger, letzte_warnung_am = daten

        # 🕒 Zeitpunkt der letzten Aktivierung holen
        cursor.execute("SELECT zeitpunkt FROM logeintraege WHERE meldung = 'Schalter aktiviert' ORDER BY zeitpunkt DESC LIMIT 1")
        eintrag = cursor.fetchone()
        letzter_schalter = eintrag[0] if eintrag else None

        jetzt = datetime.now()
        intervall_grenze = jetzt - timedelta(hours=intervall_stunden)
        max_grenze = jetzt - timedelta(days=max_tage)

        warnung_noetig = False

        if not letzter_schalter:
            warnung_noetig = True
        elif letzter_schalter < intervall_grenze:
            warnung_noetig = True

        # 🕒 Schon eine Warnung verschickt?
        warnung_schon_verschickt = letzte_warnung_am and letzte_warnung_am > intervall_grenze

        if warnung_noetig and not warnung_schon_verschickt:
            print("⚠️ Inaktivität erkannt. Versende Warnmail …")

            sende_email(
                template_name="mail_warnung.html",
                empfaenger=empfaenger,
                daten={
                    "nachricht": f"Der Totmann-Schalter wurde seit dem {letzter_schalter.strftime('%d.%m.%Y %H:%M') if letzter_schalter else 'noch nie'} nicht betätigt.",
                    "intervall_stunden": intervall_stunden,
                    "timestamp": jetzt.strftime("%d.%m.%Y %H:%M"),
                    "absender": "webmaster@pixelpriest.de",
                    "betreff": "⚠️ Totmann-Schalter: Inaktivitätswarnung"
                }
            )

            # 📝 Warnzeitpunkt aktualisieren
            cursor.execute("UPDATE einstellungen SET letzte_warnung_am = %s WHERE id = 1", (jetzt,))
            mysql.connection.commit()
        else:
            print("✅ Keine Warnung notwendig.")

        cursor.close()
    except Exception as e:
        print(f"Fehler bei Inaktivitätsprüfung: {e}")