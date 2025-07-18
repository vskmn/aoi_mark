
copy python-embed\python313._pth python-embed\python313.pth
echo import site >> python-embed\python313._pth
python-embed\python.exe -m ensurepip
python-embed\python.exe -m pip install --upgrade pip
python-embed\python.exe -m pip install --target=python-embed\site-packages streamlit pillow
pause
