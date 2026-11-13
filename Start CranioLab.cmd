@echo off
setlocal
cd /d "%~dp0"

set "CRANIOLAB_PYTHON=%LOCALAPPDATA%\Python\pythoncore-3.14-64\python.exe"
if exist "%CRANIOLAB_PYTHON%" (
    "%CRANIOLAB_PYTHON%" -m streamlit run app.py
) else (
    python -m streamlit run app.py
)

if errorlevel 1 (
    echo.
    echo CranioLab could not start. Check the error above.
    pause
)
