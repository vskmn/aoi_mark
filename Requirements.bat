@echo off
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install streamlit pillow
deactivate
pause