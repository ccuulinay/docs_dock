#!/usr/bin/env python3
"""
WebFetch Tool 测试脚本
用于验证安装和基本功能
"""

import asyncio
import json
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from webfetch import WebFetchTool


async def test_basic_fetch():
    """测试基本获取功能"""
    print("=" * 60)
    print("测试 1: 基本获取功能")
    print("=" * 60)
    
    async with WebFetchTool() as fetcher:
        result = await fetcher.fetch("https://example.com")
    
    print(f"URL: {result['url']}")
    print(f"Success: {result['success']}")
    print(f"Title: {result['title']}")
    print(f"Content length: {len(result['content'])}")
    print(f"Status: {result['metadata'].get('status', 'N/A')}")
    
    if result['error']:
        print(f"Error: {result['error']}")
    
    # 显示部分内容
    if result['content']:
        print("\nContent preview:")
        print("-" * 40)
        print(result['content'][:500] + "..." if len(result['content']) > 500 else result['content'])
    
    return result['success']


async def test_with_scroll():
    """测试滚动功能"""
    print("\n" + "=" * 60)
    print("测试 2: 滚动功能")
    print("=" * 60)
    
    async with WebFetchTool(scroll=True) as fetcher:
        result = await fetcher.fetch("https://example.com")
    
    print(f"URL: {result['url']}")
    print(f"Success: {result['success']}")
    print(f"Content length: {len(result['content'])}")
    
    return result['success']


async def test_html_mode():
    """测试HTML模式"""
    print("\n" + "=" * 60)
    print("测试 3: HTML 模式")
    print("=" * 60)
    
    async with WebFetchTool(extract_text=False) as fetcher:
        result = await fetcher.fetch("https://example.com")
    
    print(f"URL: {result['url']}")
    print(f"Success: {result['success']}")
    print(f"HTML length: {len(result['content'])}")
    
    # 检查是否包含HTML标签
    has_html = '<html' in result['content'].lower() or '<!doctype' in result['content'].lower()
    print(f"Contains HTML tags: {has_html}")
    
    return result['success'] and has_html


async def test_error_handling():
    """测试错误处理"""
    print("\n" + "=" * 60)
    print("测试 4: 错误处理")
    print("=" * 60)
    
    async with WebFetchTool(timeout=5000) as fetcher:
        result = await fetcher.fetch("https://invalid-domain-that-does-not-exist.com")
    
    print(f"URL: {result['url']}")
    print(f"Success: {result['success']}")
    print(f"Error: {result['error']}")
    
    # 预期失败
    return not result['success']


async def run_all_tests():
    """运行所有测试"""
    print("\n" + "#" * 60)
    print("# WebFetch Tool 测试套件")
    print("#" * 60 + "\n")
    
    results = []
    
    try:
        results.append(("基本获取", await test_basic_fetch()))
    except Exception as e:
        print(f"测试 1 失败: {e}")
        results.append(("基本获取", False))
    
    try:
        results.append(("滚动功能", await test_with_scroll()))
    except Exception as e:
        print(f"测试 2 失败: {e}")
        results.append(("滚动功能", False))
    
    try:
        results.append(("HTML模式", await test_html_mode()))
    except Exception as e:
        print(f"测试 3 失败: {e}")
        results.append(("HTML模式", False))
    
    try:
        results.append(("错误处理", await test_error_handling()))
    except Exception as e:
        print(f"测试 4 失败: {e}")
        results.append(("错误处理", False))
    
    # 打印汇总
    print("\n" + "#" * 60)
    print("# 测试结果汇总")
    print("#" * 60)
    
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name}: {status}")
    
    all_passed = all(r[1] for r in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有测试通过！WebFetch Tool 工作正常。")
    else:
        print("⚠️ 部分测试失败，请检查配置。")
    print("=" * 60)
    
    return all_passed


if __name__ == '__main__':
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
