# spiel_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils import login_required, mysql

game = Blueprint("spiel", __name__)

# 🏠 Spielbrett
@game.route("/spiel/<int:spiel_id>", strict_slashes=False)
@login_required
def spielbrett(user, spiel_id):
    return render_template("spiel.html", spiel_id=spiel_id)

# 🎮 Neues Spiel starten
@game.route("/neues-spiel", methods=["GET", "POST"])
@login_required
def neues_spiel(user):
    cursor = mysql.connection.cursor()

    # max_mitspieler aus der Tabelle einstellungen
    cursor.execute("SELECT max_mitspieler FROM einstellungen LIMIT 1")
    result = cursor.fetchone()
    max_mitspieler = result[0] if result else 3

    if request.method == "POST":
        mitspieler = request.form.getlist("spieler[]")
        if not mitspieler:
            flash("Mindestens ein Spieler muss ausgewählt werden.", "warning")
            return redirect(url_for("spiel.neues_spiel"))

        # Spiel starten (z. B. in Funktion auslagern)
        spiel_id = erstelle_spielpartie(mitspieler)
        return redirect(url_for("spiel.spielbrett", spiel_id=spiel_id))

    # bekannte Spieler aus DB
    cursor.execute("SELECT benutzername FROM benutzer ORDER BY benutzername")
    bekannte_spieler = [row[0] for row in cursor.fetchall()]

    return render_template("neues_spiel.html", bekannte_spieler=bekannte_spieler, max_mitspieler=max_mitspieler)

def erstelle_spielpartie(spieler_ids, cursor):
    """
    Legt eine neue Spielpartie an und verknüpft alle Spieler.
    Gibt die neue Spiel-ID zurück.
    """

    # Spielpartie anlegen
    cursor.execute("INSERT INTO spielpartien (startzeit, beendet) VALUES (NOW(), 0)")
    spiel_id = cursor.lastrowid

    # Teilnehmer hinzufügen mit Start-Punkten 0
    for spieler_id in spieler_ids:
        cursor.execute(
            "INSERT INTO spielteilnehmer (spiel_id, benutzer_id, punkte) VALUES (%s, %s, 0)",
            (spiel_id, spieler_id)
        )

    return spiel_id