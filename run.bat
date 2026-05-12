@echo off
if not exist venv\Scripts\activate.bat (
    echo Virtual environment not found! Please run setup.bat first.
    pause
    exit /b
)

call venv\Scripts\activate.bat
start "OCR Guesser" /min python guesser.py
