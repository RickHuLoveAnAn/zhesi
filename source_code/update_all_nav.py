#!/usr/bin/env python3
"""清理所有 HTML 文件中重复的浮动导航，只保留最后一个"""

import re
from pathlib import Path

BASE = Path('/Users/rick/.openclaw/workspace/zhesi')


def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 找所有 <div class="float-nav" 的位置
    pattern = re.compile(r'<div class="float-nav"')
    positions = [m.start() for m in pattern.finditer(content)]

    if len(positions) <= 1:
        return False

    # 保留最后一个 nav，从第一个到最后一个之前全部删除
    first_start = positions[0]
    # 找第一个 nav 的起始点之前的内容（删除 <!-- 浮动导航 --> 或前面的空白）
    before_first = content[:first_start]
    # 确保删掉前面的导航注释
    before_first = re.sub(r'\s*<!--[^-]*浮动导航[^-]*-->\s*$', '', before_first)

    # 从最后一个 nav 位置开始找它的结束
    last_start = positions[-1]
    remaining = content[last_start:]

    # 找最后一个 nav 的完整结束（到 </div></div> 或 <footer 前面）
    end_match = re.search(r'</div>\s*</div>\s*(?=\s*(?:<footer|</body>))', remaining, re.DOTALL)
    if end_match:
        last_end = last_start + end_match.end()
    else:
        # fallback: 找 </div></div>
        end_match2 = re.search(r'</div>\s*</div>\s*', remaining, re.DOTALL)
        if end_match2:
            last_end = last_start + end_match2.end()
        else:
            print(f"  WARNING: {filepath.name} - cannot find nav end")
            return False

    # 重新组装
    content = before_first + remaining[:last_end - last_start]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


def main():
    updated = []
    for f in list(BASE.glob('*.html')) + list((BASE / 'daojia').glob('*.html')):
        try:
            if fix_file(f):
                updated.append(str(f.relative_to(BASE)))
        except Exception as e:
            print(f"Error {f.name}: {e}")

    print(f"Fixed {len(updated)} files")
    for f in updated:
        print(f"  {f}")


if __name__ == '__main__':
    main()
