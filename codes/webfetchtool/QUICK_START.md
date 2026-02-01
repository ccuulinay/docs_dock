# WebFetch Tool 快速开始指南

## 5分钟快速设置

### 1. 安装依赖（2分钟）

```bash
# 安装 Python 依赖
pip install playwright

# 安装浏览器
playwright install chromium
```

### 2. 验证安装（1分钟）

```bash
# Windows CMD
webfetch.bat https://example.com

# Git Bash
./webfetch.sh https://example.com

# 或者直接使用 Python
python webfetch.py https://example.com
```

### 3. 配置 Copilot（2分钟）

打开 VS Code 设置 (Ctrl+,)，搜索 `github.copilot.chat.instructions`，添加：

```json
{
  "github.copilot.chat.instructions": [
    {
      "text": "获取网页内容时使用: python C:\\\\Tools\\\\webfetch.py \\"<URL>\\" --scroll --pretty。返回JSON，检查success字段，提取title和content。"
    }
  ]
}
```

将 `C:\\Tools\\webfetch.py` 替换为你的实际路径。

## 常用命令速查

| 场景 | 命令 |
|------|------|
| 基本获取 | `python webfetch.py "https://example.com"` |
| 完整内容 | `python webfetch.py "https://example.com" --scroll --pretty` |
| 使用代理 | `python webfetch.py "https://example.com" --proxy "http://proxy:8080"` |
| 等待元素 | `python webfetch.py "https://example.com" --wait-for "#content"` |
| 获取HTML | `python webfetch.py "https://example.com" --html` |
| 保存文件 | `python webfetch.py "https://example.com" --output result.json` |

## 环境变量配置

**Windows (CMD):**
```cmd
set HTTP_PROXY=http://proxy.company.com:8080
set HTTPS_PROXY=http://proxy.company.com:8080
```

**Git Bash:**
```bash
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| `ModuleNotFoundError` | `pip install playwright` |
| 浏览器启动失败 | `playwright install --force chromium` |
| 连接超时 | 添加 `--timeout 60000` |
| 代理错误 | 检查代理配置或联系IT |
| 内容不完整 | 添加 `--scroll` 参数 |

## 测试命令

```bash
# 运行测试套件
python test_webfetch.py
```

## 下一步

1. 阅读完整文档：[README.md](README.md)
2. 配置 Copilot：[VS_CODE_SETUP.md](VS_CODE_SETUP.md)
3. 复制系统提示词：[SYSTEM_PROMPT_SNIPPET.md](SYSTEM_PROMPT_SNIPPET.md)

## 获取帮助

如遇到问题，请检查：
1. Python 版本 >= 3.8
2. Playwright 已正确安装
3. Chromium 浏览器已下载
4. 代理配置正确（如需要）
