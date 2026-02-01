#!/bin/bash
# WebFetch Tool 安装脚本 (Git Bash / Linux / macOS)

set -e

echo "========================================"
echo "WebFetch Tool 安装程序"
echo "========================================"
echo

# 检查 Python
if ! command -v python &> /dev/null; then
    echo "[错误] 未检测到 Python，请先安装 Python 3.8+"
    exit 1
fi
echo "[OK] Python 已安装: $(python --version)"

# 安装依赖
echo
echo "正在安装 Python 依赖..."
pip install -r requirements.txt
echo "[OK] 依赖安装完成"

# 安装 Playwright 浏览器
echo
echo "正在安装 Playwright Chromium 浏览器..."
playwright install chromium
echo "[OK] 浏览器安装完成"

# 添加执行权限
echo
echo "添加执行权限..."
chmod +x webfetch.sh
echo "[OK] 权限设置完成"

# 运行测试
echo
echo "正在运行测试..."
if python test_webfetch.py; then
    echo
    echo "[OK] 所有测试通过"
else
    echo
    echo "[警告] 测试未完全通过，但基本功能可能可用"
fi

echo
echo "========================================"
echo "安装完成！"
echo "========================================"
echo
echo "使用方法:"
echo "  ./webfetch.sh https://example.com"
echo "  python webfetch.py https://example.com"
echo
echo "查看 QUICK_START.md 获取更多信息"
