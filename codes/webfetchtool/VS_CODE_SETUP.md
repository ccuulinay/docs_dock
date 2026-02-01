# VS Code + GitHub Copilot 配置指南

本文档说明如何在 VS Code 中配置 GitHub Copilot 使用 WebFetch Tool。

## 配置方式

GitHub Copilot 支持通过以下方式配置系统提示词：

### 方式一：Copilot Chat 指令（推荐）

在 VS Code 设置中添加自定义指令：

1. 打开 VS Code 设置 (Ctrl+,)
2. 搜索 `github.copilot.chat.instructions`
3. 点击 "Edit in settings.json"
4. 添加以下配置：

```json
{
  "github.copilot.chat.instructions": [
    {
      "text": "当需要访问网页时，使用 WebFetch Tool。工具路径: C:\\Tools\\webfetch.py。命令格式: python C:\\Tools\\webfetch.py <URL> [--proxy http://proxy:8080] [--scroll] [--pretty]。返回JSON格式，包含url/success/title/content/error/metadata字段。始终检查success字段。"
    }
  ]
}
```

### 方式二：工作区设置

在项目根目录创建 `.vscode/settings.json`：

```json
{
  "github.copilot.chat.instructions": [
    {
      "file": "${workspaceFolder}/.copilot/webfetch-instructions.md"
    }
  ]
}
```

然后创建 `.copilot/webfetch-instructions.md` 文件，将 SYSTEM_PROMPT_SNIPPET.md 的内容复制进去。

### 方式三：用户设置（全局生效）

1. 打开用户设置 JSON (Ctrl+Shift+P → "Preferences: Open User Settings (JSON)")
2. 添加配置：

```json
{
  "github.copilot.chat.instructions": [
    {
      "text": "## WebFetch Tool 使用规范\\n\\n由于网络限制，内置 webfetch 不可用。使用外部工具：python C:/Tools/webfetch.py <URL> [--proxy PROXY] [--scroll] [--pretty]。返回JSON，检查success字段。"
    }
  ]
}
```

## 完整配置示例

### settings.json（用户配置）

```json
{
  // GitHub Copilot 配置
  "github.copilot.enable": {
    "*": true,
    "markdown": true,
    "plaintext": true
  },
  
  // Copilot Chat 指令
  "github.copilot.chat.instructions": [
    {
      "text": "## WebFetch Tool 使用规范\\n\\n当需要获取网页内容时，使用 WebFetch Tool 代替内置功能。\\n\\n### 工具信息\\n- 路径: C:\\\\Tools\\\\webfetch.py\\n- 依赖: Python + Playwright\\n\\n### 命令格式\\n基本: python C:\\\\Tools\\\\webfetch.py \\"<URL>\\"\\n完整: python C:\\\\Tools\\\\webfetch.py \\"<URL>\\" --scroll --pretty\\n代理: python C:\\\\Tools\\\\webfetch.py \\"<URL>\\" --proxy \\"http://proxy:8080\\"\\n\\n### 返回格式\\nJSON对象: {url, success, title, content, error, metadata}\\n\\n### 使用步骤\\n1. 构建命令（URL用引号包裹）\\n2. 执行并获取JSON输出\\n3. 检查success字段\\n4. 提取title和content\\n5. 向用户呈现内容\\n\\n### 注意事项\\n- 始终检查success字段\\n- 长页面使用--scroll\\n- 公司环境配置代理\\n- URL必须用引号包裹"
    }
  ],
  
  // 代理配置（如需要）
  "http.proxy": "http://proxy.company.com:8080",
  "https.proxy": "http://proxy.company.com:8080"
}
```

### 工作区配置

**`.vscode/settings.json`:**

```json
{
  "github.copilot.chat.instructions": [
    {
      "file": "${workspaceFolder}/.copilot/instructions.md"
    }
  ]
}
```

**`.copilot/instructions.md`:**

```markdown
# Copilot 工作区指令

## WebFetch Tool 配置

### 工具路径
- Windows: `C:\Tools\webfetch.py`
- 或相对路径: `./tools/webfetch.py`

### 使用场景
获取网页内容、技术文档、API 参考等。

### 命令模板
```bash
# 基本获取
python C:\Tools\webfetch.py "<URL>"

# 完整内容（推荐）
python C:\Tools\webfetch.py "<URL>" --scroll --pretty --timeout 60000

# 公司网络（带代理）
python C:\Tools\webfetch.py "<URL>" --proxy "http://proxy.company.com:8080" --scroll
```

### 返回数据结构
```json
{
  "url": "原始URL",
  "success": true/false,
  "title": "页面标题",
  "content": "正文内容",
  "error": "错误信息",
  "metadata": {
    "status": 200,
    "content_type": "text/html"
  }
}
```

### 处理流程
1. 用户请求网页内容
2. 构建并执行 WebFetch 命令
3. 解析 JSON 结果
4. 检查 `success` 字段
5. 提取 `title` 和 `content`
6. 向用户呈现分析结果

### 错误处理
- `success: false` → 报告错误，提供解决建议
- `timeout` → 建议增加 `--timeout` 参数
- `proxy error` → 检查代理配置
```

## 环境变量配置

### Windows 系统环境变量

1. 打开"系统属性" → "高级" → "环境变量"
2. 添加以下用户变量：

```
WEBFETCH_PATH=C:\Tools\webfetch.py
HTTP_PROXY=http://proxy.company.com:8080
HTTPS_PROXY=http://proxy.company.com:8080
```

3. 在系统提示词中引用：

```json
{
  "github.copilot.chat.instructions": [
    {
      "text": "WebFetch Tool 路径: ${env:WEBFETCH_PATH}。代理: ${env:HTTP_PROXY}"
    }
  ]
}
```

## 测试配置

配置完成后，在 Copilot Chat 中测试：

```
用户: 请查看 https://example.com 的内容

Copilot 应该:
1. 调用: python C:\Tools\webfetch.py "https://example.com" --pretty
2. 返回页面标题和内容
```

## 故障排除

### Copilot 没有使用 WebFetch Tool

1. 检查指令是否正确添加到 settings.json
2. 重启 VS Code
3. 在 Copilot Chat 中明确提示："请使用 webfetch.py 工具获取..."

### 工具执行失败

1. 在终端手动测试命令：
   ```bash
   python C:\Tools\webfetch.py "https://example.com" --pretty
   ```
2. 检查 Python 和 Playwright 是否安装正确
3. 检查代理配置

### 返回内容不完整

在指令中强调使用 `--scroll` 参数：

```json
{
  "text": "获取网页时始终使用 --scroll 参数确保获取完整内容"
}
```

## 快捷键配置（可选）

为常用操作添加快捷键：

**`keybindings.json`:**

```json
[
  {
    "key": "ctrl+shift+w",
    "command": "workbench.action.terminal.sendSequence",
    "args": { "text": "python C:\\Tools\\webfetch.py " },
    "when": "terminalFocus"
  }
]
```

## 参考链接

- [VS Code Copilot 文档](https://code.visualstudio.com/docs/copilot/copilot-customization)
- [GitHub Copilot 指令配置](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)
