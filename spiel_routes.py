# File: spiel_routes.py
from flask import Blueprint, render_template
from utils import login_required

spiel = Blueprint("spiel", __name__)

# 👤 Kniffel-Spiel: Hauptseite
@spiel.route("/spiel", strict_slashes=False)
@login_required
def spiel():
    return render_template("spiel.html")