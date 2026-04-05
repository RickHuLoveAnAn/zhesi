#!/usr/bin/env python3
"""
Add pinyin field to each block in all JSON data files.
Uses jieba word segmentation + pypinyin Style.TONE (Unicode tone marks).
"""

import json
import re
from pathlib import Path
import jieba
from pypinyin import lazy_pinyin, Style

BASE = Path('/Users/rick/.openclaw/workspace/zhesi')
DATA_DIR = BASE / 'data'


def is_cjk(char: str) -> bool:
    """Check if a character is a CJK ideograph."""
    code = ord(char)
    return 0x4E00 <= code <= 0x9FFF or 0x3400 <= code <= 0x4DBF


def orig_to_ruby(orig: str) -> str:
    """
    Build ruby HTML using jieba word segmentation.
    Each Chinese character is paired with its pinyin (with tone mark).
    """
    words = list(jieba.cut(orig))
    html = ''
    for word in words:
        if not word.strip():
            html += word
            continue
        pinyins = lazy_pinyin(word, style=Style.TONE)
        for char, py in zip(word, pinyins):
            if is_cjk(char):
                escaped = char.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                html += f'<ruby>{escaped}<rt>{py}</rt></ruby>'
            else:
                html += char
    return html


def build_pinyin_sentences(orig: str) -> str:
    """
    Build pinyin string grouped by sentence for TTS reading.
    Splits orig by sentence-ending punctuation (。；) and computes
    pinyin for each sentence independently, then joins sentences
    with ' 。 ' so TTS reads each sentence as one continuous phrase.
    """
    # Split orig into parts: [text, sep, text, sep, ...]
    parts = re.split(r'(。|；)', orig)
    sentences = []
    for part in parts:
        if not part.strip():
            continue
        if part in '。；':
            # sentence boundary - add separator
            if sentences:
                sentences.append(' ' + part + ' ')
            continue
        # Regular text: compute pinyin and join syllables with spaces
        words = list(jieba.cut(part))
        syllable_groups = []
        for word in words:
            if not word.strip():
                continue
            pinyins = lazy_pinyin(word, style=Style.TONE)
            syllable_groups.append(' '.join(pinyins))
        sentences.append(' '.join(syllable_groups))
    result = ''.join(sentences)
    # Clean up multiple spaces
    result = re.sub(r' +', ' ', result).strip()
    return result


def add_pinyin_to_file(json_path: Path) -> bool:
    """Add pinyin, ruby, and pinyinSentences fields to each block."""
    data = json.loads(json_path.read_text(encoding='utf-8'))
    modified = False

    for block in data.get('blocks', []):
        orig = block.get('orig', '')
        if not orig:
            continue
        # Always regenerate to ensure correctness

        # Build pinyin list using jieba segmentation
        words = list(jieba.cut(orig))
        pinyin_list = []
        for word in words:
            if word.strip():
                pinyins = lazy_pinyin(word, style=Style.TONE)
                pinyin_list.extend(pinyins)

        block['pinyin'] = ' '.join(pinyin_list)
        block['ruby'] = orig_to_ruby(orig)
        block['pinyinSentences'] = build_pinyin_sentences(orig)
        modified = True

    if modified:
        json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    return modified


def main():
    # Pre-load jieba to avoid repeated initialization output
    _ = list(jieba.cut('测试'))

    json_files = list(DATA_DIR.glob('*.json'))
    total = len(json_files)
    modified_count = 0

    for json_path in sorted(json_files):
        modified = add_pinyin_to_file(json_path)
        status = '✓' if modified else '-'
        print(f"  {status} {json_path.name}")
        if modified:
            modified_count += 1

    print(f"\nDone: {modified_count}/{total} files updated.")


if __name__ == '__main__':
    main()
