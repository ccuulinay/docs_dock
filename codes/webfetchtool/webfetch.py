#!/usr/bin/env python3
"""
WebFetch Tool - 基于 Playwright 的网页内容获取工具
用于 GitHub Copilot 在受限网络环境下访问网页内容

环境要求:
- Python 3.8+
- Playwright: pip install playwright
- Playwright browsers: playwright install chromium
"""

import asyncio
import argparse
import json
import sys
import os
from typing import Optional, Dict, Any
from urllib.parse import urlparse

from playwright.async_api import async_playwright, Page, Browser, BrowserContext


class WebFetchTool:
    """网页内容获取工具"""
    
    def __init__(
        self,
        proxy: Optional[str] = None,
        timeout: int = 30000,
        wait_for: Optional[str] = None,
        scroll: bool = False,
        extract_text: bool = True
    ):
        """
        初始化 WebFetchTool
        
        Args:
            proxy: 代理服务器地址，如 "http://proxy.company.com:8080"
            timeout: 页面加载超时时间（毫秒）
            wait_for: 等待特定选择器出现
            scroll: 是否滚动页面以加载懒加载内容
            extract_text: 是否提取纯文本内容（而非HTML）
        """
        self.proxy = proxy or os.environ.get('HTTP_PROXY') or os.environ.get('HTTPS_PROXY')
        self.timeout = timeout
        self.wait_for = wait_for
        self.scroll = scroll
        self.extract_text = extract_text
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            'headless': True,
        }
        
        # 如果配置了代理
        if self.proxy:
            browser_args['proxy'] = {'server': self.proxy}
        
        self.browser = await playwright.chromium.launch(**browser_args)
        
        # 创建上下文
        context_args = {
            'user_agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ),
            'viewport': {'width': 1920, 'height': 1080},
        }
        
        self.context = await self.browser.new_context(**context_args)
        
        # 添加基本的反检测脚本
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
        """)
        
        self.page = await self.context.new_page()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
    
    async def fetch(self, url: str) -> Dict[str, Any]:
        """
        获取网页内容
        
        Args:
            url: 目标URL
            
        Returns:
            包含页面信息的字典
        """
        if not self.page:
            raise RuntimeError("Browser not initialized. Use 'async with' context manager.")
        
        result = {
            'url': url,
            'success': False,
            'title': '',
            'content': '',
            'error': None,
            'metadata': {}
        }
        
        try:
            # 导航到页面
            response = await self.page.goto(
                url, 
                wait_until='networkidle',
                timeout=self.timeout
            )
            
            if not response:
                result['error'] = 'Failed to get response from server'
                return result
            
            # 记录响应信息
            result['metadata']['status'] = response.status
            result['metadata']['content_type'] = response.headers.get('content-type', 'unknown')
            
            # 等待特定元素（如果指定）
            if self.wait_for:
                try:
                    await self.page.wait_for_selector(
                        self.wait_for, 
                        timeout=self.timeout
                    )
                except Exception as e:
                    result['metadata']['wait_warning'] = f"Wait for selector failed: {str(e)}"
            
            # 滚动页面以加载懒加载内容
            if self.scroll:
                await self._scroll_page()
            
            # 获取页面标题
            result['title'] = await self.page.title()
            
            # 获取页面内容
            if self.extract_text:
                # 提取纯文本内容
                result['content'] = await self._extract_text_content()
            else:
                # 获取HTML内容
                result['content'] = await self.page.content()
            
            # 获取元数据
            result['metadata']['description'] = await self._get_meta_description()
            
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    async def _scroll_page(self):
        """滚动页面以加载懒加载内容"""
        if not self.page:
            return
        
        # 获取页面高度
        last_height = await self.page.evaluate('document.body.scrollHeight')
        
        while True:
            # 滚动到底部
            await self.page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            
            # 等待内容加载
            await asyncio.sleep(0.5)
            
            # 检查新高度
            new_height = await self.page.evaluate('document.body.scrollHeight')
            
            if new_height == last_height:
                break
            
            last_height = new_height
            
            # 限制滚动次数，避免无限滚动
            if last_height > 50000:  # 最大50k像素
                break
    
    async def _extract_text_content(self) -> str:
        """提取页面的纯文本内容"""
        if not self.page:
            return ''
        
        # 使用 JavaScript 提取主要内容
        text_content = await self.page.evaluate("""
            () => {
                // 移除脚本和样式元素
                const scripts = document.querySelectorAll('script, style, nav, footer, aside');
                scripts.forEach(el => el.remove());
                
                // 获取主要内容区域（优先选择常见的内容容器）
                const contentSelectors = [
                    'article',
                    'main',
                    '[role="main"]',
                    '.content',
                    '#content',
                    '.post-content',
                    '.article-content',
                    '.entry-content'
                ];
                
                for (const selector of contentSelectors) {
                    const element = document.querySelector(selector);
                    if (element) {
                        return element.innerText;
                    }
                }
                
                // 如果没有找到特定容器，返回body文本
                return document.body.innerText;
            }
        """)
        
        # 清理文本
        lines = text_content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            # 过滤空行和过短的行
            if line and len(line) > 2:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    async def _get_meta_description(self) -> str:
        """获取页面的 meta description"""
        if not self.page:
            return ''
        
        try:
            meta = await self.page.query_selector('meta[name="description"]')
            if meta:
                return await meta.get_attribute('content') or ''
        except:
            pass
        
        return ''


async def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='WebFetch Tool - 获取网页内容',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本使用
  python webfetch.py https://example.com
  
  # 使用代理
  python webfetch.py https://example.com --proxy "http://proxy.company.com:8080"
  
  # 获取HTML源码
  python webfetch.py https://example.com --html
  
  # 等待特定元素加载
  python webfetch.py https://example.com --wait-for "#main-content"
  
  # 滚动页面加载懒加载内容
  python webfetch.py https://example.com --scroll
        """
    )
    
    parser.add_argument('url', help='要获取的网页URL')
    parser.add_argument('--proxy', '-p', help='代理服务器地址')
    parser.add_argument('--timeout', '-t', type=int, default=30000, 
                        help='页面加载超时时间（毫秒，默认30000）')
    parser.add_argument('--wait-for', '-w', help='等待特定CSS选择器出现')
    parser.add_argument('--scroll', '-s', action='store_true',
                        help='滚动页面以加载懒加载内容')
    parser.add_argument('--html', action='store_true',
                        help='返回HTML源码而非纯文本')
    parser.add_argument('--output', '-o', help='输出文件路径（默认输出到stdout）')
    parser.add_argument('--pretty', action='store_true',
                        help='美化JSON输出')
    
    args = parser.parse_args()
    
    # 验证URL
    parsed = urlparse(args.url)
    if not parsed.scheme or not parsed.netloc:
        print(json.dumps({
            'success': False,
            'error': f'Invalid URL: {args.url}'
        }, ensure_ascii=False))
        sys.exit(1)
    
    # 执行获取
    async with WebFetchTool(
        proxy=args.proxy,
        timeout=args.timeout,
        wait_for=args.wait_for,
        scroll=args.scroll,
        extract_text=not args.html
    ) as fetcher:
        result = await fetcher.fetch(args.url)
    
    # 输出结果
    output = json.dumps(
        result, 
        ensure_ascii=False, 
        indent=2 if args.pretty else None
    )
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Result saved to: {args.output}")
    else:
        print(output)
    
    # 根据成功与否设置退出码
    sys.exit(0 if result['success'] else 1)


if __name__ == '__main__':
    asyncio.run(main())
