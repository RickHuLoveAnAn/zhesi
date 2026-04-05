#!/usr/bin/env python3
"""Test article.html + JSON data infrastructure"""

import json
import os
from pathlib import Path

BASE = Path('/Users/rick/.openclaw/workspace/zhesi')
DATA_DIR = BASE / 'data'

# Expected article IDs (40 - excluding index/tiandao which aren't articles)
EXPECTED_IDS = {
    # Zhuangzi Inner (7)
    'xiaoyao-you', 'qi-wu-lun', 'yang-sheng-zhu', 'ren-jian-shi',
    'de-chong-fu', 'da-zong-shi', 'ying-di-wang',
    # Zhuangzi Outer (15)
    'pian-mu', 'ma-ti', 'qu-qie', 'zai-you', 'tian-di', 'tian-dao',
    'tian-yun', 'ke-yi', 'shan-xing', 'qiu-shui', 'zhi-le', 'da-sheng',
    'shan-mu', 'tian-zi-fang', 'zhi-bei-you',
    # Zhuangzi Misc (11)
    'geng-sang-chu', 'xu-wu-gui', 'ze-yang', 'wai-wu', 'yu-yan',
    'rang-wang', 'dao-zhi', 'shuo-jian', 'yu-fu', 'lie-yu-kou', 'tian-xia',
    # Daoist Classics (7)
    'qing-jing-jing', 'taiyi-jinhua', 'dao-de-jing', 'wen-zi',
    'lie-zi', 'huainan-zi', 'bao-pu-zi',
}

REQUIRED_FIELDS = ['id', 'filename', 'title', 'blocks', 'coreQuote']
DAOJIA_IDS = {'qing-jing-jing', 'taiyi-jinhua', 'dao-de-jing', 'wen-zi',
               'lie-zi', 'huainan-zi', 'bao-pu-zi'}


def test_all_json_files_exist():
    """40 expected JSON files must exist"""
    existing = set(f.stem for f in DATA_DIR.glob('*.json'))
    missing = EXPECTED_IDS - existing
    extra = existing - EXPECTED_IDS
    assert not missing, f"Missing JSON files: {missing}"
    assert not extra, f"Unexpected JSON files: {extra}"


def test_json_valid_schema():
    """Each JSON has all required fields"""
    for f in DATA_DIR.glob('*.json'):
        data = json.loads(f.read_text(encoding='utf-8'))
        for field in REQUIRED_FIELDS:
            assert field in data, f"{f.name} missing field: {field}"


def test_blocks_have_orig_and_note():
    """Each block has non-empty orig and note"""
    for f in DATA_DIR.glob('*.json'):
        data = json.loads(f.read_text(encoding='utf-8'))
        for block in (data.get('blocks') or []):
            assert 'orig' in block, f"{f.name}: block missing 'orig'"
            assert 'note' in block, f"{f.name}: block missing 'note'"
            assert block.get('orig'), f"{f.name}: block orig is empty"


def test_no_empty_required_fields():
    """No empty strings for id, title, blocks"""
    for f in DATA_DIR.glob('*.json'):
        data = json.loads(f.read_text(encoding='utf-8'))
        assert data.get('id'), f"{f.name}: empty id"
        assert data.get('title'), f"{f.name}: empty title"
        assert len(data.get('blocks', [])) > 0, f"{f.name}: no blocks"


def test_bg_char_single_or_empty():
    """bgChar is single char or empty"""
    for f in DATA_DIR.glob('*.json'):
        data = json.loads(f.read_text(encoding='utf-8'))
        bg = data.get('bgChar', '')
        assert len(bg) <= 1, f"{f.name}: bgChar too long: {bg}"


def test_no_raw_newlines_in_fields():
    """Note/orig/coreQuote must not contain raw \\n or \\r"""
    for f in DATA_DIR.glob('*.json'):
        data = json.loads(f.read_text(encoding='utf-8'))
        for i, block in enumerate(data.get('blocks', [])):
            note = block.get('note', '')
            orig = block.get('orig', '')
            assert '\n' not in note and '\r' not in note, \
                f"{f.name} block[{i}] note has raw newlines"
            assert '\n' not in orig and '\r' not in orig, \
                f"{f.name} block[{i}] orig has raw newlines"
        cq = data.get('coreQuote', '')
        assert '\n' not in cq and '\r' not in cq, \
            f"{f.name} coreQuote has raw newlines"


def test_daojia_articles_have_isDaoJia_true():
    """Daoist classic articles should have isDaoJia=true"""
    for fid in DAOJIA_IDS:
        f = DATA_DIR / f'{fid}.json'
        if f.exists():
            data = json.loads(f.read_text(encoding='utf-8'))
            assert data.get('isDaoJia') == True, \
                f"{fid} should have isDaoJia=true"


def test_index_html_exists():
    """index.html must exist at root"""
    assert (BASE / 'index.html').exists(), "index.html not found"


def test_index_html_has_toc():
    """index.html contains card grid with all sections"""
    html = (BASE / 'index.html').read_text(encoding='utf-8')
    assert 'home-cards' in html, "Missing home-cards"
    assert 'home-card' in html, "Missing home-card"
    # Has all 4 section cards
    assert '庄子·内篇' in html
    assert '庄子·外篇' in html
    assert '庄子·杂篇' in html
    assert '道家经典' in html
    # Has key article links
    assert 'article.html?id=xiaoyao-you' in html
    assert 'article.html?id=taiyi-jinhua' in html


def test_article_html_exists():
    """article.html must exist"""
    assert (BASE / 'article.html').exists(), "article.html not found"


def test_article_html_loads():
    """article.html is valid HTML with closing tags"""
    html = (BASE / 'article.html').read_text(encoding='utf-8')
    assert '<!DOCTYPE html>' in html, "Missing DOCTYPE"
    assert '</html>' in html, "Unclosed html tag"
    assert '</body>' in html, "Unclosed body tag"
    assert '<script' in html, "Missing script tag"


def test_article_html_has_core_elements():
    """article.html contains all key rendering elements"""
    html = (BASE / 'article.html').read_text(encoding='utf-8')
    assert 'id="hero-title"' in html, "Missing hero-title"
    assert 'id="hero-label"' in html, "Missing hero-label"
    assert 'id="hero-subtitle"' in html, "Missing hero-subtitle"
    assert 'id="orig-col"' in html, "Missing orig-col"
    assert 'id="note-col"' in html, "Missing note-col"
    assert 'class="float-nav"' in html, "Missing float-nav"
    assert 'source_code/nav.css' in html, "Missing nav.css link"
    assert 'source_code/nav.js' in html, "Missing nav.js script"


def test_article_html_fetches_json():
    """article.html JS fetches JSON by id param"""
    html = (BASE / 'article.html').read_text(encoding='utf-8')
    assert 'fetch(`data/${id}.json`)' in html, \
        "Missing fetch('data/${id}.json')"
    assert 'URLSearchParams' in html, "Missing URLSearchParams"
    assert 'renderArticle' in html, "Missing renderArticle"


def test_article_renders_core_quote():
    """article.html renders coreQuote as blockquote"""
    html = (BASE / 'article.html').read_text(encoding='utf-8')
    assert 'class="core-quote"' in html, "Missing core-quote"
    assert 'blockquote>' in html, "Missing blockquote element"


def test_article_renders_comparison():
    """article.html has comparison table structure"""
    html = (BASE / 'article.html').read_text(encoding='utf-8')
    assert 'comparison-section' in html, "Missing comparison-section"
    assert 'row-label' in html, "Missing row-label class"


def test_navigation_has_all_chapters():
    """Float-nav links to article.html?id=xxx for all 40 articles"""
    html = (BASE / 'article.html').read_text(encoding='utf-8')
    for fid in EXPECTED_IDS:
        expected = f'href="article.html?id={fid}"'
        assert expected in html, f"Missing nav link for {fid}"


def test_navigation_section_counts():
    """Nav section headers show correct counts"""
    html = (BASE / 'article.html').read_text(encoding='utf-8')
    assert '内篇（7篇）' in html, "Wrong inner count"
    assert '外篇（15篇）' in html, "Wrong outer count"
    assert '杂篇（11篇）' in html, "Wrong misc count"
    assert '道家经典（7篇）' in html, "Wrong daojia count"


def test_each_json_loads_without_error():
    """Each JSON file parses without error"""
    for f in DATA_DIR.glob('*.json'):
        try:
            json.loads(f.read_text(encoding='utf-8'))
        except json.JSONDecodeError as e:
            assert False, f"{f.name} failed to parse: {e}"


def test_blocks_have_num_field():
    """Each block has a num field"""
    for f in DATA_DIR.glob('*.json'):
        data = json.loads(f.read_text(encoding='utf-8'))
        for i, block in enumerate(data.get('blocks', [])):
            assert 'num' in block, f"{f.name} block[{i}] missing num"


def test_comparison_rows_have_three_fields():
    """Comparison rows have label, left, right"""
    for f in DATA_DIR.glob('*.json'):
        data = json.loads(f.read_text(encoding='utf-8'))
        for row in data.get('comparison', []):
            assert 'label' in row, f"{f.name} comparison row missing label"
            assert 'left' in row, f"{f.name} comparison row missing left"
            assert 'right' in row, f"{f.name} comparison row missing right"


def test_title_is_not_unknown():
    """No article should have title '未知'"""
    for f in DATA_DIR.glob('*.json'):
        data = json.loads(f.read_text(encoding='utf-8'))
        title = data.get('title', '')
        # index pages can have special titles, but not '未知'
        if f.stem != 'index':
            assert title != '未知', f"{f.name} has unknown title"


def test_blocks_have_pinyin_field():
    """Each block has a non-empty pinyin field"""
    for f in DATA_DIR.glob('*.json'):
        data = json.loads(f.read_text(encoding='utf-8'))
        for i, block in enumerate(data.get('blocks', [])):
            assert 'pinyin' in block, f"{f.name} block[{i}] missing pinyin"
            assert block.get('pinyin'), f"{f.name} block[{i}] pinyin is empty"


def test_blocks_have_ruby_field():
    """Each block has a non-empty ruby field"""
    for f in DATA_DIR.glob('*.json'):
        data = json.loads(f.read_text(encoding='utf-8'))
        for i, block in enumerate(data.get('blocks', [])):
            assert 'ruby' in block, f"{f.name} block[{i}] missing ruby"
            assert block.get('ruby'), f"{f.name} block[{i}] ruby is empty"


def test_ruby_contains_ruby_tags():
    """ruby field contains <ruby> HTML tags"""
    for f in DATA_DIR.glob('*.json'):
        data = json.loads(f.read_text(encoding='utf-8'))
        for i, block in enumerate(data.get('blocks', [])):
            ruby = block.get('ruby', '')
            assert '<ruby>' in ruby, f"{f.name} block[{i}] ruby missing <ruby> tag"
            assert '<rt>' in ruby, f"{f.name} block[{i}] ruby missing <rt> tag"


def test_pinyin_has_tone_marks():
    """pinyin field contains proper Unicode tone marks (not ASCII tone numbers)"""
    for f in DATA_DIR.glob('*.json'):
        data = json.loads(f.read_text(encoding='utf-8'))
        for i, block in enumerate(data.get('blocks', [])):
            pinyin = block.get('pinyin', '')
            # Unicode tone marks are non-ASCII (combining diacritics on vowels)
            has_tone_mark = any(ord(c) > 127 for c in pinyin)
            assert has_tone_mark, f"{f.name} block[{i}] pinyin missing Unicode tone marks: {pinyin[:50]}"


def test_article_html_has_pinyin_toggle():
    """article.html has pinyin toggle button and togglePinyin function"""
    html = (BASE / 'article.html').read_text(encoding='utf-8')
    assert 'id="pinyinToggle"' in html, "Missing pinyinToggle button"
    assert 'togglePinyin()' in html, "Missing togglePinyin function"
    assert 'orig-ruby' in html, "Missing orig-ruby class in article.html"


def test_article_html_renders_ruby_div():
    """article.html renderArticle adds orig-ruby div for each block"""
    html = (BASE / 'article.html').read_text(encoding='utf-8')
    assert 'style="display:none"' in html or "style=\"display:none\"" in html, \
        "Missing hidden orig-ruby div in article.html"


def test_article_html_has_audio_toggle():
    """article.html has audio toggle button and HTML5 Audio player"""
    html = (BASE / 'article.html').read_text(encoding='utf-8')
    assert 'id="audioToggle"' in html, "Missing audioToggle button"
    assert 'toggleAudio()' in html, "Missing toggleAudio function"
    assert 'initAudioPlayer' in html, "Missing initAudioPlayer function"
    assert 'articleAudio' in html, "Missing articleAudio variable"
    assert '__articleBlocks' in html, "Missing __articleBlocks exposure"


def test_blocks_have_pinyin_sentences():
    """Each block has a non-empty pinyinSentences field"""
    for f in DATA_DIR.glob('*.json'):
        data = json.loads(f.read_text(encoding='utf-8'))
        for i, block in enumerate(data.get('blocks', [])):
            assert 'pinyinSentences' in block, f"{f.name} block[{i}] missing pinyinSentences"
            ps = block['pinyinSentences']
            assert ps, f"{f.name} block[{i}] pinyinSentences is empty"
            # Must have Chinese punctuation or reasonable length (not just single char)
            assert len(ps) >= 4, f"{f.name} block[{i}] pinyinSentences too short: {ps}"


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
