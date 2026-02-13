@echo off
echo ========================================
echo 如说修行网上佛学院 - 重新设计版预览
echo ========================================
echo.
echo 正在启动本地服务器...
echo.
echo 请在浏览器中访问:
echo http://localhost:8000/index-redesign.html
echo.
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

python -m http.server 8000
