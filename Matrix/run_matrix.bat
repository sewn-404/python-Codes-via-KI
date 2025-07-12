@echo off
set python_script=Matrix.py

if exist %python_script% (
    echo Python-Skript existiert bereits.
    python %python_script% -WindowStyle minimized
) else (
    echo Python-Skript wird erstellt...
    python generate_matrix.py
    echo Python-Skript erstellt.
    python %python_script% -WindowStyle minimized
)
pause