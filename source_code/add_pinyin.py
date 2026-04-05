#!/usr/bin/env python3
"""
Add pinyin field to each block in all JSON data files.
Uses jieba word segmentation + pypinyin Style.TONE (Unicode tone marks).
"""

import json
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


def add_pinyin_to_file(json_path: Path) -> bool:
    """Add pinyin and ruby fields to each block. Returns True if modified."""
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
            else:
                # Preserve whitespace/punctuation as-is in the list
                for ch in word:
                    if not is_cjk(ch):
                        pass  # skip non-CJK from pinyin list

        block['pinyin'] = ' '.join(pinyin_list)
        block['ruby'] = orig_to_ruby(orig)
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
