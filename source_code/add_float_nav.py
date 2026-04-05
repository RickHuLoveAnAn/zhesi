import os

base = os.path.expanduser("~/.openclaw/workspace/zhesi")

articles = [
    ("index.html", "导航页"),
    ("zhuangzi-tiandao.html", "天道"),
    ("xiaoyao-you.html", "逍遥游"),
    ("qi-wu-lun.html", "齐物论"),
    ("yang-sheng-zhu.html", "养生主"),
    ("ren-jian-shi.html", "人间世"),
    ("de-chong-fu.html", "德充符"),
    ("da-zong-shi.html", "大宗师"),
    ("ying-di-wang.html", "应帝王"),
]

floating_nav_html = '  <!-- 浮动导航 -->\n  <div class="float-nav" id="floatNav">\n    <button class="float-nav-btn" onclick="toggleFloatNav()" title="庄子内篇导航">\n      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">\n        <line x1="3" y1="6" x2="21" y2="6"/>\n        <line x1="3" y1="12" x2="21" y2="12"/>\n        <line x1="3" y1="18" x2="21" y2="18"/>\n      </svg>\n    </button>\n    <div class="float-nav-panel" id="floatNavPanel">\n      <div class="float-nav-title">庄子·内篇</div>\n'

for fname, label in articles:
    floating_nav_html += f'      <a class="float-nav-item" href="{fname}">{label}</a>\n'

floating_nav_html += '    </div>\n  </div>\n'

floating_nav_css = '''
    /* ── 浮动导航 ── */
    .float-nav {
      position: fixed;
      bottom: 28px;
      right: 28px;
      z-index: 100;
    }
    .float-nav-btn {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: #1a1208;
      color: #f5f0e6;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 16px rgba(0,0,0,0.25);
      transition: transform 0.2s, background 0.2s;
    }
    .float-nav-btn:hover { background: #b83a2e; transform: scale(1.08); }
    .float-nav-panel {
      display: none;
      position: absolute;
      bottom: 52px;
      right: 0;
      background: #1a1208;
      border-radius: 10px;
      padding: 14px 4px;
      min-width: 130px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .float-nav.open .float-nav-panel { display: block; animation: fadeUp 0.2s ease; }
    .float-nav-title {
      font-family: "ZCOOL XiaoWei", serif;
      font-size: 0.85rem;
      color: #a67c52;
      padding: 0 14px 10px;
      margin-bottom: 6px;
      border-bottom: 1px solid rgba(166,124,82,0.3);
      letter-spacing: 0.1em;
    }
    .float-nav-item {
      display: block;
      padding: 8px 16px;
      font-size: 0.8rem;
      color: #d4c9b8;
      text-decoration: none;
      border-radius: 4px;
      transition: background 0.15s, color 0.15s;
      white-space: nowrap;
    }
    .float-nav-item:hover { background: rgba(184,58,46,0.2); color: #f5f0e6; }
    .float-nav-item.active { color: #b83a2e; font-weight: 600; }
'''

js = '''
    function toggleFloatNav() {
      document.getElementById('floatNav').classList.toggle('open');
    }
    document.addEventListener('click', function(e) {
      var nav = document.getElementById('floatNav');
      if (!nav.contains(e.target)) nav.classList.remove('open');
    });
'''

for fname, label in articles:
    fpath = os.path.join(base, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add CSS before </head>
    if '/* ── 浮动导航 ── */' not in content:
        content = content.replace('</head>', f'<style>{floating_nav_css}</style></head>')

    # Add HTML before <footer>
    content = content.replace('<footer>', f'{floating_nav_html}<footer>')

    # Add JS before </body>
    content = content.replace('</body>', f'<script>{js}</script></body>')

    # Highlight active item
    content = content.replace(f'href="{fname}"', f'href="{fname}" class="active"')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated: {fname}")

print("All done!")
