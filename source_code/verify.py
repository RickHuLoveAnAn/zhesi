#!/usr/bin/env python3
"""验证 zhesi HTML 文件的完整性"""

from pathlib import Path

BASE = Path('/Users/rick/.openclaw/workspace/zhesi')

def check_file(filepath):
    content = open(filepath, 'r', encoding='utf-8').read()
    errors = []
    is_daojia = '/daojia/' in str(filepath)
    is_root_index = str(filepath).endswith('index.html') and not is_daojia
    is_daojia_index = str(filepath).endswith('daojia/index.html')
    is_chapter = not is_root_index and not is_daojia_index

    # === 基础检查 ===
    if '<!DOCTYPE html>' not in content:
        errors.append('missing DOCTYPE')
    if '</html>' not in content:
        errors.append('missing </html>')
    if '</body>' not in content:
        errors.append('missing </body>')

    # nav.css 和 nav.js 引用
    if is_daojia:
        if '../source_code/nav.css' not in content:
            errors.append('missing daojia nav.css link')
        if '../source_code/nav.js' not in content:
            errors.append('missing daojia nav.js link')
    else:
        if 'source_code/nav.css' not in content:
            errors.append('missing nav.css link')
        if 'source_code/nav.js' not in content:
            errors.append('missing nav.js link')

    # nav HTML 结构
    if 'class="float-nav"' not in content:
        errors.append('missing float-nav')
    if 'class="float-nav-panel"' not in content:
        errors.append('missing float-nav-panel')
    if 'class="float-nav-section-btn"' not in content:
        errors.append('missing float-nav-section-btn')
    if 'class="float-nav-items"' not in content:
        errors.append('missing float-nav-items')

    # 通用 UI 元素
    if 'class="side-rule"' not in content:
        errors.append('missing side-rule')
    if 'class="hero"' not in content:
        errors.append('missing hero')
    if 'fonts.googleapis.com' not in content:
        errors.append('missing Google Fonts')

    # nav 数量检查
    nav_count = content.count('class="float-nav"')
    if nav_count != 1:
        errors.append(f'duplicate nav count={nav_count}')

    # inline style 检查
    if '<style>' in content and '</style>' in content:
        errors.append('has inline <style>')

    # === 类型特定检查 ===
    if is_root_index:
        # 根目录 index.html - 应该是目录页，使用 toc-area
        if 'class="toc-area"' not in content:
            errors.append('missing toc-area')
        if 'class="toc-list"' not in content:
            errors.append('missing toc-list')

    elif is_daojia_index:
        # daojia/index.html - 卡片导航页，使用 cards-area
        if 'class="cards-area"' not in content:
            errors.append('missing cards-area')
        if 'class="cards-grid"' not in content:
            errors.append('missing cards-grid')

    elif is_chapter:
        # 章节内容页 - 使用 reading-area + 左右两栏
        if 'class="reading-area"' not in content:
            errors.append('missing reading-area')
        if 'class="orig-col"' not in content:
            errors.append('missing orig-col (left column)')
        if 'class="note-col"' not in content:
            errors.append('missing note-col (right column)')
        if 'class="text-grid"' not in content:
            errors.append('missing text-grid (two-column layout)')

        # 高亮名句
        if 'class="core-quote"' not in content:
            errors.append('missing core-quote (highlighted quote)')
        # 对照表格
        if 'class="comparison-section"' not in content:
            errors.append('missing comparison-section (comparison table)')

    ok = len(errors) == 0
    return ok, errors


def main():
    files = sorted([f for f in BASE.glob('*.html') if 'source_code' not in str(f)])
    files += sorted([f for f in (BASE / 'daojia').glob('*.html')])

    total = 0
    passed = 0
    failed = []

    for f in files:
        total += 1
        ok, errors = check_file(f)
        if ok:
            passed += 1
            print(f'  PASS {f.name}')
        else:
            failed.append((f, errors))
            print(f'  FAIL {f.name}')
            for e in errors:
                print(f'    - {e}')

    print(f'\n{passed}/{total} files passed')
    if failed:
        print(f'\nFailed ({len(failed)}):')
        for f, errors in failed:
            print(f'  {f.name}: {", ".join(errors)}')


if __name__ == '__main__':
    main()
