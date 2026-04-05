#!/usr/bin/env python3
"""精确定位删除重复的 float-nav div"""

import re
from pathlib import Path

BASE = Path('/Users/rick/.openclaw/workspace/zhesi')

def find_nth_nav_end(content, nav_index):
    """找到第 n 个 float-nav div 的结束位置"""
    pattern = re.compile(r'<div class="float-nav" id="floatNav">')
    matches = list(pattern.finditer(content))
    if nav_index >= len(matches):
        return None
    nav_start = matches[nav_index].start()
    # 从 nav_start 往后找 </div></div> 后面跟 <footer> 或 </body>
    after = content[nav_start:]
    m = re.search(r'</div>\s*</div>\s*(?=\s*<footer|\s*</body)', after)
    if m:
        return nav_start + m.end()
    return None


def fix_file(filepath):
    content = filepath.read_text(encoding='utf-8')

    nav_pattern = re.compile(r'<div class="float-nav" id="floatNav">')
    matches = list(nav_pattern.finditer(content))

    if len(matches) <= 1:
        return False

    # 策略：保留最后一个 nav
    # 找到倒数第二个 nav 的开始和结束
    second_last_nav_start = matches[-2].start()
    last_nav_end = find_nth_nav_end(content, len(matches) - 1)

    if last_nav_end is None:
        return False

    # 删除从 second_last_nav_start 到 last_nav_end 的所有内容
    new_content = content[:second_last_nav_start] + content[last_nav_end:]

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
            if fix_file(f):
                fixed.append(f.name)
        except Exception as e:
            print(f"ERROR {f.name}: {e}")

    print(f"Fixed: {len(fixed)} files")
    for name in fixed:
        print(f"  ~ {name}")


if __name__ == '__main__':
    main()
