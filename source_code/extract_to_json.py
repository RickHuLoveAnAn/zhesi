#!/usr/bin/env python3
"""从 HTML 文件和 build_remaining.py 提取文章数据为 JSON"""

import os
import re
import json
from pathlib import Path

BASE = Path('/Users/rick/.openclaw/workspace/zhesi')
DATA_DIR = BASE / 'data'
DATA_DIR.mkdir(exist_ok=True)

DAOJIA_FILES = {
    'qing-jing-jing', 'taiyi-jinhua', 'dao-de-jing',
    'wen-zi', 'lie-zi', 'huainan-zi', 'bao-pu-zi'
}

ZHUANGZI_INNER = {'xiaoyao-you', 'qi-wu-lun', 'yang-sheng-zhu', 'ren-jian-shi',
                   'de-chong-fu', 'da-zong-shi', 'ying-di-wang'}
ZHUANGZI_OUTER = {'pian-mu', 'ma-ti', 'qu-qie', 'zai-you', 'tian-di', 'tian-dao',
                   'tian-yun', 'ke-yi', 'shan-xing', 'qiu-shui', 'zhi-le', 'da-sheng',
                   'shan-mu', 'tian-zi-fang', 'zhi-bei-you'}
ZHUANGZI_MISC = {'geng-sang-chu', 'xu-wu-gui', 'ze-yang', 'wai-wu', 'yu-yan',
                  'rang-wang', 'dao-zhi', 'shuo-jian', 'yu-fu', 'lie-yu-kou', 'tian-xia'}

SECTION_MAP = {
    'xiaoyao-you': ('内篇', '内篇 · 第一'),
    'qi-wu-lun': ('内篇', '内篇 · 第二'),
    'yang-sheng-zhu': ('内篇', '内篇 · 第三'),
    'ren-jian-shi': ('内篇', '内篇 · 第四'),
    'de-chong-fu': ('内篇', '内篇 · 第五'),
    'da-zong-shi': ('内篇', '内篇 · 第六'),
    'ying-di-wang': ('内篇', '内篇 · 第七'),
}

AUTHORS = {
    'xiaoyao-you': '战国·庄周', 'qi-wu-lun': '战国·庄周',
    'yang-sheng-zhu': '战国·庄周', 'ren-jian-shi': '战国·庄周',
    'de-chong-fu': '战国·庄周', 'da-zong-shi': '战国·庄周',
    'ying-di-wang': '战国·庄周',
    'pian-mu': '战国·庄周', 'ma-ti': '战国·庄周', 'qu-qie': '战国·庄周',
    'zai-you': '战国·庄周', 'tian-di': '战国·庄周', 'tian-dao': '战国·庄周',
    'tian-yun': '战国·庄周', 'ke-yi': '战国·庄周', 'shan-xing': '战国·庄周',
    'qiu-shui': '战国·庄周', 'zhi-le': '战国·庄周', 'da-sheng': '战国·庄周',
    'shan-mu': '战国·庄周', 'tian-zi-fang': '战国·庄周', 'zhi-bei-you': '战国·庄周',
    'geng-sang-chu': '战国·庄周', 'xu-wu-gui': '战国·庄周', 'ze-yang': '战国·庄周',
    'wai-wu': '战国·庄周', 'yu-yan': '战国·庄周', 'rang-wang': '战国·庄周',
    'dao-zhi': '战国·庄周', 'shuo-jian': '战国·庄周', 'yu-fu': '战国·庄周',
    'lie-yu-kou': '战国·庄周', 'tian-xia': '战国·庄周',
    'qing-jing-jing': '道家经典',
    'taiyi-jinhua': '道家经典',
    'dao-de-jing': '老子·李耳',
    'wen-zi': '辛计然·文子',
    'lie-zi': '郑·列御寇',
    'huainan-zi': '西汉·刘安',
    'bao-pu-zi': '东晋·葛洪',
}

def get_section(file_id):
    if file_id in ZHUANGZI_INNER:
        num = list(ZHUANGZI_INNER).index(file_id) + 1
        return ('内篇', f'内篇 · 第{num}')
    if file_id in ZHUANGZI_OUTER:
        num = list(ZHUANGZI_OUTER).index(file_id) + 1
        return ('外篇', f'外篇 · 第{num}')
    if file_id in ZHUANGZI_MISC:
        num = list(ZHUANGZI_MISC).index(file_id) + 1
        return ('杂篇', f'杂篇 · 第{num}')
    if file_id in DAOJIA_FILES:
        return ('道家', '道家经典')
    return ('未知', '未知')


def extract_from_html(filepath):
    content = filepath.read_text(encoding='utf-8')
    file_id = filepath.name.replace('.html', '')
    is_daojia = '/daojia/' in str(filepath) or file_id in DAOJIA_FILES

    # title
    m = re.search(r'<title>([^<]+)</title>', content)
    title = m.group(1).replace('庄子·', '') if m else '未知'

    # hero-label
    m = re.search(r'<div class="hero-label">([^<]+)</div>', content)
    label = m.group(1) if m else ''

    # hero-subtitle
    m = re.search(r'<div class="hero-subtitle">([^<]+)</div>', content)
    subtitle = m.group(1) if m else ''

    # bgChar
    m = re.search(r"\.hero::after\s*\{[^}]*content:\s*'([^']+)'", content)
    bg_char = m.group(1) if m else ''

    # core-quote
    m = re.search(r'<blockquote>(.*?)</blockquote>', content, re.DOTALL)
    core_quote = ''
    if m:
        raw = m.group(1)
        raw = re.sub(r'<br\s*/?>', '<br>', raw)
        raw = re.sub(r'<[^>]+>', '', raw)
        raw = re.sub(r'[\r\n]+\s*', '<br>', raw)
        raw = re.sub(r'(<br>)+', '<br>', raw)
        core_quote = raw.strip().strip('<br>').rstrip('；')

    # orig blocks
    blocks = []
    orig_texts = re.findall(r'<div class="orig-block-text">([\s\S]*?)</div>', content)
    orig_nums = re.findall(r'<div class="orig-block-num">([^<]+)</div>', content)

    # note blocks
    note_texts = re.findall(r'<div class="note-block-text">([\s\S]*?)</div>', content)
    note_nums = re.findall(r'<div class="note-block-num">([^<]+)</div>', content)

    def _clean(html):
        """Extract text from HTML, converting newlines to <br>"""
        if not html:
            return ''
        text = html.strip()
        # Convert paragraph breaks to <br>
        text = re.sub(r'<p[^>]*>(.*?)</p>', r'\1<br>', text, flags=re.DOTALL)
        # Remove remaining HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Convert actual newlines to <br> and strip trailing whitespace
        text = re.sub(r'[\r\n]+\s*', '<br>', text)
        # Collapse multiple <br>
        text = re.sub(r'(<br>)+', '<br>', text)
        return text.strip().strip('<br>').rstrip('；')

    for i, num in enumerate(orig_nums):
        text = orig_texts[i] if i < len(orig_texts) else ''
        text = _clean(text)
        blocks.append({'num': num.strip(), 'orig': text, 'note': ''})

    for i, num in enumerate(note_nums):
        if i < len(blocks):
            note_html = note_texts[i] if i < len(note_texts) else ''
            blocks[i]['note'] = _clean(note_html)

    # comparison rows
    comparison = []
    row_labels = re.findall(r'<td class="row-label">([^<]+)</td>', content)
    left_cols = re.findall(r'<td class="row-label">[^<]+</td>\s*<td>([^<]+)</td>', content)
    # find right cols by finding td after left td
    all_tds = re.findall(r'<td>([^<]+)</td>', content)
    # simpler: just match row tr elements
    rows = re.findall(r'<tr>([\s\S]*?)</tr>', content)
    for row in rows:
        label_m = re.search(r'<td class="row-label">([^<]+)</td>', row)
        tds = re.findall(r'<td>([^<]+)</td>', row)
        if label_m and len(tds) >= 2:
            comparison.append({
                'label': label_m.group(1).strip(),
                'left': tds[0].strip(),
                'right': tds[1].strip()
            })

    section, section_label = get_section(file_id)

    return {
        'id': file_id,
        'filename': f'{file_id}.html',
        'title': title,
        'label': label or section_label,
        'section': section,
        'author': AUTHORS.get(file_id, '未知'),
        'bgChar': bg_char,
        'subtitle': subtitle,
        'isDaoJia': is_daojia,
        'coreQuote': core_quote,
        'blocks': blocks,
        'comparison': comparison
    }


def extract_from_build_remaining():
    """From build_remaining.py pages list"""
    pages_data = [
        {
            'id': 'dao-zhi',
            'filename': 'dao-zhi.html',
            'title': '盗跖',
            'section': '杂篇',
            'label': '杂篇 ·',
            'author': '战国·庄周',
            'bgChar': '盗',
            'isDaoJia': False,
            'coreQuote': '以利合者，迫穷祸患相弃；以天属者，迫穷祸患相收',
            'blocks': [
                {'num': '一', 'orig': '无足问于知和曰：\'人卒未有不兴名就利者。\'彼富则人归之，归则下之，下则贵之。夫见下贵者，所以长生、安体、乐意之道也。', 'note': '知和指出：名利是人之所迫——富贵则人归附，归附则居人之下，以下为贵，这是长生的道路。'},
                {'num': '二', 'orig': '今子独无意焉，知不足邪？意知而力不能行邪？故推正不忘邪？', 'note': '无足批评追求名利的人——知不足、力不行，却推说正道不忘，是自欺。'},
                {'num': '三', 'orig': '夫以利合者，迫穷祸患害相弃也。以天属者，迫穷祸患害相收也。君子之交淡若水，小人之交甘若醴。', 'note': '核心：以利合者，迫穷祸患相弃；以天属者，迫穷祸患相收。君子之交淡若水，小人之交甘若醴——真正的情谊以天性相连，不以利益驱动。'},
            ],
            'comparison': [
                {'label': '性质', 'left': '以利相交', 'right': '以天属相交'},
                {'label': '表现', 'left': '富贵时归附，穷困时相弃', 'right': '穷困时相收，利益时相合'},
                {'label': '境界', 'left': '小人之交，甘以绝', 'right': '君子之交，淡以亲'},
            ]
        },
        {
            'id': 'tian-xia',
            'filename': 'tian-xia.html',
            'title': '天下',
            'section': '杂篇',
            'label': '杂篇 ·',
            'author': '战国·庄周',
            'bgChar': '天',
            'isDaoJia': False,
            'coreQuote': '内圣外王之道，暗而不明，郁而不发',
            'blocks': [
                {'num': '一', 'orig': '天下之治方术者多矣，皆以其有为不可加矣。古之所谓道术者，恶乎在？圣有所生，王有所成，皆原于一。', 'note': '天下治方术者众多，都认为自己的一套已登峰造极。古代的道术，却不如此——圣人有所生，王有所成，皆原于"道"之一。'},
                {'num': '二', 'orig': '不离于宗，谓之天人。不离于精，谓之神人。不离于真，谓之至人。以天为宗，以德为本，以道为门，兆于变化，谓之圣人。', 'note': '四等人：天人（不离于宗）、神人（不离于精）、至人（不离于真）、圣人（以天为宗、以德为本、以道为门、兆于变化）。'},
                {'num': '三', 'orig': '内圣外王之道，暗而不明，郁而不发，天下之人各为其所欲焉以自为方。', 'note': '内圣外王：中国古代政治哲学的最高理想——内有圣人之德，外施王者之政。庄子叹其暗而不明、郁而不发，天下人各自为方，各是其是。'},
            ],
            'comparison': [
                {'label': '理想', 'left': '内圣——道德修养', 'right': '外王——政治事功'},
                {'label': '困境', 'left': '道术为天下裂', 'right': '各为其所欲，自以为是'},
                {'label': '评价', 'left': '郁而不发', 'right': '天下之大，求一以贯之者寡'},
            ]
        },
        {
            'id': 'dao-de-jing',
            'filename': 'dao-de-jing.html',
            'title': '道德经',
            'section': '道家',
            'label': '道家经典',
            'author': '老子·李耳',
            'bgChar': '道',
            'isDaoJia': True,
            'coreQuote': '上善若水，水善利万物而不争',
            'blocks': [
                {'num': '一', 'orig': '道可道，非常道。名可名，非常名。无名，天地之始；有名，万物之母。故常无欲，以观其妙；常有欲，以观其徼。', 'note': '道本体：可以用语言表述的道，就不是永恒的道。道的本体无形无名，是天地的起源、万物的根本。从"无欲"可观道之妙，从"有欲"可观道之徼。'},
                {'num': '二', 'orig': '天下皆知美之为美，斯恶已。皆知善之为善，斯不善已。故有无相生，难易相成，长短相形，高下相倾，音声相和，前后相随。', 'note': '相对性：天下皆知美为美，则丑已生；皆知善为善，则不善已立。有无、难易、长短、高下——一切对立都是相互成就的。'},
                {'num': '三', 'orig': '上善若水。水善利万物而不争，处众人之所恶，故几于道。', 'note': '上善若水：最高的善就像水一样——水利万物却不争，停留在众人厌恶的地方（水往低处流），所以最接近道。'},
                {'num': '四', 'orig': '为学日益，为道日损。损之又损，以至于无为，无为而无不为。', 'note': '为道日损：求学每天有得，修道每天在减。减到极点，就是"无为"——无为反而无不为。'},
                {'num': '五', 'orig': '小国寡民，使有什伯之器而不用，使民重死而不远徙。甘其食，美其服，安其居，乐其俗。邻国相望，鸡犬之声相闻，民至老死不相往来。', 'note': '小国寡民：老子的理想社会——国小民少，兵器无用，民重死不远迁，自足其食、安其居、乐其俗，邻国相望却老死不相往来。'},
            ],
            'comparison': [
                {'label': '核心', 'left': '道法自然', 'right': '无为而治'},
                {'label': '政治', 'left': '小国寡民', 'right': '鸡犬之声相闻，老死不相往来'},
                {'label': '修养', 'left': '为道日损', 'right': '上善若水，不争几于道'},
            ]
        },
        {
            'id': 'wen-zi',
            'filename': 'wen-zi.html',
            'title': '文子',
            'section': '道家',
            'label': '道家经典',
            'author': '辛计然·文子',
            'bgChar': '道',
            'isDaoJia': True,
            'coreQuote': '道者，万物之奥，善人之宝',
            'blocks': [
                {'num': '一', 'orig': '道者，万物之奥，善人之宝，不善人之所不保也。', 'note': '道为至宝：道是万物的深藏之处，善人珍惜它，不善的人也离不开它（虽暂失之，终不可保）。'},
                {'num': '二', 'orig': '圣人内求于己，不可得者，虽有过失，天地知之，知而不改者，天下非之。', 'note': '反求于己：圣人内求于己——有过失天地知之，知而不改则天下非之。反省的力量来自内心，不是外在的惩罚。'},
                {'num': '三', 'orig': '故通于天者，顺于道以游世者；通于地者，顺于德以游物者。', 'note': '通天顺道：通于天者，顺道以游世；通于地者，顺德以游物——人应与天地之道相通，而非与外物相争。'},
            ],
            'comparison': [
                {'label': '本体', 'left': '道为万物之奥', 'right': '不可言传'},
                {'label': '修养', 'left': '内求于己', 'right': '过失天地知之'},
                {'label': '境界', 'left': '顺道以游世', 'right': '顺德以游物'},
            ]
        },
        {
            'id': 'lie-zi',
            'filename': 'lie-zi.html',
            'title': '列子',
            'section': '道家',
            'label': '道家经典',
            'author': '郑·列御寇',
            'bgChar': '物',
            'isDaoJia': True,
            'coreQuote': '物物而不物于物，则胡可得而累邪',
            'blocks': [
                {'num': '一', 'orig': '有生不生，有化不化。不生者能生生，不化者能化化。生者不能不生，化者不能不化，故常生常化。', 'note': '不生者能生生：能够生成万物者，本身是不被生的。"不生者"是本体，"生生者"是道的作用。'},
                {'num': '二', 'orig': '夫言化者，皆有不生者也。有有者，言无者之所由生生也。有无之相生，其变乃大。', 'note': '有无相生：有与无相互生成，有产生无，无产生有，变化是无穷的。'},
                {'num': '三', 'orig': '物物而不物于物，则胡可得而累邪？', 'note': '物物而不物于物：主宰物而不被物所驱使、所束缚——人应做物的主人，而非物的奴仆。'},
            ],
            'comparison': [
                {'label': '本体', 'left': '不生者能生生', 'right': '不化者能化化'},
                {'label': '变化', 'left': '有无相生', 'right': '其变乃大'},
                {'label': '修养', 'left': '物物而不物于物', 'right': '不为外物所累'},
            ]
        },
        {
            'id': 'huainan-zi',
            'filename': 'huainan-zi.html',
            'title': '淮南子',
            'section': '道家',
            'label': '道家经典',
            'author': '西汉·刘安',
            'bgChar': '海',
            'isDaoJia': True,
            'coreQuote': '百川异源，而皆归于海；百家殊业，皆务于治',
            'blocks': [
                {'num': '一', 'orig': '天气为魂，地气为魄， Geist 之守，体气乃通。', 'note': '魂魄与体气：天气为魂，地气为魄， Geist 守住，体气乃通——人的精神与形体相合，生命才完整。'},
                {'num': '二', 'orig': '百川异源，而皆归于海。百家殊业，皆务于治。', 'note': '百川归海：百川源头各异，终归于海；百家事业不同，皆务于治——表面分歧，终点一致，归于大道。'},
                {'num': '三', 'orig': '圣人内修道术，不外饰仁义，而民自化。', 'note': '内圣而化：圣人在内心修道术，不在外在装饰仁义，而民众自然被感化——无为而化，是最深的治理。'},
            ],
            'comparison': [
                {'label': '宇宙', 'left': '天气为魂，地气为魄', 'right': 'Geist守则体气通'},
                {'label': '政治', 'left': '内修道术', 'right': '民自化'},
                {'label': '哲学', 'left': '百川归海', 'right': '百家殊业，归于一道'},
            ]
        },
        {
            'id': 'bao-pu-zi',
            'filename': 'bao-pu-zi.html',
            'title': '抱朴子',
            'section': '道家',
            'label': '道家经典',
            'author': '东晋·葛洪',
            'bgChar': '玄',
            'isDaoJia': True,
            'coreQuote': '玄者，自然之始祖，而万殊之大宗',
            'blocks': [
                {'num': '一', 'orig': '玄者，自然之始祖，而万殊之大宗也。', 'note': '玄为大宗：玄是自然的始祖、万殊的大宗——宇宙本体是"玄"，道家修仙即回归于玄。'},
                {'num': '二', 'orig': '得之者贵，不待黄钺之威；生之者富，不需天禄之赏。', 'note': '仙道贵生：得玄道者富贵，不待威势；养生者富足，不需天禄——仙道贵生，生命超越凡俗的限制。'},
                {'num': '三', 'orig': '欲求仙者，要当以忠孝和顺仁信为本。', 'note': '仙道与世法：修仙者以忠孝和顺仁信为本——道教修炼并不离世间法，而是以人间德行为根基。'},
            ],
            'comparison': [
                {'label': '本体', 'left': '玄为自然之祖', 'right': '万殊之大宗'},
                {'label': '目标', 'left': '贵生', 'right': '不待威势天禄'},
                {'label': '修养', 'left': '以忠孝仁信为本', 'right': '仙道不离世法'},
            ]
        },
    ]
    return {p['id']: p for p in pages_data}


def main():
    all_data = {}

    from_build = extract_from_build_remaining()
    all_data.update(from_build)

    # From root HTML files
    for f in sorted(BASE.glob('*.html')):
        if 'source_code' in str(f) or f.name == 'article.html':
            continue
        file_id = f.name.replace('.html', '')
        if file_id in from_build:
            continue
        try:
            data = extract_from_html(f)
            all_data[file_id] = data
            print(f"Extracted: {file_id}")
        except Exception as e:
            print(f"Error extracting {f.name}: {e}")

    # From daojia directory
    for f in sorted((BASE / 'daojia').glob('*.html')):
        file_id = f.name.replace('.html', '')
        if file_id in from_build:
            continue
        try:
            data = extract_from_html(f)
            all_data[file_id] = data
            print(f"Extracted: {file_id}")
        except Exception as e:
            print(f"Error extracting {f.name}: {e}")

    for file_id, data in all_data.items():
        outpath = DATA_DIR / f'{file_id}.json'
        with open(outpath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nExtracted {len(all_data)} chapters to {DATA_DIR}/")
    for fid in sorted(all_data.keys()):
        print(f"  - {fid}.json")


if __name__ == '__main__':
    main()
