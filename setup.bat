@echo off 
if not exist venv\Scripts\activate.bat (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists. Skipping creation...
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt 

echo Installation complete. 
pause
