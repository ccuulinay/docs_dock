@echo off
REM WebFetch Tool 安装脚本 (Windows)

echo ========================================
echo WebFetch Tool 安装程序
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    exit /b 1
)
echo [OK] Python 已安装

REM 安装依赖
echo.
echo 正在安装 Python 依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] 依赖安装失败
    exit /b 1
)
echo [OK] 依赖安装完成

REM 安装 Playwright 浏览器
echo.
echo 正在安装 Playwright Chromium 浏览器...
playwright install chromium
if errorlevel 1 (
    echo [错误] 浏览器安装失败
    exit /b 1
)
echo [OK] 浏览器安装完成

REM 运行测试
echo.
echo 正在运行测试...
python test_webfetch.py
if errorlevel 1 (
    echo.
    echo [警告] 测试未完全通过，但基本功能可能可用
) else (
    echo.
    echo [OK] 所有测试通过
)

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 使用方法:
echo   webfetch.bat https://example.com
echo   python webfetch.py https://example.com
echo.
echo 查看 QUICK_START.md 获取更多信息
pause
