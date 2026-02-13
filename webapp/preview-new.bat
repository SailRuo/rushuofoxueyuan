@echo off
echo ====================================
echo   如说修行 - 新版本预览
echo ====================================
echo.
echo 正在启动服务器...
echo.
echo 访问地址:
echo   新版本: http://localhost:8000/index-new.html
echo   旧版本: http://localhost:8000/index.html
echo   对比页: http://localhost:8000/compare.html
echo.
echo 按 Ctrl+C 停止服务器
echo.
start http://localhost:8000/compare.html
python -m http.server 8000
