@echo off
echo ========================================
echo   Game AI Petualangan - Web Edition
echo ========================================
echo.

echo Installing dependencies...
pip install flask flask-socketio

echo.
echo Starting web application...
echo Web app akan berjalan di: http://localhost:5000
echo Buka browser dan kunjungi URL di atas!
echo.
echo Tekan Ctrl+C untuk menghentikan server
echo.

python run_web.py

pause 