# DESIGN.md — 齐物论 (Zhesi)

A static HTML site presenting classical Chinese philosophical texts (Zhuangzi 庄子 and Daoist classics) with an authentic traditional East Asian aesthetic. No build system, no dependencies — pure HTML/CSS/JS served as static files.

---

## 1. Visual Theme & Atmosphere

**Aesthetic:** Classical Chinese ink wash painting (水墨画) meets scholarly parchment. The page should feel like reading an ancient scroll in a quiet library — warm paper tones, dark ink text, vermilion and gold accents that evoke carved seals and gilded marginalia.

**Mood:** Contemplative, refined, timeless. Not minimalist for the sake of modernism, but minimal in the way a well-used book is minimal: every element earns its place.

**Key differentiators:**
- Hero sections use AI-generated classical ink wash paintings as atmospheric backgrounds
- Two-column layout (原文 / 注释) mirrors the scholarly tradition of annotated classical texts
- Scroll spy highlights the currently-read passage in vermilion, creating a reading experience that feels guided

---

## 2. Color Palette

```css
--ink:          #1a1208;   /* Primary text, headings — deep ink black */
--ink-light:    #4a3f2f;   /* Secondary text, subtitles */
--paper:        #f5f0e6;   /* Page background — aged parchment */
--paper-dark:   #ede5d8;   /* Subtle contrast areas */
--vermilion:    #b83a2e;   /* Accent: section numbers, active states, links — Chinese red */
--gold:         #a67c52;   /* Accent: pinyin ruby text, decorative elements — aged gold */
--gold-light:   #c9a87c;   /* Lighter gold for hover states */
--muted:        #8a7a68;   /* Placeholder, disabled, meta text */
--border:       #d4c9b8;   /* Dividers, card borders */
--border-light: #e8dfd0;   /* Subtle inner borders */
```

**Functional roles:**
- `paper` — page background, reading area
- `ink` — all body text, original text blocks
- `vermilion` — interactive elements, active states, section numbers, key highlights
- `gold` — pinyin annotations (ruby text), decorative accents
- `muted` — placeholder text, timestamps, disabled states
- `border` — structural dividers, card edges

---

## 3. Typography

**Display / Headings:**
```
font-family: "ZCOOL XiaoWei", "STSong", serif;
font-weight: 400;
```
Used for: hero titles, section headers in float-nav, block numbers, blockquotes.

**Body / Reading:**
```
font-family: "Noto Serif SC", "STSong", serif;
font-weight: 400;
```
Used for: original classical Chinese text, annotations, notes, all prose.

**Google Fonts import:**
```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600&family=ZCOOL+XiaoWei&display=swap" rel="stylesheet">
```

**Scale:**
- Hero title: 3.6rem, ZCOOL XiaoWei
- Hero subtitle: 1.1rem, Noto Serif SC
- Block number: 0.65rem, ZCOOL XiaoWei, vermilion
- Original text (orig): 1.15rem, Noto Serif SC, line-height 2.2
- Annotation (note): 0.95rem, Noto Serif SC
- Pinyin ruby: 0.48em, gold color, centered below character

---

## 4. Component Styling

### Buttons (Pinyin Toggle, Audio Toggle)

```css
/* Container: pill-shaped, border, transparent background */
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

**States:**
- Default: `color: var(--muted)`, `border: var(--border)`
- Hover: `color: var(--vermilion)`, `border-color: var(--vermilion)`, background tint
- Active / Playing: `color: var(--vermilion)`, `border-color: var(--vermilion)`, background tint
- Disabled (audio unavailable): `opacity: 0.35`, `pointer-events: none`, title shows "音频未生成"

### Article Blocks (Two-Column)

**Layout:** CSS Grid, `1fr 1fr` columns, 48px gap. On mobile: single column, notes below original.

**Left column (orig-col):**
- Background: transparent
- Each `.orig-block` has left padding for block number (rendered as vermilion 0.65rem ZCOOL XiaoWei)
- Active state (during audio playback or scroll spy): `background: rgba(184,58,46,0.04)`, vermilion left border `2px solid var(--vermilion)`

**Right column (note-col):**
- Background: `var(--paper-dark)` with left border `1px solid var(--border-light)`
- `.note-block` active state: vermilion left border `3px solid var(--vermilion)`, background tint

### Hero Section

- Height: 72vh
- Background: AI-generated ink wash painting (set via JS as `background-image` on `.hero`)
- Gradient overlay: `linear-gradient(to bottom, var(--vermilion), transparent)` at top; `linear-gradient(to top, rgba(26,18,8,0.85), transparent)` at bottom
- Title (`.hero-title`): ZCOOL XiaoWei, 3.6rem, white with text-shadow, centered
- Subtitle (`.hero-subtitle`): Noto Serif SC, 1.1rem, muted gold, below title
- Label (`.hero-label`): 0.7rem, vermilion, letter-spacing 0.3em, uppercase

### Float-Nav Panel

- Position: fixed, right side, vertically centered
- Width: 200px max
- Background: `var(--paper)` with `1px solid var(--border)`, subtle shadow
- Section headers: ZCOOL XiaoWei, 0.7rem, vermilion, letter-spacing 0.2em
- Nav links: Noto Serif SC, 0.8rem, `color: var(--ink-light)`
- Active link: vermilion color
- Overflow: auto, max-height 70vh, custom scrollbar

### Audio Player (Inline Toolbar)

- Progress bar: `var(--border)` track, `var(--vermilion)` fill, 3px height
- Time label: 0.7rem, muted, `min-width: 80px`
- Stop button: 10px icon, muted, hover turns vermilion

### Blockquote (Core Quote)

- `border-left: 3px solid var(--vermilion)`
- `padding-left: 24px`
- `margin: 40px 0`
- `font-family: ZCOOL XiaoWei`
- `font-size: 1.2rem`
- Color: `var(--ink-light)`

### Side Decoration

Vertical rule on the left edge of reading area:
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

## 5. Layout Principles

**Page structure:**
```
[Back to Index link — fixed top left]
[Side rule decoration — fixed left edge]
[Hero — 72vh, ink wash bg, gradient overlay, title centered]
[Hidden img loader — triggers hero bg via onload]
[Reading Area — max-width 1100px, centered, two-column grid]
  [Toolbar — pinyin toggle + audio controls, right-aligned]
  [Orig column — classical text blocks]
  [Note column — annotations, paper-dark bg]
  [Comparison table — if present]
[Footer — centered, muted]
[Float-nav — fixed right side, vertically centered]
```

**Two-column grid:**
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

**Responsive breakpoints:**
- `max-width: 680px`: single column, reduced padding, float-nav hidden

---

## 6. Shadow System

- Float-nav: `0 4px 24px rgba(26,18,8,0.08)`
- Hero gradient overlays: layered `linear-gradient` (no box-shadow)
- Button hover: no shadow change, just color transition
- Block active: no shadow, color/border change only

---

## 7. Design Do's and Don'ts

**Do:**
- Use ZCOOL XiaoWei for all display text (titles, numbers, section labels)
- Use Noto Serif SC for all reading text (classical Chinese, annotations)
- Keep the paper background throughout the reading area
- Use vermilion sparingly: active states, section numbers, key highlights
- Use gold only for pinyin ruby text
- Maintain generous line-height (2.2) for classical Chinese readability
- Show ink wash paintings as atmospheric hero backgrounds, never as flat illustrations

**Don't:**
- Don't use Inter, Roboto, Arial, or system fonts
- Don't use bright or saturated colors beyond vermilion/gold on paper
- Don't add drop shadows to text elements
- Don't use gradient backgrounds on the reading area (paper only)
- Don't make the reading area narrower than 1100px max-width
- Don't use more than 2px border on structural elements
- Don't show duplicate illustrations below the hero

---

## 8. Responsive Behavior

| Breakpoint | Layout | Float-nav | Side-rule |
|---|---|---|---|
| > 680px | Two-column grid | Visible | Visible |
| ≤ 680px | Single column | Hidden | Hidden |

Mobile: orig column above, note column below. Hero title scales down. Toolbar remains top-right.

---

## 9. Agent Prompt Guide

When making design decisions or edits to this project, use prompts like:

**Adding a new article:**
> "Add a new Zhuangzi chapter following the existing structure. Use ZCOOL XiaoWei for the hero title, Noto Serif SC for body text. The hero background should be an ink wash painting generated via MiniMax image-01 API."

**Improving readability:**
> "Increase the line-height of the original text blocks to 2.4 and ensure the note column has enough contrast against the paper background. Use vermilion only for active/highlighted states."

**Adding a new UI element:**
> "Any new buttons should follow the existing pill-shaped style: transparent background, 1px border, rounded 20px. Hover states should use vermilion. Use Noto Serif SC at 0.72rem."

**Changing color scheme:**
> "The current palette uses ink/paper/vermilion/gold. Any changes should maintain the classical East Asian scholarly aesthetic — no blue/purple gradients, no modern SaaS aesthetics."

**Adding animations:**
> "New animations should be subtle fade-up reveals (opacity 0→1, translateY 20px→0, 0.5s ease). Avoid bouncy or playful animations — the mood is contemplative."

---

## 10. File Inventory

| File | Purpose |
|---|---|
| `index.html` | Home page with card grid navigation |
| `article.html` | Single article template, loads JSON by `?id=` param |
| `data/*.json` | Article content (blocks, comparison, metadata) |
| `audio/*.mp3` | Pre-generated TTS audio files |
| `images/*.png` | AI-generated ink wash hero illustrations |
| `source_code/nav.css` | All styles — design system lives here |
| `source_code/nav.js` | Float-nav HTML injection |
| `source_code/add_pinyin.py` | Generates pinyin/ruby/pinyinSentences fields |
| `source_code/generate_all_audio.py` | Batch TTS audio generation |
| `source_code/generate_all_images.py` | Batch image generation |
| `source_code/test_article.py` | pytest test suite |
| `design-refs/` | VoltAgent design reference library (global, not in repo) |
