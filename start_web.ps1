Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Game AI Petualangan - Web Edition" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Installing dependencies..." -ForegroundColor Green
pip install flask flask-socketio

Write-Host ""
Write-Host "Starting web application..." -ForegroundColor Green
Write-Host "Web app akan berjalan di: http://localhost:5000" -ForegroundColor Yellow
Write-Host "Buka browser dan kunjungi URL di atas!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Tekan Ctrl+C untuk menghentikan server" -ForegroundColor Red
Write-Host ""

python run_web.py

Read-Host "Press Enter to exit" 