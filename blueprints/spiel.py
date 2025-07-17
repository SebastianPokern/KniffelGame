# blueprints/spiel.py
from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, current_app, jsonify, session
)
from utils import login_required, mysql
from spiel_logik import (
    berechne_augen, berechne_dreierpasch, berechne_viererpasch,
    berechne_full_house, berechne_kleine_strasse,
    berechne_grosse_strasse, berechne_kniffel, berechne_chance,
    berechne_punkte
)
# import bcrypt
from werkzeug.security import generate_password_hash
import random
import string
from datetime import datetime
import MySQLdb.cursors

game = Blueprint("spiel", __name__)

# 🏠 Spielbrett
@game.route("/spiel/<int:spiel_id>", strict_slashes=False)
@login_required
def spielbrett(user, spiel_id):
    session["spiel_id"] = spiel_id
    print("Aktuelle Session:", session)

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Teilnehmer, Benutzerdaten + aktuelle Punkte aus spielzuege holen
    cursor.execute("""
        SELECT 
            b.benutzername,
            st.ist_aktiv,
            st.benutzer_id,
            st.id AS teilnehmer_id,
            COALESCE(SUM(sz.punkte), 0) AS punkte
        FROM spielteilnehmer st
        JOIN benutzer b ON st.benutzer_id = b.id
        LEFT JOIN spielzuege sz ON sz.teilnehmer_id = st.id AND sz.gewertet = 1
        WHERE st.spiel_id = %s
        GROUP BY st.id
    """, (spiel_id,))
    spieler = cursor.fetchall()

    aktiver_benutzer = next((s["benutzer_id"] for s in spieler if s["ist_aktiv"]), None)

    return render_template("spiel.html",
                           spiel_id=spiel_id,
                           spieler=spieler,
                           aktiver_benutzer=aktiver_benutzer)

# Spielende-Anzeige
@game.route("/spiel/<int:spiel_id>/gewinner", strict_slashes=False)
@login_required
def gewinner_anzeige(user, spiel_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT b.benutzername, st.punkte
        FROM spielteilnehmer st
        JOIN benutzer b ON b.id = st.benutzer_id
        WHERE st.spiel_id = %s
        ORDER BY st.punkte DESC
    """, (spiel_id,))
    spieler = cursor.fetchall()
    gewinner = spieler[0] if spieler else None
    return render_template("gewinner.html", spieler=spieler, gewinner=gewinner)

# 🎮 Neues Spiel starten
@game.route("/neues-spiel", methods=["GET", "POST"])
@login_required
def neues_spiel(user):
    cursor = mysql.connection.cursor()

    # Max. Mitspieler aus den Einstellungen lesen
    cursor.execute("SELECT max_mitspieler FROM einstellungen LIMIT 1")
    result = cursor.fetchone()
    max_mitspieler = result[0] if result else 3

    if request.method == "POST":
        spielernamen = request.form.getlist("spieler[]")
        if not spielernamen:
            flash("Mindestens ein Spieler muss ausgewählt werden.", "warning")
            return redirect(url_for("spiel.neues_spiel"))

        # Spielpartie erstellen mit Teilnehmern
        spiel_id = erstelle_spielpartie(spielernamen, cursor)
        mysql.connection.commit()
        return redirect(url_for("spiel.spielbrett", spiel_id=spiel_id))

    # bekannte Benutzer aus DB
    cursor.execute("SELECT benutzername FROM benutzer ORDER BY benutzername")
    bekannte_spieler = [row[0] for row in cursor.fetchall()]

    return render_template("neues_spiel.html", bekannte_spieler=bekannte_spieler, max_mitspieler=max_mitspieler)

def erstelle_spielpartie(spielernamen, cursor):
    """
    Erstellt eine neue Spielpartie, legt neue Benutzer ggf. an und
    verknüpft alle Teilnehmer.
    """
    benutzer_ids = []

    for name in spielernamen:
        cursor.execute("SELECT id FROM benutzer WHERE benutzername = %s", (name,))
        result = cursor.fetchone()

        if result:
            benutzer_ids.append(result[0])
        else:
            # 🔐 Neuen Benutzer erstellen mit Zufallspasswort
            random_pw = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

            if current_app.config.get("DEBUG", False):
                pw_hash = random_pw  # Kein Hash im DEBUG-Modus
            else:
                #pw_hash = bcrypt.hashpw(random_pw.encode(), bcrypt.gensalt()).decode()
                pw_hash = generate_password_hash(random_pw)

            cursor.execute(
                "INSERT INTO benutzer (benutzername, passwort_hash, ist_aktiv, erstellt_am) VALUES (%s, %s, 1, NOW())",
                (name, pw_hash)
            )
            benutzer_ids.append(cursor.lastrowid)

    # 🆕 Spielpartie anlegen
    cursor.execute("INSERT INTO spielpartien (startzeit, beendet) VALUES (NOW(), 0)")
    spiel_id = cursor.lastrowid

    # 👥 Teilnehmer verknüpfen
    for benutzer_id in benutzer_ids:
        cursor.execute(
            "INSERT INTO spielteilnehmer (spiel_id, benutzer_id, punkte) VALUES (%s, %s, 0)",
            (spiel_id, benutzer_id)
        )

    cursor.execute("""
            UPDATE spielteilnehmer
            SET ist_aktiv = 1
            WHERE spiel_id = %s
            ORDER BY id
            LIMIT 1
        """, (spiel_id,))

    return spiel_id

# Neue Route für AJAX-Anfrage zur Punkteberechnung
@game.route("/ajax/punkte-berechnung", methods=["POST"])
@login_required
def ajax_punkte_berechnung(user):
    try:
        daten = request.get_json()
        wuerfel = daten.get("wuerfel", [])  # Liste z.B. [2,2,2,5,6]

        if not wuerfel or len(wuerfel) != 5:
            return jsonify({"fehler": "Ungültiger Wurf"}), 400

        # Berechnungen durchführen
        punkte = {
            "Einsen": berechne_augen(wuerfel, 1),
            "Zweien": berechne_augen(wuerfel, 2),
            "Dreien": berechne_augen(wuerfel, 3),
            "Vieren": berechne_augen(wuerfel, 4),
            "Fünfen": berechne_augen(wuerfel, 5),
            "Sechsen": berechne_augen(wuerfel, 6),
            "Dreierpasch": berechne_dreierpasch(wuerfel),
            "Viererpasch": berechne_viererpasch(wuerfel),
            "Full House": berechne_full_house(wuerfel),
            "Kleine Straße": berechne_kleine_strasse(wuerfel),
            "Große Straße": berechne_grosse_strasse(wuerfel),
            "Kniffel": berechne_kniffel(wuerfel),
            "Chance": berechne_chance(wuerfel)
        }

        return jsonify(punkte)

    except Exception as e:
        return jsonify({"fehler": str(e)}), 500

# Route zum Speichern eines Spielzugs
@game.route("/ajax/zug-speichern", methods=["POST"])
@login_required
def ajax_zug_speichern(user):
    try:
        daten = request.get_json()
        kategorie = daten.get("kategorie")
        punkte = daten.get("punkte")
        wuerfel = daten.get("wuerfel")

        if not kategorie or punkte is None or not isinstance(wuerfel, list) or len(wuerfel) != 5:
            return jsonify({"status": "fehler", "msg": "Ungültige Daten"}), 400

        spiel_id = session.get("spiel_id")
        if not spiel_id:
            return jsonify({"status": "fehler", "msg": "Kein aktives Spiel"}), 400

        # Teilnehmer-ID holen
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT id, benutzer_id 
            FROM spielteilnehmer
            WHERE spiel_id = %s AND ist_aktiv = 1
        """, (spiel_id,))
        teilnehmer = cursor.fetchone()
        if not teilnehmer:
            return jsonify({"status": "fehler", "msg": "Teilnehmer nicht gefunden"}), 404

        teilnehmer_id = teilnehmer["id"]

        # Zählung bisheriger Züge für diesen Teilnehmer = Rundenfortschritt
        cursor.execute("""
            SELECT COUNT(*) AS anzahl
            FROM spielzuege
            WHERE teilnehmer_id = %s AND gewertet = 1
        """, (teilnehmer_id,))
        row = cursor.fetchone()
        # bei DictCursor ist row ein dict, bei normalem Cursor ein tuple
        if isinstance(row, dict):
            # nimm das erste (und einzige) Value im Dict:
            anzahl_runden = list(row.values())[0]
        else:
            # tuple‑Fallback (z.B. wenn doch kein DictCursor aktiv)
            anzahl_runden = row[0]
        aktuelle_runde = anzahl_runden + 1

        # Einfügen des neuen Zugs
        cursor.execute("""
            INSERT INTO spielzuege (teilnehmer_id, wurf_nummer, wuerfelwerte, gewertet, punktekategorie, punkte)
            VALUES (%s, %s, %s, 1, %s, %s)
        """, (
            teilnehmer_id,
            3,  # Wir gehen davon aus, dass der dritte Wurf gemacht wurde
            ",".join(str(w) for w in wuerfel),
            kategorie,
            punkte
        ))
        mysql.connection.commit()

        # Punkte aktualisieren
        cursor.execute("""
            UPDATE spielteilnehmer
            SET punkte = punkte + %s
            WHERE id = %s
        """, (punkte, teilnehmer_id))

        # Aktiven Spieler deaktivieren
        cursor.execute("""
            UPDATE spielteilnehmer
            SET ist_aktiv = 0
            WHERE spiel_id = %s
        """, (spiel_id,))

        # Nächsten Spieler aktivieren (runde-rotiert)
        cursor.execute("""
            SELECT id FROM spielteilnehmer
            WHERE spiel_id = %s
            ORDER BY id
        """, (spiel_id,))
        alle_ids = [row["id"] for row in cursor.fetchall()]
        index = alle_ids.index(teilnehmer_id)
        naechster_id = alle_ids[(index + 1) % len(alle_ids)]

        cursor.execute("""
            UPDATE spielteilnehmer
            SET ist_aktiv = 1
            WHERE id = %s
        """, (naechster_id,))

        # Prüfen ob alle 13 Kategorien vergeben sind pro Spieler
        cursor.execute("""
            SELECT COUNT(*) AS anzahl
            FROM spielzuege
            WHERE teilnehmer_id = %s AND gewertet = 1
        """, (teilnehmer_id,))
        row = cursor.fetchone()
        if isinstance(row, dict):
            anzahl_runden = list(row.values())[0]
        else:
            anzahl_runden = row[0]

        spiel_beendet = False
        if anzahl_runden >= 13:
            # Prüfen ob *alle* Spieler 13 Runden gespielt haben
            cursor.execute("""
                SELECT COUNT(*) AS offenes
                FROM spielteilnehmer t
                LEFT JOIN (
                    SELECT teilnehmer_id, COUNT(*) AS zuege
                    FROM spielzuege
                    WHERE gewertet = 1
                    GROUP BY teilnehmer_id
                ) z ON z.teilnehmer_id = t.id
                WHERE t.spiel_id = %s AND (z.zuege IS NULL OR z.zuege < 13)
            """, (spiel_id,))
            offenes = cursor.fetchone()["offenes"]
            if offenes == 0:
                spiel_beendet = True
                # Redirect auf Spielende-Seite
                return jsonify({"status": "fertig", "redirect": url_for("spiel.gewinner_anzeige", spiel_id=spiel_id)})

        mysql.connection.commit()

        cursor.execute("""
                SELECT st.benutzer_id, st.id AS teilnehmer_id, st.ist_aktiv
                FROM spielteilnehmer st
                WHERE st.spiel_id = %s
            """, (spiel_id,))
        teilnehmer_daten = cursor.fetchall()

        # Für jeden Teilnehmer die aktuellen Punkte summieren
        spieler_liste = []
        for t in teilnehmer_daten:
            cursor.execute("""
                    SELECT COALESCE(SUM(punkte),0) AS summe
                    FROM spielzuege
                    WHERE teilnehmer_id = %s AND gewertet = 1
                """, (t["teilnehmer_id"],))
            punkte = cursor.fetchone()["summe"]
            spieler_liste.append({
                "benutzer_id": t["benutzer_id"],
                "teilnehmer_id": t["teilnehmer_id"],
                "ist_aktiv": bool(t["ist_aktiv"]),
                "punkte": punkte
            })

        # JSON‑Antwort zusammenbauen
        return jsonify({
            "status": "ok",
            "next_player": naechster_id,
            "spieler": spieler_liste
        })

    except Exception as e:
        current_app.logger.error(f"Fehler beim Speichern des Zuges: {e}")
        return jsonify({"status": "fehler", "msg": "Interner Fehler"}), 500