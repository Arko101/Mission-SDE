@echo off
cd /d "%~dp0"
echo.
echo =====================================================
echo   SDE Mission Control - SQLite-backed study tracker

echo =====================================================
echo.
echo Open this address in your browser:
echo http://127.0.0.1:8765
echo.
echo Keep this terminal window open while using the app.
echo Press Ctrl+C to stop. Your progress is saved.
echo.
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 server.py
) else (
  python server.py
)
pause
