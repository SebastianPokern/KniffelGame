# spiel_routes.py
from flask import Blueprint, render_template, url_for
from utils import login_required

game = Blueprint("spiel", __name__)

# 🏠 Spielbrett
@game.route("/spiel", strict_slashes=False)
@login_required
def spielbrett(user):
    return render_template("spiel.html"), 500