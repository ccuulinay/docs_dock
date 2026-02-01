#!/bin/bash
# WebFetch Tool - Git Bash Wrapper
# 用法: ./webfetch.sh <URL> [options]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python "${SCRIPT_DIR}/webfetch.py" "$@"
