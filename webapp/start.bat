@echo off
echo ====================================
echo   如说修行 - 本地开发服务器
echo ====================================
echo.
echo 正在启动服务器...
echo 访问地址: http://localhost:8000
echo 按 Ctrl+C 停止服务器
echo.
python -m http.server 8000
