@echo off
REM WebFetch Tool - Windows Batch Wrapper
REM 用法: webfetch.bat <URL> [options]

set SCRIPT_DIR=%~dp0
python "%SCRIPT_DIR%webfetch.py" %*
