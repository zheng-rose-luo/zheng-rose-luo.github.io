#!/usr/bin/env python3
"""Build GitHub Pages HTML from editable pages/*.md and posts/*/*.md."""
from html import escape
from pathlib import Path
from hashlib import sha256
import shutil
import re
import markdown

ROOT = Path(__file__).resolve().parent
NAME = 'Zheng (Rose) Luo'
EMAIL = 'rose.zheng.luo@gmail.com'
CV_PATH = 'assets/pdfs/Zheng_Luo_CV.pdf'
CV_LEGACY_PATH = 'assets/pdfs/CV_Zheng_Luo_EN.pdf'
NAV = [('index.html', 'About'), ('projects.html', 'Research'),
       ('interests.html', 'Interests'), ('blog.html', 'Writing'), ('notes.html', 'Notes')]


def cv_url(prefix=''):
    # A stable filename with a content version avoids stale browser copies.
    version = sha256((ROOT / CV_PATH).read_bytes()).hexdigest()[:12]
    return f'{prefix}{CV_PATH}?v={version}'


def read_md(path):
    raw = path.read_text(encoding='utf-8-sig').replace('\r\n', '\n')
    match = re.match(r'^---\n(.*?)\n---\s*\n(.*)', raw, re.S)
    meta = {}
    if match:
        for line in match[1].splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                meta[key.strip()] = value.strip().strip('"').strip("'")
        raw = match[2]
    meta.setdefault('title', path.stem.replace('-', ' '))
    return meta, raw


def render_md(body, prefix=''):
    # Protect TeX from Markdown emphasis and backslash processing.
    math = []
    def protect(match):
        math.append(match[0])
        return f'MATHPLACEHOLDER{len(math)-1}END'
    body = re.sub(r'\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]|\\\([^\n]*?\\\)|(?<!\\)\$(?!\$)[^\n$]+(?<!\\)\$', protect, body)
    md = markdown.Markdown(extensions=['extra', 'toc', 'sane_lists'],
                           extension_configs={'toc': {'toc_depth': '2-3'}})
    result = md.convert(body)
    for i, value in enumerate(math):
        result = result.replace(f'MATHPLACEHOLDER{i}END', escape(value))
    # Root-relative assets from older notes also work in local file previews.
    result = re.sub(r'((?:src|href)=["\'])/assets/', rf'\1{prefix}assets/', result)
    return result, md.toc, bool(math)


def shell(title, content, active, prefix='', description='', math=False, lang='en'):
    links = ''.join(f'<a href="{prefix}{url}"' + (' aria-current="page"' if url == active else '')
                    + f'>{label}</a>' for url, label in NAV)
    links += f'<a href="{cv_url(prefix)}" target="_blank" rel="noopener">CV <span class="file-label">(PDF)</span></a>'
    maths = r'''<script>window.MathJax={tex:{inlineMath:[['$','$'],['\\(','\\)']],displayMath:[['$$','$$'],['\\[','\\]']]}};</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>''' if math else ''
    return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} | {NAME}</title><meta name="description" content="{escape(description, quote=True)}">
<link rel="icon" type="image/png" sizes="32x32" href="{prefix}assets/images/favicon-32x32.png">
<link rel="apple-touch-icon" href="{prefix}assets/images/apple-touch-icon.png">
<link rel="manifest" href="{prefix}site.webmanifest"><link rel="stylesheet" href="{prefix}css/style.css"><link rel="stylesheet" href="{prefix}css/content.css">{maths}</head>
<body><a class="skip-link" href="#main">Skip to content</a><div class="wrap">
<header><a class="brand" href="{prefix}index.html">{NAME}</a><nav aria-label="Main navigation">{links}</nav></header>
<main id="main">{content}</main>
<footer><span>{NAME}</span><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{prefix}notes.html">Personal notes</a></footer>
</div></body></html>\n'''


def write(path, html):
    (ROOT / path).write_text(html, encoding='utf-8')


def page(name):
    meta, body = read_md(ROOT / 'pages' / f'{name}.md')
    return meta, render_md(body)[0]


def research_direction(detail=False):
    meta, body = read_md(ROOT / 'pages' / 'goals.md')
    chunks = re.split(r'^## (.+)\n', body, flags=re.M)
    sections = {key: render_md(value.strip())[0]
                for key, value in zip(chunks[1::2], chunks[2::2])}
    columns = ''.join(
        f'<div class="goal-column"><p class="eyebrow">{label}</p>'
        f'<h3>{escape(meta[heading])}</h3>{sections[label]}</div>'
        for label, heading in [('Scientific goal', 'scientific_heading'),
                               ('Engineering goal', 'engineering_heading')]
    )
    destination = '#a-possible-starting-question' if detail else 'interests.html'
    link = 'Explore a possible starting question' if detail else 'Explore my research interests'
    return f'''<section class="research-direction" aria-labelledby="direction-title">
<div class="direction-heading"><p class="eyebrow">{escape(meta['eyebrow'])}</p>
<h2 id="direction-title">{escape(meta['title'])}</h2></div>
<div class="goal-columns">{columns}</div>
<div class="shared-approach">{sections['Shared approach']}
<a class="textlink" href="{destination}">{link}</a></div></section>'''


def project_card(item, compact=False):
    image = ''
    if item.get('image'):
        image = f'<img loading="lazy" src="{escape(item["image"], quote=True)}" alt="{escape(item.get("image_alt", item["title"]), quote=True)}">'
    info = f'''<p class="meta">{escape(item.get('period', ''))}</p><h2><a href="{item['link']}">{escape(item['title'])}</a></h2>
<p>{escape(item.get('excerpt', ''))}</p><p class="meta">{escape(item.get('status', ''))}</p><a class="textlink" href="{item['link']}">Read the project</a>'''
    if compact:
        return f'<article class="small-project">{image}<div>{info}</div></article>'
    return f'<article class="portfolio-row"><div class="portfolio-image">{image}</div><div>{info}</div></article>'


def build_post(path, kind):
    meta, body = read_md(path)
    if meta.get('draft', '').lower() == 'true':
        # Remove only this post's generated HTML when marking it a draft.
        path.with_suffix('.html').unlink(missing_ok=True)
        return None
    prefix = '../../'
    body = re.sub(r'^\s*# [^\n]+\n', '', body, count=1)
    rendered, toc, math = render_md(body, prefix)
    # Older bilingual notes use another H1 for the translated section.
    rendered = re.sub(r'<(/?)h1(\b[^>]*)>', r'<\1h2\2>', rendered)
    category = {'projects': 'Research project', 'blog': 'Research writing', 'notes': 'Personal notebook'}[kind]
    date = meta.get('date', '')
    if meta.get('updated'):
        date += f' · Updated {meta["updated"]}'
    status = meta.get('status', '')
    note = '<p class="notebook-label">A personal observation or question, recorded at the time of writing.</p>' if kind == 'notes' else ''
    header = f'''<div class="page-title"><p class="eyebrow">{category}</p><h1>{escape(meta['title'])}</h1>
<p class="intro">{escape(meta.get('excerpt', ''))}</p><p class="meta">{escape(date)}{(' · '+escape(status)) if status else ''}</p>{note}</div>'''
    if kind == 'projects' and 'href=' in toc:
        content = f'{header}<div class="article-layout"><aside class="page-toc" aria-label="On this page"><p class="eyebrow">On this page</p>{toc}</aside><article class="prose">{rendered}</article></div>'
    else:
        content = f'{header}<article class="prose reading">{rendered}</article>'
    active = {'projects': 'projects.html', 'blog': 'blog.html', 'notes': 'notes.html'}[kind]
    content += f'<p class="back-link"><a href="{prefix}{active}">All {"research projects" if kind == "projects" else "writing" if kind == "blog" else "notes"}</a></p>'
    target = path.with_suffix('.html').relative_to(ROOT).as_posix()
    write(target, shell(meta['title'], content, active, prefix, meta.get('excerpt', ''), math, meta.get('lang', 'en')))
    return dict(meta, link=target)


def listing(items):
    return '<div class="writing-list">' + ''.join(f'''<article class="writing-item"><p class="meta">{escape(i.get('date', ''))}</p>
<h2><a href="{i['link']}">{escape(i['title'])}</a></h2><p>{escape(i.get('excerpt', ''))}</p></article>''' for i in items) + '</div>'


def build_all():
    # Preserve the previous public CV URL as an alias of the current file.
    shutil.copyfile(ROOT / CV_PATH, ROOT / CV_LEGACY_PATH)
    collections = {}
    for kind in ('projects', 'blog', 'notes'):
        items = [build_post(path, kind) for path in sorted((ROOT / 'posts' / kind).glob('*.md'))]
        collections[kind] = [item for item in items if item]
    projects = sorted(collections['projects'], key=lambda i: (int(i.get('order', '99')), i['title']))
    blogs = sorted(collections['blog'], key=lambda i: i.get('date', ''), reverse=True)
    notes = sorted(collections['notes'], key=lambda i: i.get('date', ''), reverse=True)

    meta, intro = page('research')
    _, publications = page('publications')
    content = f'<div class="page-title"><p class="eyebrow">{escape(meta["eyebrow"])}</p>{intro}</div>'
    content += ''.join(project_card(i) for i in projects)
    content += f'<section class="prose publications">{publications}</section>'
    html = shell(meta['title'], content, 'projects.html', description=meta['description'])
    write('projects.html', html)
    write('research.html', html)

    meta, body = read_md(ROOT / 'pages' / 'interests.md')
    introduction, questions = re.split(r'(?=^## )', body, maxsplit=1, flags=re.M)
    content = f'<div class="page-title"><p class="eyebrow">{escape(meta["eyebrow"])}</p>{render_md(introduction)[0]}</div>'
    content += research_direction(detail=True)
    content += f'<article class="prose reading interests">{render_md(questions)[0]}</article>'
    write('interests.html', shell(meta['title'], content, 'interests.html', description=meta['description']))

    content = '<div class="page-title"><p class="eyebrow">Reading and research</p><h1>Writing</h1><p class="intro">Research explanations, reading notes and questions that grow out of them.</p></div>' + listing(blogs)
    content += '<p class="back-link">For small discoveries and everyday observations, visit <a href="notes.html">Personal notes</a>.</p>'
    write('blog.html', shell('Writing', content, 'blog.html', description='Research writing and reading notes by Zheng Luo.'))
    content = '<div class="page-title"><p class="eyebrow">A personal notebook</p><h1>Notes</h1><p class="intro">Small discoveries, sketches and questions from everyday life. These entries preserve thoughts as they developed; they are not presented as research findings.</p></div>' + listing(notes)
    write('notes.html', shell('Notes', content, 'notes.html', description='Personal observations, sketches and open questions by Zheng Luo.'))

    meta, body = page('about')
    body = body.replace('<p>', '<p class="lead">', 1)
    hero = f'''<section class="hero"><div class="hero-layout"><div><p class="eyebrow">{escape(meta['eyebrow'])}</p>{body}</div>
<img class="portrait" src="assets/images/MyPhoto.jpg" alt="Zheng Luo"></div>
<div class="actions"><a class="button" href="interests.html">Research interests</a><a href="{cv_url()}" download="Zheng_Luo_CV.pdf">Download CV (PDF)</a><a href="projects.html">Explore my research</a><a href="mailto:{EMAIL}">Get in touch</a></div></section>'''
    selected = '<section aria-labelledby="selected-heading"><div class="section-title"><h2 id="selected-heading">Selected research</h2><a class="textlink" href="projects.html">All projects</a></div>'
    if projects:
        first = projects[0]
        selected += f'''<article class="feature"><figure class="feature-media"><img src="{escape(first.get('image', ''), quote=True)}" alt="{escape(first.get('image_alt', first['title']), quote=True)}"><figcaption>Electrostatic simulation around a prescribed conducting tip.</figcaption></figure><div class="feature-copy"><p class="eyebrow">Theory, computation and experiment</p><h2>{escape(first['title'])}</h2><p>{escape(first.get('excerpt', ''))}</p><a class="textlink" href="{first['link']}">Read the research story</a></div></article>'''
    by_slug = {Path(i['link']).stem: i for i in projects}
    selected += '<div class="research-pair">' + ''.join(project_card(by_slug[slug], True) for slug in ('neuroeff', 'polymer-network-phase-diagram') if slug in by_slug) + '</div></section>'
    writing_links = ''.join(f'<li><a href="{i["link"]}">{escape(i["title"])}</a></li>' for i in blogs[:2])
    below = f'''<section class="below"><div><h2>Research writing</h2><ul>{writing_links}</ul></div><div><h2>Small discoveries</h2><p>Observations, sketches and open questions recorded along the way.</p><p><a href="notes.html">Browse my personal notes</a></p></div></section>'''
    write('index.html', shell('About', hero + research_direction() + selected + below, 'index.html', description=meta['description']))
    write('electrical-failure.html', shell('Electrical failure', '<div class="page-title"><h1>Electrical failure and defect tolerance</h1><p><a href="posts/projects/dielectric-breakdown-theory.html">Read the full research project</a></p></div>', 'projects.html'))
    print(f'Built home, research, interests, writing and notes; {len(projects)} projects, {len(blogs)} articles, {len(notes)} notes.')


if __name__ == '__main__':
    build_all()
