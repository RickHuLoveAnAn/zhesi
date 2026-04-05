# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static HTML site presenting classical Chinese philosophical texts (道家/ Zhuangzi and Daoist classics) with traditional Chinese aesthetic. Pure static files — no build system, no tests, no dependencies.

## Directory Structure

- `/` — Zhuangzi (庄子) full text: 33 chapters across 内篇(7), 外篇(15), 杂篇(11)
- `/daojia/` — Seven Daoist classics: 清静经, 太乙金华宗旨, 道德经, 文子, 列子, 淮南子, 抱朴子
- `/daojia/index.html` — Navigation hub for Daoist texts

## Architecture

**Design System** — CSS variables define the aesthetic:
```
--ink, --ink-light, --paper, --vermilion, --gold, --muted, --border
```
Background: `#f5f0e6` (paper), Text: `#1a1208` (ink), Accent: `#b83a2e` (vermilion)

**Typography** — Google Fonts: `Noto Serif SC` (body), `ZCOOL XiaoWei` (headings)

**Shared Patterns** — All pages share: side-rule decoration, hero section, fade-up animations, IntersectionObserver reveal, float-nav panel

## Build System

`source_code/` contains Python scripts used to generate/update HTML files:
- `build_remaining.py` — generates remaining chapter HTMLs from source
- `add_float_nav.py` — injects float navigation panel into HTML
- `update_nav.py`, `redesign_nav*.py` — float-nav panel variants
- `fix_nav_css*.py`, `fix_nav_default.py` — float-nav CSS fixes

## Common Tasks

- **Serve locally**: any HTTP server, e.g. `python3 -m http.server 8080` or `npx serve`
- **Add a new Zhuangzi chapter**: run or adapt `source_code/build_remaining.py`, or copy an existing HTML file and update `<title>`, chapter number/name/description in TOC links, update float-nav if present
- **Add a new Daoist text**: add to `daojia/index.html` card grid and create the HTML file in `daojia/`

##朗读功能（MiniMax TTS）

用户激活 `minimax-multimodal-toolkit` 技能后，可让 AI 朗读文章。

**流程**：
1. 用户激活 `minimax-multimodal-toolkit` 技能
2. 用户说"朗读《逍遥游》"
3. AI 从 `data/{article-id}.json` 读取原文 blocks
4. 拼接所有 block.orig 为完整文本
5. 调用 MiniMax TTS API 生成音频（使用 `female-tianmei` 音色）
6. 返回 .mp3 文件给用户

**环境变量**（需要先 export）：
```bash
export MINIMAX_API_HOST='https://api.minimaxi.com'
export MINIMAX_API_KEY='sk-cp-...'
```

**注意**：长文章（>10000 字）需要分段调用 TTS API
