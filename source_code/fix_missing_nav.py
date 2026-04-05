#!/usr/bin/env python3
"""修复 nav 被错误删除的文件，重新插入 nav HTML"""

import re
from pathlib import Path

BASE = Path('/Users/rick/.openclaw/workspace/zhesi')
NAV_ZHUANGZI = (BASE / 'source_code/nav.html').read_text(encoding='utf-8')
NAV_DAOJIA = (BASE / 'source_code/nav_daojia.html').read_text(encoding='utf-8')

def fix_file(filepath):
    content = filepath.read_text(encoding='utf-8')
    is_daojia = '/daojia/' in str(filepath)
    nav_html = NAV_DAOJIA if is_daojia else NAV_ZHUANGZI

    # 检查是否已经有 float-nav
    if 'class="float-nav"' in content:
        return False  # 已经有 nav，不需要修复

    # 找 </div>...</div><footer> 模式（残留的 nav 关闭标签）
    # 尝试多种模式
    patterns = [
        # 4空格缩进 (root files)
        (r'\n</div>\n    </div>\n(<footer>)', r'\n' + nav_html + r'\n\1'),
        # 无缩进 (daojia files)
        (r'\n</div>\n(<footer>)', r'\n' + nav_html + r'\n\1'),
        # 其他可能的变体
        (r'</div>\n    </div>\n(<footer>)', nav_html + r'\n\1'),
        (r'</div>\n(<footer>)', nav_html + r'\n\1'),
    ]

    for pattern, replacement in patterns:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            filepath.write_text(new_content, encoding='utf-8')
            return True

    return False


def main():
    # 需要修复的 8 个文件（pian-mu 已手动修复）
    files_to_fix = [
        'bao-pu-zi.html',
        'geng-sang-chu.html',
        'ma-ti.html',
        'qu-qie.html',
        'xu-wu-gui.html',
        'ze-yang.html',
        'index.html',
        'daojia/bao-pu-zi.html',
        'daojia/index.html',
        'daojia/qing-jing-jing.html',
    ]

    fixed = []
    for name in files_to_fix:
        f = BASE / name
        if not f.exists():
            print(f"  SKIP {name}: not found")
            continue
        try:
            if fix_file(f):
                fixed.append(name)
                print(f"  FIXED {name}")
            else:
                print(f"  NO CHANGE {name}")
        except Exception as e:
            print(f"  ERROR {name}: {e}")

    print(f"\nFixed: {len(fixed)} files")


if __name__ == '__main__':
    main()
