# DESIGN.md — 齐物论 (Zhesi)

纯静态 HTML 网站，展示古典中国哲学文本（庄子及道家经典），采用纯正东亚传统美学风格。无构建系统、无依赖项——纯 HTML/CSS/JS 静态文件服务。

---

## 1. 视觉风格与氛围

**美学定位：** 古典中国水墨画 × 学术羊皮纸。页面给人的感觉应该如同在宁静书斋中阅读古籍——温暖的纸色、深沉的墨字、朱砂与金色点缀，唤起印章篆刻与金镶玉边的意象。

**整体气质：** 沉静、雅致、永恒。不是为极简而极简，而是像一本被反复翻阅的好书那样自然地克制——每个元素都有它存在的理由。

**差异化特色：**
- Hero 区域使用 AI 生成的水墨画作为氛围背景
- 双栏布局（原文 / 注释）呼应古典文献"注疏"传统
- 滚动监听以朱砂高亮当前阅读段落，营造引导感

---

## 2. 色彩系统

```css
--ink:          #1a1208;   /* 主文字、标题 —— 深沉墨黑 */
--ink-light:    #4a3f2f;   /* 次级文字、副标题 */
--paper:        #f5f0e6;   /* 页面背景 —— 陈年宣纸色 */
--paper-dark:   #ede5d8;   /* 微对比区域 */
--vermilion:    #b83a2e;   /* 强调：篇章节号、激活状态、链接 —— 中国红 */
--gold:         #a67c52;   /* 强调：拼音注音（ruby）、装饰元素 —— 古金色 */
--gold-light:   #c9a87c;   /* 悬停状态浅金 */
--muted:        #8a7a68;   /* 占位符、禁用态、元信息文字 */
--border:       #d4c9b8;   /* 分割线、卡片边框 */
--border-light: #e8dfd0;   /* 内部分割线 */
```

**功能定义：**
- `paper` — 页面背景、阅读区底色
- `ink` — 正文、原文区块所有文字
- `vermilion` — 交互元素、激活态、篇章节号、重点高亮
- `gold` — 拼音 ruby 文字、装饰点缀
- `muted` — 占位文字、时间戳、禁用状态
- `border` — 结构分割线、卡片边缘

---

## 3. 字体层级

**展示 / 标题字体：**
```
font-family: "ZCOOL XiaoWei", "STSong", serif;
font-weight: 400;
```
适用范围：Hero 标题、浮动导航篇章节标题、段落序号、核心引文。

**正文字体：**
```
font-family: "Noto Serif SC", "STSong", serif;
font-weight: 400;
```
适用范围：古典中文原文、注释、注解、所有正文。

**Google Fonts 引入：**
```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600&family=ZCOOL+XiaoWei&display=swap" rel="stylesheet">
```

**字号规范：**
- Hero 标题：3.6rem，ZCOOL XiaoWei
- Hero 副标题：1.1rem，Noto Serif SC
- 段落序号：0.65rem，ZCOOL XiaoWei，朱砂色
- 原文（orig）：1.15rem，Noto Serif SC，行高 2.2
- 注释（note）：0.95rem，Noto Serif SC
- 拼音 ruby：0.48em，金色，字符下方居中

---

## 4. 组件样式

### 按钮（拼音切换、音频朗读）

```css
/* 胶囊形状，描边，透明背景 */
padding: 6px 14px;
border: 1px solid var(--border);
border-radius: 20px;
background: transparent;
color: var(--muted);
font-family: "Noto Serif SC", serif;
font-size: 0.72rem;
letter-spacing: 0.1em;
cursor: pointer;
transition: color 0.2s, border-color 0.2s, background 0.2s;
```

**状态：**
- 默认：`color: var(--muted)`，`border: var(--border)`
- 悬停：`color: var(--vermilion)`，`border-color: var(--vermilion)`，背景微晕
- 激活 / 播放中：`color: var(--vermilion)`，`border-color: var(--vermilion)`，背景微晕
- 禁用（音频未生成）：`opacity: 0.35`，`pointer-events: none`，title 显示"音频未生成"

### 文章区块（双栏布局）

**布局：** CSS Grid，`1fr 1fr` 双栏，间距 48px。移动端：单栏，注释在原文下方。

**左栏（orig-col）：**
- 背景：透明
- 每个 `.orig-block` 左侧留出段落序号位置（朱砂色 0.65rem ZCOOL XiaoWei）
- 激活状态（音频播放中或滚动监听）：`background: rgba(184,58,46,0.04)`，左侧朱砂色 2px 边框

**右栏（note-col）：**
- 背景：`var(--paper-dark)`，左侧 1px `var(--border-light)` 描边
- `.note-block` 激活状态：左侧朱砂色 3px 边框，背景微晕

### Hero 区域

- 高度：72vh
- 背景：AI 生成水墨画（通过 JS 设置为 `.hero` 的 `background-image`）
- 渐变叠加层：顶部 `linear-gradient(to bottom, var(--vermilion), transparent)`；底部 `linear-gradient(to top, rgba(26,18,8,0.85), transparent)`
- 标题（`.hero-title`）：ZCOOL XiaoWei，3.6rem，白色带文字阴影，居中
- 副标题（`.hero-subtitle`）：Noto Serif SC，1.1rem，暗金色，标题下方
- 标签（`.hero-label`）：0.7rem，朱砂色，letter-spacing 0.3em

### 浮动导航面板

- 位置：固定，右侧，垂直居中
- 最大宽度：200px
- 背景：`var(--paper)`，`1px solid var(--border)`，柔和阴影
- 篇章节标题：ZCOOL XiaoWei，0.7rem，朱砂色，letter-spacing 0.2em
- 导航链接：Noto Serif SC，0.8rem，`color: var(--ink-light)`
- 当前激活链接：朱砂色
- 内容溢出：auto，最大高度 70vh，自定义滚动条

### 音频播放器（工具栏内嵌）

- 进度条：`var(--border)` 轨道，`var(--vermilion)` 填充，3px 高
- 时间标签：0.7rem，暗色，`min-width: 80px`
- 停止按钮：10px 图标，暗色，悬停变朱砂色

### 核心引文（Blockquote）

- 左边框：`3px solid var(--vermilion)`
- 左内边距：24px
- 上下外边距：40px 0
- 字体：ZCOOL XiaoWei
- 字号：1.2rem
- 颜色：`var(--ink-light)`

### 侧边装饰线

阅读区左侧边缘的垂直细线：
```css
.side-rule {
  position: fixed;
  left: 28px;
  top: 0;
  bottom: 0;
  width: 1px;
  background: linear-gradient(
    to bottom,
    transparent 0%,
    var(--border-light) 15%,
    var(--border) 50%,
    var(--border-light) 85%,
    transparent 100%
  );
  pointer-events: none;
  z-index: 0;
}
```

---

## 5. 布局原则

**页面结构：**
```
[返回目录链接 — 固定左上]
[侧边装饰线 — 固定左边缘]
[Hero — 72vh，水墨背景，渐变叠加，标题居中]
[隐藏图片加载器 — 通过 onload 触发 Hero 背景]
[阅读区 — 最大宽度 1100px，居中，双栏 Grid]
  [工具栏 — 拼音切换 + 音频控制，右对齐]
  [原文栏 — 古典文本段落]
  [注释栏 — 注解，paper-dark 背景]
  [对比表格 — 如有]
[页脚 — 居中，暗色]
[浮动导航 — 固定右侧，垂直居中]
```

**双栏 Grid：**
```css
.reading-area {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  max-width: 1100px;
  margin: 0 auto;
  padding: 40px 48px 80px;
}
```

**响应式断点：**
- `max-width: 680px`：单栏，缩小内边距，隐藏浮动导航

---

## 6. 阴影系统

- 浮动导航：`0 4px 24px rgba(26,18,8,0.08)`
- Hero 渐变叠加：多层 `linear-gradient`（不使用 box-shadow）
- 按钮悬停：不改变阴影，仅切换颜色
- 区块激活：不使用阴影，仅改变颜色和边框

---

## 7. 设计守则

**宜：**
- 所有展示文字（标题、序号、篇章节标签）使用 ZCOOL XiaoWei
- 所有阅读文字（古典中文、注释）使用 Noto Serif SC
- 阅读区全程保持纸色背景
- 朱砂色仅用于：激活状态、篇章节号、重点高亮
- 金色仅用于：拼音 ruby 文字
- 保持充裕行高（2.2）以确保古典中文可读性
- 水墨画作为氛围背景使用，不作为平面插图

**忌：**
- 禁止使用 Inter、Roboto、Arial、系统字体
- 禁止在朱砂/金色以外使用高饱和颜色
- 禁止为文字元素添加投影
- 禁止在阅读区使用渐变背景（只用纸色）
- 禁止将阅读区最大宽度压缩至 1100px 以下
- 禁止在结构元素上使用超过 2px 的边框
- 禁止在 Hero 下方展示重复的配图

---

## 8. 响应式行为

| 断点 | 布局 | 浮动导航 | 侧边装饰线 |
|---|---|---|---|
| > 680px | 双栏 Grid | 显示 | 显示 |
| ≤ 680px | 单栏 | 隐藏 | 隐藏 |

移动端：原文栏在上，注释栏在下。Hero 标题缩小字号。工具栏保留右上位置。

---

## 9. Agent 使用指南

对项目进行设计决策或修改时，可参考以下提示词：

**添加新文章：**
> "按照现有结构添加一篇新的庄子章节。Hero 标题使用 ZCOOL XiaoWei，正文使用 Noto Serif SC。Hero 背景使用 MiniMax image-01 API 生成水墨画。"

**提升可读性：**
> "将原文段落的行高提升至 2.4，并确保注释栏与纸色背景之间有足够对比。朱砂色仅用于激活/高亮状态。"

**新增 UI 元素：**
> "新按钮需遵循现有胶囊样式：透明背景、1px 描边、圆角 20px。悬停状态使用朱砂色。字体使用 Noto Serif SC，字号 0.72rem。"

**修改配色方案：**
> "当前色板为 ink/paper/vermilion/gold。修改时需保持东亚古典书斋美学——禁止蓝紫色渐变，禁止现代 SaaS 风格。"

**添加动画：**
> "新动画应为淡入上浮效果（opacity 0→1，translateY 20px→0，0.5s ease）。避免弹跳或活泼动画——整体氛围是沉静的。"

---

## 10. 文件清单

| 文件 | 用途 |
|---|---|
| `index.html` | 首页，卡片网格导航 |
| `article.html` | 单文章模板，通过 `?id=` 参数加载 JSON |
| `data/*.json` | 文章内容（段落、对比、元数据） |
| `audio/*.mp3` | 预生成的 TTS 音频文件 |
| `images/*.png` | AI 生成的水墨风格配图 |
| `source_code/nav.css` | 所有样式——设计系统核心 |
| `source_code/nav.js` | 浮动导航 HTML 注入 |
| `source_code/add_pinyin.py` | 生成 pinyin/ruby/pinyinSentences 字段 |
| `source_code/generate_all_audio.py` | 批量 TTS 音频生成 |
| `source_code/generate_all_images.py` | 批量配图生成 |
| `source_code/test_article.py` | pytest 测试套件 |
| `design-refs/` | VoltAgent 设计参考库（全局目录，不在项目内） |
