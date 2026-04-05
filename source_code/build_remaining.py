import os

base = os.path.expanduser("~/.openclaw/workspace/zhesi")
daojia_dir = os.path.join(base, "daojia")
os.makedirs(daojia_dir, exist_ok=True)

# Read an existing file as template
template_path = os.path.join(base, "xiaoyao-you.html")
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

# Extract just the CSS/head part for reuse
# We'll use the exact same HTML structure

def make_page(title, subtitle, label, orig_blocks, note_blocks, core_quote, summary_rows, filename, bg_char=""):
    """Create a page from structured data."""
    # orig_blocks: list of (num, text)
    # note_blocks: list of (num, text)
    # summary_rows: list of (label, col1, col2)

    orig_html = ""
    for num, text in orig_blocks:
        orig_html += f'''
        <div class="orig-block" data-reveal>
          <div class="orig-block-num">{num}</div>
          <div class="orig-block-text">{text}</div>
        </div>'''

    note_html = ""
    for num, text in note_blocks:
        note_html += f'''
        <div class="note-block" data-reveal>
          <div class="note-block-num">{num}</div>
          <div class="note-block-text">{text}</div>
        </div>'''

    summary_html = ""
    for row in summary_rows:
        summary_html += f'''<tr>
          <td class="row-label">{row[0]}</td>
          <td>{row[1]}</td>
          <td>{row[2]}</td>
        </tr>'''

    page = template.replace(">逍遥游<", f">{title}<").replace("内篇 ·", f"{label} ·").replace("小大虽殊，而放於自得之場，则物任其性，事称其能，各當其分，逍遙一也，豈容勝負於其間哉！", core_quote)

    # More precise replacements
    page = template  # reset

    hero_label = label
    hero_title = title
    hero_sub = subtitle
    hero_quote_p1 = core_quote.split('；')[0] if '；' in core_quote else core_quote
    hero_quote_p2 = '；'.join(core_quote.split('；')[1:]) if '；' in core_quote else ''

    # Actually build from scratch using string replacement on a base template
    # We need to rebuild since template varies too much

    with open(template_path, 'r', encoding='utf-8') as f:
        base_html = f.read()

    # Replace hero
    base_html = base_html.replace('>逍遥游<', f'>{title}<')
    base_html = base_html.replace('内篇 ·', f'{label} ·')
    base_html = base_html.replace('小大虽殊，而放於自得之場，则物任其性，事称其能，各當其分，逍遙一也，豈容勝負於其間哉！',
                                  f'{hero_sub}')

    # Replace bg char
    if bg_char:
        base_html = base_html.replace('>逍<', f'>{bg_char}<')

    # Build orig column
    orig_col = ""
    for num, text in orig_blocks:
        orig_col += f'''
        <div class="orig-block" data-reveal>
          <div class="orig-block-num">{num}</div>
          <div class="orig-block-text">{text}</div>
        </div>'''

    note_col = ""
    for num, text in note_blocks:
        note_col += f'''
        <div class="note-block" data-reveal>
          <div class="note-block-num">{num}</div>
          <div class="note-block-text"><p>{text}</p></div>
        </div>'''

    # Find and replace the orig-col and note-col in base_html
    import re
    # Replace orig blocks
    orig_pattern = r'<div class="orig-block"[^>]*>.*?</div>\s*</div>\s*(?=<div class="orig-block"|</div>\s*<footer)'
    note_pattern = r'<div class="note-block"[^>]*>.*?</div>\s*</div>\s*(?=<div class="note-block"|</div>\s*<footer)'

    # Simpler approach: rebuild the whole content area
    content_start = base_html.find('<div class="reading-area">')
    content_end = base_html.find('<footer>')
    reading_content = base_html[content_start:content_end]

    # Count how many orig-blocks and note-blocks in template
    orig_count = reading_content.count('class="orig-block"')
    note_count = reading_content.count('class="note-block"')

    # Replace by replacing individual blocks
    new_reading = reading_content
    for i, (num, text) in enumerate(orig_blocks):
        old = f'<div class="orig-block-num">{i+1}</div>'
        new = f'<div class="orig-block-num">{num}</div>'
        new_reading = new_reading.replace(old, new, 1)

    # Actually a simpler approach: just write the file directly using string building
    new_page = build_page(title, subtitle, label, orig_blocks, note_blocks, core_quote, summary_rows, bg_char, base_html)

    outpath = os.path.join(base if 'dao-de-jing' not in filename and 'wen-zi' not in filename and 'lie-zi' not in filename and 'huainan' not in filename and 'bao-pu' not in filename else daojia_dir, filename)
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(new_page)
    print(f"Wrote: {outpath}")

def build_page(title, subtitle, label, orig_blocks, note_blocks, core_quote, summary_rows, bg_char, base_html):
    """Build a complete page."""

    # Build the two columns
    left_blocks = ""
    for num, text in orig_blocks:
        left_blocks += f'''
        <div class="orig-block" data-reveal>
          <div class="orig-block-num">{num}</div>
          <div class="orig-block-text">{text}</div>
        </div>
'''

    right_blocks = ""
    for num, text in note_blocks:
        right_blocks += f'''
        <div class="note-block" data-reveal>
          <div class="note-block-num">{num}</div>
          <div class="note-block-text"><p>{text}</p></div>
        </div>
'''

    summary_html = ""
    for row in summary_rows:
        summary_html += f"<tr><td class=\"row-label\">{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"

    # Find the content area markers
    start_marker = '<div class="reading-area"'
    end_marker = '<footer>'

    si = base_html.find(start_marker)
    ei = base_html.find(end_marker)

    if si == -1 or ei == -1:
        # Try alternative markers from a simpler file
        with open(os.path.join(base, "qing-jing-jing.html"), 'r', encoding='utf-8') as f:
            simple_base = f.read()
        si = simple_base.find(start_marker)
        ei = simple_base.find(end_marker)
        if si != -1 and ei != -1:
            base_html = simple_base

    before = base_html[:si]
    after = base_html[ei:]

    new_reading_area = f'''
  <div class="reading-area">
    <div class="text-grid">

      <!-- 左侧：原文全文 -->
      <div class="orig-col">
{left_blocks}
        <div class="core-quote" data-reveal>
          <blockquote>{core_quote.replace('；', '<br>')}</blockquote>
          <cite>——{title}</cite>
        </div>

        <div class="comparison-section" data-reveal>
          <div class="comparison-label">对照</div>
          <table>
            <thead>
              <tr>
                <th style="width:90px;"></th>
                <th></th>
                <th></th>
              </tr>
            </thead>
            <tbody>
{summary_html}
            </tbody>
          </table>
        </div>
      </div>

      <!-- 右侧：注释 -->
      <div class="note-col">
        <div class="note-col-header">注释</div>
{right_blocks}
      </div>
    </div>
  </div>
'''

    new_page = before + new_reading_area + after

    # Update hero text
    new_page = new_page.replace('>逍遥游<', f'>{title}<')
    if '内篇 ·' in new_page:
        new_page = new_page.replace('内篇 ·', f'{label} ·')
    if bg_char:
        new_page = new_page.replace('>逍<', f'>{bg_char}<')

    # Update subtitle
    new_page = new_page.replace('小大虽殊，而放於自得之場，则物任其性，事称其能，各當其分，逍遙一也，豈容勝負於其間哉！', subtitle)

    return new_page


# ===================== PAGES =====================

pages = [

    # 1. 盗跖
    ("dao-zhi.html", "盗跖", "杂篇 ·", "杂篇", "战国·庄周",
     [
         ("一", "无足问于知和曰：'人卒未有不兴名就利者。'彼富则人归之，归则下之，下则贵之。夫见下贵者，所以长生、安体、乐意之道也。"),
         ("二", "今子独无意焉，知不足邪？意知而力不能行邪？故推正不忘邪？"),
         ("三", "夫以利合者，迫穷祸患害相弃也。以天属者，迫穷祸患害相收也。君子之交淡若水，小人之交甘若醴。"),
     ],
     [
         ("一", "知和指出：名利是人之所迫——富贵则人归附，归附则居人之下，以下为贵，这是长生的道路。"),
         ("二", "无足批评追求名利的人——知不足、力不行，却推说正道不忘，是自欺。"),
         ("三", "<strong>核心：</strong>以利合者，迫穷祸患相弃；以天属者，迫穷祸患相收。君子之交淡若水，小人之交甘若醴——真正的情谊以天性相连，不以利益驱动。"),
     ],
     "以利合者，迫穷祸患相弃；以天属者，迫穷祸患相收",
     [("性质", "以利相交", "以天属相交"), ("表现", "富贵时归附，穷困时相弃", "穷困时相收，利益时相合"), ("境界", "小人之交，甘以绝", "君子之交，淡以亲")],
     "盗"
    ),

    # 2. 天下
    ("tian-xia.html", "天下", "杂篇 ·", "杂篇", "战国·庄周",
     [
         ("一", "天下之治方术者多矣，皆以其有为不可加矣。古之所谓道术者，恶乎在？圣有所生，王有所成，皆原于一。"),
         ("二", "不离于宗，谓之天人。不离于精，谓之神人。不离于真，谓之至人。以天为宗，以德为本，以道为门，兆于变化，谓之圣人。"),
         ("三", "内圣外王之道，暗而不明，郁而不发，天下之人各为其所欲焉以自为方。"),
     ],
     [
         ("一", "天下治方术者众多，都认为自己的一套已登峰造极。古代的道术，却不如此——圣人有所生，王有所成，皆原于"道"之一。"),
         ("二", "<strong>四等人：</strong>天人（不离于宗）、神人（不离于精）、至人（不离于真）、圣人（以天为宗、以德为本、以道为门、兆于变化）。"),
         ("三", "<strong>内圣外王：</strong>中国古代政治哲学的最高理想——内有圣人之德，外施王者之政。庄子叹其暗而不明、郁而不发，天下人各自为方，各是其是。"),
     ],
     "内圣外王之道，暗而不明，郁而不发",
     [("理想", "内圣——道德修养", "外王——政治事功"), ("困境", "道术为天下裂", "各为其所欲，自以为是"), ("评价", "郁而不发", "天下之大，求一以贯之者寡")],
     "天"
    ),

    # 3. 道德经
    ("dao-de-jing.html", "道德经", "道家经典", "道家", "老子·李耳",
     [
         ("一", "道可道，非常道。名可名，非常名。无名，天地之始；有名，万物之母。故常无欲，以观其妙；常有欲，以观其徼。"),
         ("二", "天下皆知美之为美，斯恶已。皆知善之为善，斯不善已。故有无相生，难易相成，长短相形，高下相倾，音声相和，前后相随。"),
         ("三", "上善若水。水善利万物而不争，处众人之所恶，故几于道。"),
         ("四", "为学日益，为道日损。损之又损，以至于无为，无为而无不为。"),
         ("五", "小国寡民，使有什伯之器而不用，使民重死而不远徙。甘其食，美其服，安其居，乐其俗。邻国相望，鸡犬之声相闻，民至老死不相往来。"),
     ],
     [
         ("一", "<strong>道本体：</strong>可以用语言表述的道，就不是永恒的道。道的本体无形无名，是天地的起源、万物的根本。从"无欲"可观道之妙，从"有欲"可观道之徼。"),
         ("二", "<strong>相对性：</strong>天下皆知美为美，则丑已生；皆知善为善，则不善已立。有无、难易、长短、高下——一切对立都是相互成就的。"),
         ("三", "<strong>上善若水：</strong>最高的善就像水一样——水利万物却不争，停留在众人厌恶的地方（水往低处流），所以最接近道。"),
         ("四", "<strong>为道日损：</strong>求学每天有得，修道每天在减。减到极点，就是"无为"——无为反而无不为。"),
         ("五", "<strong>小国寡民：</strong>老子的理想社会——国小民少，兵器无用，民重死不远迁，自足其食、安其居、乐其俗，邻国相望却老死不相往来。"),
     ],
     "上善若水，水善利万物而不争",
     [("核心", "道法自然", "无为而治"), ("政治", "小国寡民", "鸡犬之声相闻，老死不相往来"), ("修养", "为道日损", "上善若水，不争几于道")],
     "道",
     "daojia"
    ),

    # 4. 文子
    ("wen-zi.html", "文子", "道家经典", "道家", "辛计然·文子",
     [
         ("一", "道者，万物之奥，善人之宝，不善人之所不保也。"),
         ("二", "圣人内求于己，不可得者，虽有过失，天地知之，知而不改者，天下非之。"),
         ("三", "故通于天者，顺于道以游世者；通于地者，顺于德以游物者。"),
     ],
     [
         ("一", "<strong>道为至宝：</strong>道是万物的深藏之处，善人珍惜它，不善的人也离不开它（虽暂失之，终不可保）。"),
         ("二", "<strong>反求于己：</strong>圣人内求于己——有过失天地知之，知而不改则天下非之。反省的力量来自内心，不是外在的惩罚。"),
         ("三", "<strong>通天顺道：</strong>通于天者，顺道以游世；通于地者，顺德以游物——人应与天地之道相通，而非与外物相争。"),
     ],
     "道者，万物之奥，善人之宝",
     [("本体", "道为万物之奥", "不可言传"), ("修养", "内求于己", "过失天地知之"), ("境界", "顺道以游世", "顺德以游物")],
     "道",
     "daojia"
    ),

    # 5. 列子
    ("lie-zi.html", "列子", "道家经典", "道家", "郑·列御寇",
     [
         ("一", "有生不生，有化不化。不生者能生生，不化者能化化。生者不能不生，化者不能不化，故常生常化。"),
         ("二", "夫言化者，皆有不生者也。有有者，言无者之所由生生也。有无之相生，其变乃大。"),
         ("三", "物物而不物于物，则胡可得而累邪？"),
     ],
     [
         ("一", "<strong>不生者能生生：</strong>能够生成万物者，本身是不被生的。"不生者"是本体，"生生者"是道的作用。"),
         ("二", "<strong>有无相生：</strong>有与无相互生成，有产生无，无产生有，变化是无穷的。"),
         ("三", "<strong>物物而不物于物：</strong>，主宰物而不被物所驱使、所束缚——人应做物的主人，而非物的奴仆。"),
     ],
     "物物而不物于物，则胡可得而累邪",
     [("本体", "不生者能生生", "不化者能化化"), ("变化", "有无相生", "其变乃大"), ("修养", "物物而不物于物", "不为外物所累")],
     "物",
     "daojia"
    ),

    # 6. 淮南子
    ("huainan-zi.html", "淮南子", "道家经典", "道家", "西汉·刘安",
     [
         ("一", "天气为魂，地气为魄， Geist 之守，体气乃通。"),
         ("二", "百川异源，而皆归于海。百家殊业，皆务于治。"),
         ("三", "圣人内修道术，不外饰仁义，而民自化。"),
     ],
     [
         ("一", "<strong>魂魄与体气：</strong>天气为魂，地气为魄， Geist 守住，体气乃通——人的精神与形体相合，生命才完整。"),
         ("二", "<strong>百川归海：</strong>百川源头各异，终归于海；百家事业不同，皆务于治——表面分歧，终点一致，归于大道。"),
         ("三", "<strong>内圣而化：</strong>圣人在内心修道术，不在外在装饰仁义，而民众自然被感化——无为而化，是最深的治理。"),
     ],
     "百川异源，而皆归于海；百家殊业，皆务于治",
     [("宇宙", "天气为魂，地气为魄", " Geist 守则体气通"), ("政治", "内修道术", "民自化"), ("哲学", "百川归海", "百家殊业，归于一道")],
     "海",
     "daojia"
    ),

    # 7. 抱朴子
    ("bao-pu-zi.html", "抱朴子", "道家经典", "道家", "东晋·葛洪",
     [
         ("一", "玄者，自然之始祖，而万殊之大宗也。"),
         ("二", "得之者贵，不待黄钺之威；生之者富，不需天禄之赏。"),
         ("三", "欲求仙者，要当以忠孝和顺仁信为本。"),
     ],
     [
         ("一", "<strong>玄为大宗：</strong>玄是自然的始祖、万殊的大宗——宇宙本体是"玄"，道家修仙即回归于玄。"),
         ("二", "<strong>仙道贵生：</strong>得玄道者富贵，不待威势；养生者富足，不需天禄——仙道贵生，生命超越凡俗的限制。"),
         ("三", "<strong>仙道与世法：</strong>修仙者以忠孝和顺仁信为本——道教修炼并不离世间法，而是以人间德行为根基。"),
     ],
     "玄者，自然之始祖，而万殊之大宗",
     [("本体", "玄为自然之祖", "万殊之大宗"), ("目标", "贵生", "不待威势天禄"), ("修养", "以忠孝仁信为本", "仙道不离世法")],
     "玄",
     "daojia"
    ),
]

# Read base template
base_template_path = os.path.join(base, "xiaoyao-you.html")
with open(base_template_path, 'r', encoding='utf-8') as f:
    base_template = f.read()

# Read simpler template for daojia
simple_template_path = os.path.join(daojia_dir, "qing-jing-jing.html")
if os.path.exists(simple_template_path):
    with open(simple_template_path, 'r', encoding='utf-8') as f:
        daojia_template = f.read()
else:
    daojia_template = base_template

for page_data in pages:
    filename, title, label, category, author, orig_blocks, note_blocks, core_quote, summary_rows, bg_char = page_data
    target_dir = daojia_dir if category == "道家" else base
    target_template = daojia_template if category == "道家" else base_template

    # Build page using the target template
    left = ""
    for num, text in orig_blocks:
        left += f'<div class="orig-block" data-reveal><div class="orig-block-num">{num}</div><div class="orig-block-text">{text}</div></div>\n'

    right = ""
    for num, text in note_blocks:
        right += f'<div class="note-block" data-reveal><div class="note-block-num">{num}</div><div class="note-block-text"><p>{text}</p></div></div>\n'

    summary = ""
    for row in summary_rows:
        summary += f"<tr><td class=\"row-label\">{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"

    # Use the simpler daojia template if available
    tpl = daojia_template if category == "道家" else base_template

    # Replace reading area
    si = tpl.find('<div class="reading-area"')
    ei = tpl.find('<footer>')
    if si == -1:
        si = tpl.find('<div class="text-grid"')
        if si != -1:
            si2 = si
            # find start of reading area
            tmp = tpl[:si]
            si = tmp.rfind('<section')
        else:
            si = 0

    # Actually just rebuild the whole thing
    new_content = f'''
  <div class="reading-area">
    <div class="text-grid">
      <div class="orig-col">
{left}
        <div class="core-quote" data-reveal>
          <blockquote>{core_quote.replace('，', '<br>').replace('；', '<br>')}</blockquote>
          <cite>——{title}</cite>
        </div>
        <div class="comparison-section" data-reveal>
          <div class="comparison-label">对照</div>
          <table>
            <thead><tr><th style="width:90px;"></th><th></th><th></th></tr></thead>
            <tbody>{summary}</tbody>
          </table>
        </div>
      </div>
      <div class="note-col">
        <div class="note-col-header">注释</div>
{right}
      </div>
    </div>
  </div>
'''

    if ei > si > 0:
        new_page = tpl[:si] + new_content + tpl[ei:]
    else:
        new_page = tpl

    # Update hero
    new_page = new_page.replace('>逍遥游<', f'>{title}<')
    new_page = new_page.replace('内篇 ·', f'{label} ·')
    if bg_char:
        new_page = new_page.replace('>逍<', f'>{bg_char}<')

    outpath = os.path.join(target_dir, filename)
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(new_page)
    print(f"Wrote: {outpath}")

print("\nAll pages created!")
