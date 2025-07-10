# utils.py
import traceback
import os

from flask import session, redirect, url_for, render_template
from functools import wraps
from datetime import datetime

mysql = None # wird durch init_utils gesetzt

def init_utils(mysql_instance):
    global mysql
    mysql = mysql_instance

def now_str(fmt="%d.%m.%Y %H:%M"):
    return datetime.now().strftime(fmt)

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM benutzer WHERE id = %s", (session["user_id"],))
            daten = cursor.fetchone()
            if not daten:
                session.clear()
                return redirect(url_for("auth.login"))
            benutzer = dict(zip([d[0] for d in cursor.description], daten))
            cursor.close()
            return func(benutzer, *args, **kwargs)  # Übergibt benutzer als erstes Argument
        except Exception as e:
            traceback_str = traceback.format_exc() # 🔍 kompletter Traceback als String
            fehlermeldung = f"Fehler bei Benutzerprüfung: {e}"
            debug_output = f"<pre>{traceback_str}</pre>" if os.getenv("DEBUG_MODE", "false").lower() == "true" else ""
            return render_template("fehler.html", fehlermeldung=fehlermeldung + debug_output)
    return wrapper

def admin_required(func):
    @wraps(func)
    @login_required
    def wrapper(user, *args, **kwargs):
        if not user.get("ist_admin"):
            return render_template("fehler.html", fehlermeldung="Zugriff verweigert: Keine Adminrechte."), 403
        return func(user=user, *args, **kwargs)

    return wrapper

def paginate(query, page, per_page, cursor, count_query=None):
    """
    Führt eine paginierte SQL-Abfrage aus.

    :param query: SQL-SELECT-Query mit LIMIT/OFFSET-Platzhaltern
    :param page: aktuelle Seite (int)
    :param per_page: Einträge pro Seite (int)
    :param cursor: aktiver MySQL-Cursor
    :param count_query: optional: separate Query zur Ermittlung der Gesamtanzahl
    :return: (daten_liste, seitenanzahl)
    """
    offset = (page - 1) * per_page

    cursor.execute(query, (per_page, offset))
    daten_liste = cursor.fetchall()

    if count_query:
        cursor.execute(count_query)
        total = cursor.fetchone()[0]
    else:
        # Versuche eine Zählung aus dem ursprünglichen Query (nicht optimal bei komplexen Joins)
        cursor.execute("SELECT FOUND_ROWS()")
        total = cursor.fetchone()[0]

    seitenanzahl = (total + per_page - 1) // per_page
    return daten_liste, seitenanzahl