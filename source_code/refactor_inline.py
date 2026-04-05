#!/usr/bin/env python3
"""将 HTML 文件的 inline CSS/JS/HTML 替换为共享组件引用"""

import re
from pathlib import Path

BASE = Path('/Users/rick/.openclaw/workspace/zhesi')

def get_nav_html(is_daojia):
    path = BASE / ('source_code/nav_daojia.html' if is_daojia else 'source_code/nav.html')
    return path.read_text(encoding='utf-8')

def process_file(filepath):
    content = filepath.read_text(encoding='utf-8')
    original = content
    is_daojia = '/daojia/' in str(filepath) or str(filepath).endswith('daojia/index.html')
    css_prefix = '../' if is_daojia else ''
    js_prefix = '../' if is_daojia else ''

    # 1. 替换整个 <style>...</style> 块为 <link> 标签（放在 </head> 前）
    # 匹配从 <style> 开头到 </style> 结尾的整块
    style_block_pattern = re.compile(
        r'\s*<style>\s*\n.*?\n\s*</style>\s*',
        re.DOTALL
    )
    replacement = f'\n  <link rel="stylesheet" href="{css_prefix}source_code/nav.css">\n'
    content = style_block_pattern.sub(replacement, content)

    # 2. 替换 float-nav HTML 块
    nav_pattern = re.compile(
        r'\s*<div class="float-nav" id="floatNav">.*?</div>\s*</div>\s*',
        re.DOTALL
    )
    nav_html = get_nav_html(is_daojia)
    content = nav_pattern.sub('\n' + nav_html + '\n', content)

    # 3. 替换 <script>toggleFloatNav</script>
    script_pattern = re.compile(
        r'\s*<script>\s*function toggleFloatNav.*?</script>\s*',
        re.DOTALL
    )
    content = script_pattern.sub(
        f'\n  <script src="{js_prefix}source_code/nav.js" defer></script>\n',
        content
    )

    if content != original:
        filepath.write_text(content, encoding='utf-8')
        return True
    return False


def main():
    files = []
    for f in sorted(BASE.glob('*.html')):
        if 'source_code' not in str(f):
            files.append(f)
    for f in sorted((BASE / 'daojia').glob('*.html')):
        files.append(f)

    updated = []
    errors = []
    for f in files:
        try:
            if process_file(f):
                updated.append(f.name)
        except Exception as e:
            errors.append((f.name, str(e)))

    print(f"Updated: {len(updated)} files")
    for name in updated:
        print(f"  + {name}")
    if errors:
        print(f"\nErrors: {len(errors)}")
        for name, err in errors:
            print(f"  ERROR {name}: {err}")


if __name__ == '__main__':
    main()
