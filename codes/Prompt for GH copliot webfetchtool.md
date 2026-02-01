# Customized webfetchtool and system prompt part to call it
我要设计一个 webfetchtool 和对应的系统提示词部分，用于我的公司的开发环境的vscode中的GitHub Copilot。
## 我公司的开发环境主要有以下配置和限制：
1. 在Visual studio code中使用GitHub Copilot 的plugins来使用GitHub Copilot。
2. 我的GitHub Copilot 没有MCP的权限。
3. GitHub Copilot内置的websearch 和webfetch功能不能正常工作，因为我的环境里面，浏览器只有通过一个特定的proxy才能访问外部网络。
4. 我能安装playwright，并正常使用。
5. 我的操作系统是Windows，不过我有Git bash可以使用。系统已经安装了node 和Python，并且可以正常安装modules and packages。

## Task
1. 基于上述的配置和限制，设计实现一个webfetchtool，可以在GitHub Copilot需要访问网络的时候去调用。
2. 同时设计实现一个系统提示词片段，可以加到不同的系统提示词中，使得GitHub Copilot能学习到在需要访问网络的场合，能稳定地调用上面实现的webfetchtool。
