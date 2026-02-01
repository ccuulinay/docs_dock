# WebFetch Tool for GitHub Copilot

基于 Playwright 的网页内容获取工具，专为在受限网络环境下使用 GitHub Copilot 设计。

## 功能特性

- ✅ 通过 Playwright 模拟真实浏览器访问
- ✅ 支持 HTTP/HTTPS 代理配置
- ✅ 智能提取页面主要内容（过滤导航、广告等）
- ✅ 支持滚动加载懒加载内容
- ✅ 可等待特定元素加载完成
- ✅ 返回结构化 JSON 数据
- ✅ 同时支持 Windows CMD 和 Git Bash

## 环境要求

- Python 3.8+
- Node.js（Playwright 依赖）
- Windows 10+ 或 Git Bash

## 安装步骤

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 2. 安装 Playwright 浏览器

```bash
playwright install chromium
```

### 3. 验证安装

```bash
# Windows CMD
webfetch.bat https://example.com

# Git Bash
./webfetch.sh https://example.com
```

## 使用方法

### 命令行参数

```
python webfetch.py <URL> [options]

参数:
  url                  要获取的网页URL（必需）
  --proxy, -p          代理服务器地址，如 "http://proxy.company.com:8080"
  --timeout, -t        页面加载超时时间（毫秒，默认30000）
  --wait-for, -w       等待特定CSS选择器出现
  --scroll, -s         滚动页面以加载懒加载内容
  --html               返回HTML源码而非纯文本
  --output, -o         输出文件路径（默认输出到stdout）
  --pretty             美化JSON输出
```

### 使用示例

```bash
# 基本使用
python webfetch.py https://example.com

# 使用代理（推荐用于公司环境）
python webfetch.py https://example.com --proxy "http://proxy.company.com:8080"

# 或者设置环境变量
set HTTP_PROXY=http://proxy.company.com:8080
python webfetch.py https://example.com

# 等待特定元素加载
python webfetch.py https://example.com --wait-for "#main-content"

# 滚动页面加载更多内容
python webfetch.py https://example.com --scroll

# 获取HTML源码
python webfetch.py https://example.com --html --pretty

# 保存到文件
python webfetch.py https://example.com --output result.json --pretty
```

### 返回格式

```json
{
  "url": "https://example.com",
  "success": true,
  "title": "Example Domain",
  "content": "页面正文内容...",
  "error": null,
  "metadata": {
    "status": 200,
    "content_type": "text/html; charset=UTF-8",
    "description": "页面描述..."
  }
}
```

## 配置代理（公司环境）

### 方法一：命令行参数

```bash
python webfetch.py https://example.com --proxy "http://proxy.company.com:8080"
```

### 方法二：环境变量

**Windows CMD:**
```cmd
set HTTP_PROXY=http://proxy.company.com:8080
set HTTPS_PROXY=http://proxy.company.com:8080
```

**Git Bash:**
```bash
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
```

### 方法三：永久配置（推荐）

**Windows 系统环境变量:**
1. 打开"系统属性" → "环境变量"
2. 添加用户变量:
   - `HTTP_PROXY`: `http://proxy.company.com:8080`
   - `HTTPS_PROXY`: `http://proxy.company.com:8080`

## 系统提示词配置

将以下内容添加到你的 GitHub Copilot 系统提示词中：

```markdown
## WebFetch Tool 使用指南

当需要访问网页获取信息时，使用 WebFetch Tool 代替内置的 webfetch/websearch 功能。

### 工具位置
- Windows CMD: `webfetch.bat`
- Git Bash: `./webfetch.sh`
- Python: `python webfetch.py`

### 使用场景
- 需要获取网页内容进行分析时
- 内置 webfetch 功能无法正常工作时
- 需要获取动态加载的网页内容时

### 调用格式

**基本调用:**
```
python webfetch.py <URL>
```

**带代理的调用（公司环境）:**
```
python webfetch.py <URL> --proxy "http://proxy.company.com:8080"
```

**获取完整内容:**
```
python webfetch.py <URL> --scroll --pretty
```

### 处理返回结果

工具返回 JSON 格式数据：
- `success`: 是否成功获取
- `title`: 页面标题
- `content`: 页面正文内容
- `error`: 错误信息（如果有）
- `metadata`: 包含状态码等元信息

### 示例工作流

用户: "请帮我查看 https://example.com 的内容"

助手操作:
1. 调用: `python webfetch.py https://example.com --pretty`
2. 解析返回的 JSON
3. 向用户呈现 `title` 和 `content` 的内容

### 注意事项

1. 始终检查 `success` 字段确认获取成功
2. 如有错误，查看 `error` 字段获取详细信息
3. 对于长页面，使用 `--scroll` 参数获取完整内容
4. 在公司网络环境下，确保配置了正确的代理
```

## 故障排除

### 问题: `playwright` 模块未找到

**解决:**
```bash
pip install playwright
playwright install chromium
```

### 问题: 浏览器启动失败

**解决:**
```bash
# 重新安装浏览器
playwright install --force chromium
```

### 问题: 连接超时

**解决:**
- 检查代理配置是否正确
- 增加超时时间: `--timeout 60000`

### 问题: 获取的内容不完整

**解决:**
- 使用 `--scroll` 参数滚动页面
- 使用 `--wait-for` 等待特定元素加载

## 文件说明

```
webfetch_tool/
├── webfetch.py          # 主程序（Python）
├── webfetch.bat         # Windows CMD 包装脚本
├── webfetch.sh          # Git Bash 包装脚本
├── requirements.txt     # Python 依赖
└── README.md           # 本文档
```

## 许可证

MIT License - 公司内部自由使用
