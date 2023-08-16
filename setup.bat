@echo off
echo Installing required packages...
pip install -r requirements.txt

if ERRORLEVEL 1 (
    echo Failed to install required packages. Exiting...
    exit /b 1
)

echo Successfully installed required packages.
echo Running main.pyw...
start pythonw main.pyw

echo Done!
exit
