#!/usr/bin/env python3
"""清理重建后的 HTML 文件中的残留问题"""

import re
from pathlib import Path

BASE = Path('/Users/rick/.openclaw/workspace/zhesi')

def cleanup_file(filepath):
    content = filepath.read_text(encoding='utf-8')
    original = content

    # 1. 删除重复的 <div class="side-rule"></div>
    content = re.sub(r'\s*<div class="side-rule"></div>\s*<div class="side-rule"></div>\s*',
                    '\n  <div class="side-rule"></div>\n',
                    content)

    # 2. 删除 content 区和 nav 之间的残留 </div></div>
    # 找到 reading-area 或 toc-area 或 cards-area 结束后多余的 </div></div>
    content = re.sub(r'\s*</div>\s*</div>\s*(?=\s*<footer>)', '\n', content)

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

    fixed = []
    for f in files:
        try:
            if cleanup_file(f):
                fixed.append(f.name)
        except Exception as e:
            print(f"ERROR {f.name}: {e}")

    print(f"Cleaned up: {len(fixed)} files")
    for name in fixed:
        print(f"  ~ {name}")


if __name__ == '__main__':
    main()
