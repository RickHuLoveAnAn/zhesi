#!/usr/bin/env python3
"""从损坏的 HTML 文件中提取内容并重建正确结构"""

import re
from pathlib import Path

BASE = Path('/Users/rick/.openclaw/workspace/zhesi')

# 读取共享组件
NAV_CSS = (BASE / 'source_code/nav.css').read_text(encoding='utf-8')
NAV_HTML_ZHUANGZI = (BASE / 'source_code/nav.html').read_text(encoding='utf-8')
NAV_HTML_DAOJIA = (BASE / 'source_code/nav_daojia.html').read_text(encoding='utf-8')
NAV_JS = (BASE / 'source_code/nav.js').read_text(encoding='utf-8')

TAIL_ZHUANGZI = """
  <footer>
    <div class="brand">庄子 · 全文导航</div>
    <div class="copy">OpenClaw 整理 &nbsp;·&nbsp; 2026</div>
  </footer>

  <script>
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) entry.target.classList.add('visible');
      });
    }, { threshold: 0.08 });
    document.querySelectorAll('[data-reveal]').forEach(el => observer.observe(el));
  </script>
  <script src="source_code/nav.js" defer></script>
</body>
</html>"""

TAIL_DAOJIA = """
  <footer>
    <div class="brand">道家经典</div>
    <div class="copy">OpenClaw 整理 &nbsp;·&nbsp; 2026</div>
  </footer>

  <script>
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) entry.target.classList.add('visible');
      });
    }, { threshold: 0.08 });
    document.querySelectorAll('[data-reveal]').forEach(el => observer.observe(el));
  </script>
  <script src="../source_code/nav.js" defer></script>
</body>
</html>"""

HEAD_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;600&family=ZCOOL+XiaoWei&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{css_path}">
</head>
<body>
  <div class="side-rule"></div>
"""


def extract_body_content(content):
    """Extract everything from <div class="side-rule"> to the last proper content piece"""
    # Find where body content starts (after side-rule)
    side_rule_pos = content.find('<div class="side-rule">')
    if side_rule_pos == -1:
        return None

    # The content we want is from side-rule to just before the first float-nav-section
    # (which is where the corruption starts)
    first_nav_section = content.find('<div class="float-nav-section">', side_rule_pos)
    if first_nav_section == -1:
        # No corruption yet - find last </footer> or </div></body> etc.
        # Return everything from side-rule to end minus any trailing nav junk
        body_content = content[side_rule_pos:]
        # Remove any trailing float-nav fragments
        last_proper_end = body_content.rfind('</footer>')
        if last_proper_end != -1:
            body_content = body_content[:last_proper_end + len('</footer>')]
        return body_content

    # Return content from side-rule to just before first nav section
    return content[side_rule_pos:first_nav_section]


def extract_title(content):
    """Extract page title"""
    m = re.search(r'<title>([^<]+)</title>', content)
    return m.group(1) if m else '庄子'


def rebuild_file(filepath):
    """Rebuild a corrupted HTML file"""
    content = filepath.read_text(encoding='utf-8')
    is_daojia = '/daojia/' in str(filepath) or str(filepath).endswith('daojia/index.html')
    css_path = '../source_code/nav.css' if is_daojia else 'source_code/nav.css'
    nav_html = NAV_HTML_DAOJIA if is_daojia else NAV_HTML_ZHUANGZI
    tail = TAIL_DAOJIA if is_daojia else TAIL_ZHUANGZI

    title = extract_title(content)
    body_content = extract_body_content(content)
    if body_content is None:
        print(f"  ERROR: Cannot find body content in {filepath.name}")
        return False

    # Rebuild the file
    rebuilt = HEAD_TEMPLATE.format(title=title, css_path=css_path)
    rebuilt += body_content + '\n'
    rebuilt += '\n' + nav_html + '\n'
    rebuilt += tail + '\n'

    filepath.write_text(rebuilt, encoding='utf-8')
    return True


def main():
    files = []
    for f in sorted(BASE.glob('*.html')):
        if 'source_code' not in str(f):
            files.append(f)
    for f in sorted((BASE / 'daojia').glob('*.html')):
        files.append(f)

    rebuilt = []
    errors = []
    for f in files:
        try:
            if rebuild_file(f):
                rebuilt.append(f.name)
        except Exception as e:
            errors.append((f.name, str(e)))

    print(f"Rebuilt: {len(rebuilt)} files")
    for name in rebuilt:
        print(f"  + {name}")
    if errors:
        print(f"\nErrors: {len(errors)}")
        for name, err in errors:
            print(f"  ERROR {name}: {err}")


if __name__ == '__main__':
    main()
