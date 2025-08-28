@echo off

echo Setting build environment...
python -m venv .venv

echo Intializing build environment...
call .venv\Scripts\activate.bat

echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r dependencies.txt

echo.
echo Build environment setup complete.
pause
