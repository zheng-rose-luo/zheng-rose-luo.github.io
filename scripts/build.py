#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import markdown
import re
from datetime import datetime
from pathlib import Path

def extract_front_matter(content):
    """提取 Markdown 文件头部的元数据"""
    front_matter = {'title': '未命名文章', 'date': '', 'excerpt': '', 'tags': ''}
    
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if match:
        meta_text = match.group(1)
        content = match.group(2)
        for line in meta_text.split('\n'):
            if ': ' in line:
                key, value = line.split(': ', 1)
                front_matter[key.strip()] = value.strip()
    
    return front_matter, content

def convert_md_to_html(md_path, back_to_root='../../'):
    """将 Markdown 文件转换为 HTML 文章详情页"""
    
    with open(md_path, 'r', encoding='utf-8') as f:
        raw_content = f.read()
    
    front_matter, content = extract_front_matter(raw_content)
    md = markdown.Markdown(extensions=['extra', 'toc', 'codehilite'])
    html_body = md.convert(content)
    
    title = front_matter.get('title', '文章')
    date = front_matter.get('date', '')
    
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
        <div class="site-title"><a href="{back_to_root}index.html">Zheng (Rose) Luo</a></div>
        <div class="nav">
            <a href="{back_to_root}index.html">About</a>
            <a href="{back_to_root}blog.html">Blog</a>
            <a href="{back_to_root}notes.html">Notes</a>
            <a href="{back_to_root}projects.html">Projects</a>
        </div>
    </div>

    <div class="post-content" style="margin-top: 1rem;">
        {html_body}
    </div>

    <div style="margin-top: 2rem; color: #6f6f6f; font-family: Arial, sans-serif; font-size: 0.85rem; border-top: 1px solid #f0ede8; padding-top: 1rem;">
        {date if date else ''}
    </div>

    <div class="footer-note">
        Zheng LUO · <a href="mailto:rose.zheng.luo@gmail.com" style="color: #a09a92; text-decoration: none;">rose.zheng.luo@gmail.com</a>
    </div>
</div>
</body>
</html>'''
    
    return html

def generate_list_page(items, page_type, title, subtitle):
    """生成列表页（blog.html / notes.html / projects.html）"""
    
    # 按日期排序（最新的在前）
    items_sorted = sorted(items, key=lambda x: x.get('date', ''), reverse=True)
    
    # 根据类型生成不同的列表项
    if page_type == 'blog':
        list_items = ''
        for item in items_sorted:
            list_items += f'''
            <div class="post-item">
                <h3><a href="{item['link']}" style="color: #1e1e1e; text-decoration: none;">{item['title']}</a></h3>
                <span class="post-date">{item['date']}</span>
                <p class="post-excerpt">{item.get('excerpt', '')}</p>
            </div>'''
    elif page_type == 'notes':
        list_items = ''
        for item in items_sorted:
            list_items += f'''
            <div class="note-item" style="padding: 1rem 0; border-bottom: 1px solid #ece8e2;">
                <span class="note-date" style="font-family: Arial, sans-serif; font-size: 0.8rem; color: #6f6f6f;">{item['date']}</span>
                <p style="margin-top: 0.2rem;">
                    <a href="{item['link']}" style="color: #1e1e1e; text-decoration: none; font-weight: 500;">{item['title']}</a>
                </p>
                <p style="margin-top: 0.2rem; color: #4f4f4f;">{item.get('excerpt', '')}</p>
            </div>'''
    else:  # projects
        list_items = ''
        for item in items_sorted:
            tags_html = ''
            if item.get('tags'):
                tags_html = f'<div class="project-tags" style="font-family: Arial, sans-serif; font-size: 0.75rem; color: #7a7a7a; margin-top: 0.2rem;">{item["tags"]}</div>'
            list_items += f'''
            <div class="project-item" style="padding: 1.2rem 0; border-bottom: 1px dashed #e2ddd6;">
                <div class="project-title" style="font-weight: 600; font-size: 1.05rem;">
                    <a href="{item['link']}" style="color: #1e1e1e; text-decoration: none;">{item['title']}</a>
                </div>
                <div class="project-desc" style="margin-top: 0.2rem; color: #3d3d3d;">
                    {item.get('excerpt', '')}
                </div>
                {tags_html}
            </div>'''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} · Zheng LUO</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🌹</text></svg>">
    <link rel="stylesheet" href="css/style.css">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
</head>
<body>
<div class="container">

    <div class="header">
        <div class="site-title"><a href="index.html">Zheng (Rose) Luo</a></div>
        <div class="nav">
            <a href="index.html">About</a>
            <a href="blog.html">Blog</a>
            <a href="notes.html">Notes</a>
            <a href="projects.html">Projects</a>
        </div>
    </div>

    <div class="page">
        <div style="margin-bottom: 1.8rem; border-bottom: 1px solid #eae7e2; padding-bottom: 0.5rem;">
            <h2 style="font-weight: 400; font-size: 1.8rem; display: inline; margin-right: 1rem;">{title}</h2>
            <span style="color: #6f6f6f; font-size: 0.95rem;">{subtitle}</span>
        </div>

        <div class="{'blog-list' if page_type == 'blog' else 'notes-list' if page_type == 'notes' else 'project-list'}">
            {list_items}
        </div>
    </div>

    <div class="footer-note">
        Zheng LUO · <a href="mailto:rose.zheng.luo@gmail.com" style="color: #a09a92; text-decoration: none;">rose.zheng.luo@gmail.com</a>
    </div>
</div>
</body>
</html>'''
    
    return html

def build_all():
    """构建所有内容"""
    
    all_blog_items = []
    all_notes_items = []
    all_projects_items = []
    
    # 1. 处理 blog
    blog_dir = Path('posts/blog')
    if blog_dir.exists():
        md_files = list(blog_dir.glob('*.md'))
        for md_path in md_files:
            print(f'🔄 正在转换: posts/blog/{md_path.name}')
            html_content = convert_md_to_html(md_path, back_to_root='../../')
            html_path = md_path.with_suffix('.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f'   ✅ 已生成: {html_path.name}')
            
            # 提取元数据用于列表页
            with open(md_path, 'r', encoding='utf-8') as f:
                raw = f.read()
            fm, _ = extract_front_matter(raw)
            all_blog_items.append({
                'title': fm.get('title', '未命名'),
                'date': fm.get('date', ''),
                'excerpt': fm.get('excerpt', ''),
                'link': f'posts/blog/{md_path.stem}.html'
            })
    else:
        print('⚠️ posts/blog/ 不存在')
    
    # 2. 处理 notes
    notes_dir = Path('posts/notes')
    if notes_dir.exists():
        md_files = list(notes_dir.glob('*.md'))
        for md_path in md_files:
            print(f'🔄 正在转换: posts/notes/{md_path.name}')
            html_content = convert_md_to_html(md_path, back_to_root='../../')
            html_path = md_path.with_suffix('.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f'   ✅ 已生成: {html_path.name}')
            
            with open(md_path, 'r', encoding='utf-8') as f:
                raw = f.read()
            fm, _ = extract_front_matter(raw)
            all_notes_items.append({
                'title': fm.get('title', '未命名'),
                'date': fm.get('date', ''),
                'excerpt': fm.get('excerpt', ''),
                'link': f'posts/notes/{md_path.stem}.html'
            })
    else:
        print('⚠️ posts/notes/ 不存在')
    
    # 3. 处理 projects
    projects_dir = Path('posts/projects')
    if projects_dir.exists():
        md_files = list(projects_dir.glob('*.md'))
        for md_path in md_files:
            print(f'🔄 正在转换: posts/projects/{md_path.name}')
            html_content = convert_md_to_html(md_path, back_to_root='../../')
            html_path = md_path.with_suffix('.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f'   ✅ 已生成: {html_path.name}')
            
            with open(md_path, 'r', encoding='utf-8') as f:
                raw = f.read()
            fm, _ = extract_front_matter(raw)
            all_projects_items.append({
                'title': fm.get('title', '未命名'),
                'date': fm.get('date', ''),
                'excerpt': fm.get('excerpt', ''),
                'tags': fm.get('tags', ''),
                'link': f'posts/projects/{md_path.stem}.html'
            })
    else:
        print('⚠️ posts/projects/ 不存在')
    
    # 4. 生成列表页
    print('\n📋 生成列表页...')
    
    # blog.html
    blog_html = generate_list_page(all_blog_items, 'blog', 'Blog', 'Deep dives into research, methods, and ideas.')
    with open('blog.html', 'w', encoding='utf-8') as f:
        f.write(blog_html)
    print('   ✅ 已生成: blog.html')
    
    # notes.html
    notes_html = generate_list_page(all_notes_items, 'notes', 'Notes', 'Short thoughts, daily discoveries, and research snippets.')
    with open('notes.html', 'w', encoding='utf-8') as f:
        f.write(notes_html)
    print('   ✅ 已生成: notes.html')
    
    # projects.html
    projects_html = generate_list_page(all_projects_items, 'projects', 'Research Projects', 'Current and past research, from soft matter to neurodynamics.')
    with open('projects.html', 'w', encoding='utf-8') as f:
        f.write(projects_html)
    print('   ✅ 已生成: projects.html')
    
    print('\n🎉 全部转换完成！')

if __name__ == '__main__':
    build_all()