@echo off
SETLOCAL

REM --- Name der virtuellen Umgebung
SET VENV_DIR=.venv

REM --- Prüfen ob .venv existiert
IF NOT EXIST %VENV_DIR%\Scripts\activate.bat (
    echo [INFO] Erstelle neue virtuelle Umgebung...
    python -m venv %VENV_DIR%
) ELSE (
    echo [INFO] Virtuelle Umgebung existiert bereits.
)

REM --- Umgebung aktivieren
echo [INFO] Aktiviere virtuelle Umgebung...
CALL %VENV_DIR%\Scripts\activate.bat

REM --- Anforderungen installieren
IF EXIST requirements.txt (
    echo [INFO] Installiere Python-Abhängigkeiten...
    pip install -r requirements.txt
) ELSE (
    echo [WARNUNG] Keine requirements.txt gefunden.
)

REM --- Fertig
echo [FERTIG] Entwicklungsumgebung bereit!
pause