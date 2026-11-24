# 网站维护说明

这份版本延续原有的 **Markdown → HTML → git push** 工作方式。页面已生成，可直接打开 `index.html` 查看；日后修改内容时优先编辑 Markdown，随后重新生成网页。

## 改哪里

| 内容 | 可编辑文件 |
| --- | --- |
| 首页自我介绍 | `pages/about.md` |
| 首页与 Interests 共享的研究双目标 | `pages/goals.md` |
| 研究兴趣、未来方向、实验训练意愿 | `pages/interests.md` |
| 研究总览开头 | `pages/research.md` |
| 早期论文与会议成果 | `pages/publications.md` |
| 项目详情 | `posts/projects/*.md` |
| 研究长文与阅读笔记 | `posts/blog/*.md` |
| 日常观察与短札 | `posts/notes/*.md` |
| 研究图片 | `assets/images/research/` |
| 网站当前公开的 CV | `assets/pdfs/Zheng_Luo_CV.pdf` |
| 页面布局和公共导航 | `build.py` |
| 样式 | `css/style.css`、`css/content.css` |

首页展示代表项目，个人短札不会再自动占据首页主体。Notes 中保留了全部 13 篇原有短札；两个关于学习的观察改成了更精确的问题表述，另一篇修正了中英文含义相反的一个词。

项目保留原有 3 个文件名，并新增 `neuroeff.md`、`astrocyte-potassium-dynamics.md`。原有文章网址继续有效。`projects.html` 是研究入口，`research.html` 也可访问同一总览。

## 日常更新

在 VS Code 中打开网站文件夹。若 Python 尚未安装 Markdown 依赖，先运行一次：

```powershell
python -m pip install -r requirements.txt
```

编辑 Markdown 后运行：

```powershell
python build.py
```

脚本以自身所在目录为网站根目录，也可以从别处用完整路径运行。生成内容包括首页、研究总览、研究兴趣、Writing、Notes 和文章 HTML。**不要只改生成的 HTML；下一次生成会覆盖它。**

可直接打开 `index.html`，或者在网站文件夹运行本机预览：

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

浏览器访问 `http://127.0.0.1:8000`，结束时在终端按 Ctrl+C。

确认页面后，仍按原来的方式检查差异、提交并推送。Markdown 和生成的 HTML 都要纳入提交。这个交付副本没有附带 `.git`，也没有自动推送到 GitHub；接入原目录时应保留原来的 `.git`。

## 更新 CV

网站导航栏提供 `CV (PDF)`，首页提供 `Download CV (PDF)`。当前文件使用你指定的 `Zheng Luo_CV_261109.pdf`，内容原样保留。

以后只需把新 PDF 复制到 `assets/pdfs/`，统一命名为 `Zheng_Luo_CV.pdf` 并替换同名文件，然后运行 `python build.py`，检查网页，按原流程提交并推送。

在原网站目录使用 PowerShell 时，本次文件也可以这样更新：

```powershell
Copy-Item -LiteralPath 'D:\JustNeuro\CVMaterial\Zheng Luo_CV_261109.pdf' -Destination 'D:\Code\easy-website\assets\pdfs\Zheng_Luo_CV.pdf' -Force
python 'D:\Code\easy-website\build.py'
```

生成脚本会同步旧地址 `assets/pdfs/CV_Zheng_Luo_EN.pdf`，使以前分享的链接继续提供当前版本。导航和下载入口自动带有根据 PDF 内容生成的版本标记，因此替换 PDF 并重新生成后，访问者会请求新版文件。

请把两个 PDF、`build.py` 和新生成的 HTML 一同提交。研究目标以后只需编辑 `pages/goals.md`；首页和 Interests 会使用同一份内容。

## 新增文章

把文章放进对应目录，使用下列开头。日期沿用实际初写时间；后续较大修订添加 `updated`，不必把原日期改成今天。

```markdown
---
title: 文章标题
date: 2026-11-24
excerpt: 一到两句话的简介。
tags: Learning · Research notes
---

# 文章标题

正文……
```

元数据采用简单的单行 `字段: 内容`，不要使用多行 YAML 写法。中英文正文均可。正文里不用再放第二组元数据；中文版可以使用 `## 中文标题`。

项目可额外设置 `period`（研究开展年份）、`order`（研究列表顺序）、`status`（工作阶段）、`image`（从网站根目录起的相对路径）、`image_alt`（图片说明）。首页固定选取电击穿、neuroEFF 和聚合物项目，以研究总览的顺序组织。

带图注的研究图可以保留现有 `<figure>` 格式，其余内容用普通 Markdown 即可。复制同目录文章中的图片路径最方便。

## 草稿与历史内容

`draft: true` 会阻止文章出现在列表中，并移除这篇文章旧的生成 HTML。Markdown 仍在仓库中：**公开 GitHub 仓库里的 Markdown 不是私人存储空间**。真正不准备公开的内容应留在仓库之外。

Notes 用于保留观察、创作与开放问题；研究项目和长文应更严格地区分观察、解释、证据与尚待检验的判断。文章是否短，不是删除标准。

## 本次内容修订

- 首页与 Interests 改为“理解大脑的计算原理，并用它们改进人工智能”的双目标，明确希望亲自参与实验。
- 五个研究项目使用已核对材料，区分本人贡献、合作贡献与研究阶段。
- 旧力学长文删除了未核实公式、缺陷材料表和超出证据的结论；阅读笔记核对了论文原文并保留双语。
- 图片来自已有研究材料。旧图片、短札和原有 URL 均保留。
- 首页新增研究双目标区域，Interests 区分两个目标的评价标准，并加入一个可收窄的起点问题。
- CV 使用指定的 261109 版本，恢复导航与首页入口，保持旧 CV 地址可用。

本次交付是原网站的可检查副本。D 盘原目录未被覆盖，线上网站未被更新。
