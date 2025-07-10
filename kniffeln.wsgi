# /pokern/www/KniffelGame/kniffel.wsgi
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from main import app as application