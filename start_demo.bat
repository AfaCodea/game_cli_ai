@echo off
echo ========================================
echo   Game AI Petualangan - Web Demo
echo ========================================
echo.

echo Installing Flask...
pip install flask

echo.
echo Starting demo web application...
echo Web app akan berjalan di: http://localhost:5000
echo Buka browser dan kunjungi URL di atas!
echo.
echo DEMO MODE - Tidak memerlukan API key
echo Perfect untuk testing interface web!
echo.
echo Tekan Ctrl+C untuk menghentikan server
echo.

python run_demo.py

pause 