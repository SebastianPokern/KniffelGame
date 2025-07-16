# blueprints/spiel.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify, session
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

import MySQLdb.cursors

game = Blueprint("spiel", __name__)

# 🏠 Spielbrett
@game.route("/spiel/<int:spiel_id>", strict_slashes=False)
@login_required
def spielbrett(user, spiel_id):

    session["spiel_id"] = spiel_id

    print("Aktuelle Session:", session)

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Teilnehmer + Benutzerdaten holen
    cursor.execute("""
            SELECT b.benutzername, st.punkte
            FROM spielteilnehmer st
            JOIN benutzer b ON st.benutzer_id = b.id
            WHERE st.spiel_id = %s
        """, (spiel_id,))
    spieler = cursor.fetchall()

    return render_template("spiel.html", spiel_id=spiel_id, spieler=spieler)

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
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT id FROM spielteilnehmer
            WHERE benutzer_id = %s AND spiel_id = %s
        """, (user["id"], spiel_id))
        teilnehmer = cursor.fetchone()
        if not teilnehmer:
            return jsonify({"status": "fehler", "msg": "Teilnehmer nicht gefunden"}), 404

        teilnehmer_id = teilnehmer[0]

        # Zählung bisheriger Züge für diesen Teilnehmer = Rundenfortschritt
        cursor.execute("""
            SELECT COUNT(*) FROM spielzuege
            WHERE teilnehmer_id = %s AND gewertet = 1
        """, (teilnehmer_id,))
        anzahl_runden = cursor.fetchone()[0]
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

        return jsonify({"status": "ok"})

    except Exception as e:
        current_app.logger.error(f"Fehler beim Speichern des Zuges: {e}")
        return jsonify({"status": "fehler", "msg": "Interner Fehler"}), 500