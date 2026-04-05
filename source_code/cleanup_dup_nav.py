#!/usr/bin/env python3
"""删除重复的 float-nav div，只保留最后一个"""

import re
from pathlib import Path

BASE = Path('/Users/rick/.openclaw/workspace/zhesi')

def fix_dup_nav(filepath):
    content = filepath.read_text(encoding='utf-8')

    positions = [m.start() for m in re.finditer(r'<div class="float-nav" id="floatNav">', content)]
    if len(positions) <= 1:
        return False

    footer_abs = content.find('<footer>')
    if footer_abs == -1:
        footer_abs = content.find('</body>')
    if footer_abs == -1:
        return False

    # 在 content[footer_abs-2000:footer_abs+20] 中找
    search_range = content[max(0, footer_abs-2000):footer_abs+20]
    m = re.search(r'</div>\s*</div>\s*\n\s*<footer>', search_range)
    if m:
        # second_nav_end 是这个匹配在 search_range 中的开始位置，转换到 content 中的位置
        second_nav_end = max(0, footer_abs-2000) + m.start()
    else:
        return False

    first_nav_pos = positions[0]

    # 删除从第一个 nav 到第二个 nav 结束之间的所有内容
    new_content = content[:first_nav_pos] + content[second_nav_end:]

    if new_content != content:
        filepath.write_text(new_content, encoding='utf-8')
        return True
    return False


def main():
    files = []
    for f in sorted(BASE.glob('*.html')):
        if 'source_code' not in str(f):
            files.append(f)
    for f in sorted((BASE / 'daojia').glob('*.html')):
        files.append(f)

    fixed = []
    for f in files:
        try:
            if fix_dup_nav(f):
                fixed.append(f.name)
        except Exception as e:
            print(f"ERROR {f.name}: {e}")

    print(f"Fixed: {len(fixed)} files")
    for name in fixed:
        print(f"  ~ {name}")


if __name__ == '__main__':
    main()
