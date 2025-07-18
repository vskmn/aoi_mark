@echo off
cd /d "%~dp0"
call venv\Scripts\activate
streamlit run AOI_pic.py
pause