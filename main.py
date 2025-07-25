# main.py – Kniffel-Spiel

from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from utils import init_utils
import os

# 🔧 .env laden
#load_dotenv()
load_dotenv(dotenv_path=".env")

# 🔧 Flask-App initialisieren
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'BRATWURST')
app.config["DEBUG"] = os.getenv('DEBUG_MODE', 'false').lower() == "true"
app.config["TEMPLATES_AUTO_RELOAD"] = True

# 🔌 MySQL-Konfiguration
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

# 🧠 MySQL initialisieren (aus utils importiert)
mysql = MySQL(app)

# 💡 mysql an utils übergeben
init_utils(mysql)

# 📦 Eigene Module
from blueprints.auth import auth
from blueprints.core import core
from blueprints.admin import admin
from blueprints.spiel import game

# 🔗 Blueprints registrieren
app.register_blueprint(auth)
app.register_blueprint(core)
app.register_blueprint(admin)
app.register_blueprint(game)

# 🚀 Anwendung starten
if __name__ == "__main__":
    app.run()