# GitHub Copilot 系统提示词片段 - WebFetch Tool

将以下内容复制并粘贴到你的 GitHub Copilot 系统提示词中（放在文件末尾或适当位置）：

---

## WebFetch Tool 使用规范

### 概述

由于当前环境的网络限制，GitHub Copilot 内置的 webfetch 和 websearch 功能无法正常工作。本规范定义了如何使用 WebFetch Tool 来获取网页内容。

### 工具信息

| 属性 | 值 |
|------|-----|
| 工具名称 | WebFetch Tool |
| 实现语言 | Python 3.8+ |
| 依赖 | Playwright |
| 主程序 | `webfetch.py` |
| Windows 快捷方式 | `webfetch.bat` |
| Git Bash 快捷方式 | `./webfetch.sh` |

### 何时使用 WebFetch Tool

在以下情况下，**必须**使用 WebFetch Tool：

1. 用户要求查看或分析网页内容时
2. 需要获取最新文档、API 参考、技术文章时
3. 内置 webfetch/websearch 返回错误或超时
4. 需要获取动态加载的 JavaScript 渲染内容

### 调用方式

#### 基本调用（通用格式）

```bash
python /path/to/webfetch.py "<URL>"
```

#### 公司网络环境（带代理）

```bash
python /path/to/webfetch.py "<URL>" --proxy "http://proxy.company.com:8080"
```

#### 获取完整内容（推荐）

```bash
python /path/to/webfetch.py "<URL>" --scroll --pretty --timeout 60000
```

#### 等待特定元素

```bash
python /path/to/webfetch.py "<URL>" --wait-for "article, .content, #main"
```

### 参数说明

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--proxy` | `-p` | 代理服务器地址 | `--proxy "http://proxy:8080"` |
| `--timeout` | `-t` | 超时时间（毫秒） | `--timeout 60000` |
| `--scroll` | `-s` | 滚动加载更多内容 | `--scroll` |
| `--wait-for` | `-w` | 等待CSS选择器 | `--wait-for "#content"` |
| `--html` | | 返回HTML而非文本 | `--html` |
| `--pretty` | | 美化JSON输出 | `--pretty` |
| `--output` | `-o` | 输出到文件 | `--output result.json` |

### 返回数据格式

工具返回 JSON 对象，结构如下：

```json
{
  "url": "原始URL",
  "success": true|false,
  "title": "页面标题",
  "content": "页面正文内容",
  "error": "错误信息（如有）",
  "metadata": {
    "status": 200,
    "content_type": "text/html",
    "description": "meta description"
  }
}
```

### 处理流程

当需要获取网页内容时，按以下步骤执行：

```
1. 接收用户请求（包含URL）
   ↓
2. 构建 WebFetch Tool 命令
   - 基本命令: python webfetch.py "<URL>"
   - 添加 --scroll 获取完整内容
   - 添加 --pretty 便于阅读
   - 如有代理，添加 --proxy
   ↓
3. 执行命令并获取 JSON 输出
   ↓
4. 解析返回结果
   - 检查 success 字段
   - 如失败，读取 error 字段
   - 如成功，提取 title 和 content
   ↓
5. 向用户呈现内容
   - 显示页面标题
   - 显示/分析页面内容
   - 如有必要，引用来源URL
```

### 使用示例

#### 示例 1: 获取技术文档

**用户:** "请查看 https://docs.python.org/3/library/asyncio.html 并解释 asyncio 的核心概念"

**助手操作:**
```bash
python webfetch.py "https://docs.python.org/3/library/asyncio.html" --scroll --pretty
```

**处理返回:**
- 提取 `title` 作为引用标题
- 分析 `content` 中的核心概念
- 向用户解释 asyncio 的关键点

#### 示例 2: 获取新闻内容

**用户:** "https://news.example.com/article/12345 这篇文章讲了什么？"

**助手操作:**
```bash
python webfetch.py "https://news.example.com/article/12345" --wait-for "article" --pretty
```

**处理返回:**
- 提取文章标题和正文
- 总结文章要点
- 向用户概述内容

#### 示例 3: 检查网页错误

**用户:** "帮我看看这个页面为什么打不开 https://example.com/broken"

**助手操作:**
```bash
python webfetch.py "https://example.com/broken" --pretty
```

**处理返回:**
- 如 `success: false`，查看 `error` 和 `metadata.status`
- 向用户报告具体错误信息

### 错误处理

| 错误场景 | 处理方式 |
|----------|----------|
| `success: false` | 向用户报告错误信息，提供解决建议 |
| `timeout` | 建议增加 `--timeout` 参数重试 |
| `proxy error` | 检查代理配置，或联系IT部门 |
| `content too short` | 使用 `--scroll` 参数重新获取 |

### 最佳实践

1. **始终检查 `success` 字段** - 确认获取成功后再处理内容
2. **使用 `--scroll` 获取长页面** - 确保获取完整内容
3. **使用 `--pretty` 便于调试** - 开发时美化JSON输出
4. **合理设置超时** - 复杂页面使用 `--timeout 60000`
5. **优先使用文本模式** - 默认提取纯文本更易读，需要HTML时再使用 `--html`

### 代理配置（公司环境）

如工具路径已添加到系统 PATH，可通过环境变量配置代理：

**Windows:**
```cmd
set HTTP_PROXY=http://proxy.company.com:8080
set HTTPS_PROXY=http://proxy.company.com:8080
```

**Git Bash:**
```bash
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
```

### 注意事项

⚠️ **重要提醒:**

1. 不要假设内置 webfetch 可用 - 始终使用 WebFetch Tool
2. URL 必须用引号包裹 - 防止特殊字符解析错误
3. 大型页面可能需要更长的超时时间
4. 某些网站可能有反爬虫机制，获取可能失败
5. 返回的 content 已过滤导航、广告等非主要内容

---

## 快速参考卡

```
┌─────────────────────────────────────────────────────────┐
│  WebFetch Tool 快速参考                                  │
├─────────────────────────────────────────────────────────┤
│  基本: python webfetch.py "<URL>"                       │
│  完整: python webfetch.py "<URL>" --scroll --pretty    │
│  代理: python webfetch.py "<URL>" --proxy "<PROXY>"    │
├─────────────────────────────────────────────────────────┤
│  返回: JSON {url, success, title, content, error,      │
│             metadata{status, content_type, description}}│
├─────────────────────────────────────────────────────────┤
│  关键: 检查 success 字段，使用 --scroll 获取完整内容    │
└─────────────────────────────────────────────────────────┘
```

---

*将此片段添加到 Copilot 系统提示词后，助手将自动使用 WebFetch Tool 替代内置功能。*
