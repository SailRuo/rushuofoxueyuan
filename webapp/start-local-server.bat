@echo off
echo ========================================
echo   如说修行网上佛学院 - 本地服务器
echo ========================================
echo.
echo 正在启动服务器...
echo.
echo 请在浏览器中访问:
echo   http://localhost:8000/webapp/
echo.
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.
cd /d "%~dp0\.."
python -m http.server 8000
pause
