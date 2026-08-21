#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import markdown
import re
from datetime import datetime
from pathlib import Path

def extract_front_matter(content):
    """提取 Markdown 文件头部的元数据"""
    front_matter = {'title': '未命名文章', 'date': datetime.now().strftime('%Y-%m-%d'), 'excerpt': ''}
    
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if match:
        meta_text = match.group(1)
        content = match.group(2)
        for line in meta_text.split('\n'):
            if ': ' in line:
                key, value = line.split(': ', 1)
                front_matter[key.strip()] = value.strip()
    
    return front_matter, content

def convert_md_to_html(md_path, css_path='../../css/style.css', back_to_root='../../'):
    """将 Markdown 文件转换为 HTML"""
    
    with open(md_path, 'r', encoding='utf-8') as f:
        raw_content = f.read()
    
    front_matter, content = extract_front_matter(raw_content)
    md = markdown.Markdown(extensions=['extra', 'toc', 'codehilite'])
    html_body = md.convert(content)
    
    title = front_matter.get('title', '文章')
    date = front_matter.get('date', '')
    excerpt = front_matter.get('excerpt', '')
    
    # 判断当前文件类型
    if 'blog' in str(md_path):
        nav_link = '../../blog.html'
        nav_active = 'Blog'
    elif 'notes' in str(md_path):
        nav_link = '../../notes.html'
        nav_active = 'Notes'
    elif 'projects' in str(md_path):
        nav_link = '../../projects.html'
        nav_active = 'Projects'
    else:
        nav_link = '../../index.html'
        nav_active = 'About'
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} · Zheng LUO</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🌹</text></svg>">
    <link rel="stylesheet" href="{back_to_root}css/style.css">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    <script>
        MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']]
            }}
        }};
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
</head>
<body>
<div class="container">
    
    <div class="header">
        <div class="site-title"><a href="{back_to_root}index.html">🌹 Zheng (Rose) Luo</a></div>
        <div class="nav">
            <a href="{back_to_root}index.html">About</a>
            <a href="{back_to_root}blog.html">Blog</a>
            <a href="{back_to_root}notes.html">Notes</a>
            <a href="{back_to_root}projects.html">Projects</a>
        </div>
    </div>

    <!-- 文章内容：只显示正文，不再重复标题 -->
    <div class="post-content" style="margin-top: 1rem;">
        {html_body}
    </div>

    <!-- 显示日期 -->
    <div style="margin-top: 2rem; color: #6f6f6f; font-family: Arial, sans-serif; font-size: 0.85rem; border-top: 1px solid #f0ede8; padding-top: 1rem;">
        {date if date else ''}
    </div>

    <div class="footer-note">
        Zheng (Rose) Luo · <a href="mailto:rose.zheng.luo@gmail.com" style="color: #a09a92; text-decoration: none;">rose.zheng.luo@gmail.com</a>
    </div>
</div>
</body>
</html>'''
    
    return html

def build_all():
    """构建所有 .md 文件"""
    
    # 处理 blog
    blog_dir = Path('posts/blog')
    if blog_dir.exists():
        md_files = list(blog_dir.glob('*.md'))
        for md_path in md_files:
            print(f'🔄 正在转换: {md_path.name}')
            html_content = convert_md_to_html(md_path, back_to_root='../../')
            html_path = md_path.with_suffix('.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f'   ✅ 已生成: {html_path.name}')
    else:
        print('⚠️ posts/blog/ 不存在')
    
    # 处理 notes
    notes_dir = Path('posts/notes')
    if notes_dir.exists():
        md_files = list(notes_dir.glob('*.md'))
        for md_path in md_files:
            print(f'🔄 正在转换: {md_path.name}')
            html_content = convert_md_to_html(md_path, back_to_root='../../')
            html_path = md_path.with_suffix('.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f'   ✅ 已生成: {html_path.name}')
    else:
        print('⚠️ posts/notes/ 不存在')
    
    # 处理 projects
    projects_dir = Path('posts/projects')
    if projects_dir.exists():
        md_files = list(projects_dir.glob('*.md'))
        for md_path in md_files:
            print(f'🔄 正在转换: {md_path.name}')
            html_content = convert_md_to_html(md_path, back_to_root='../../')
            html_path = md_path.with_suffix('.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f'   ✅ 已生成: {html_path.name}')
    else:
        print('⚠️ posts/projects/ 不存在')
    
    print('🎉 全部转换完成！')

if __name__ == '__main__':
    build_all()