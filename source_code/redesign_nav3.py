import os, re

base = "/Users/rick/.openclaw/workspace/zhesi"
daojia = os.path.join(base, "daojia")

nav_css = """
    /* ── 浮动导航 ── */
    .float-nav{position:fixed;bottom:28px;right:28px;z-index:100}
    .float-nav-btn{width:44px;height:44px;border-radius:50%;background:#1a1208;color:#f5f0e6;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 16px rgba(0,0,0,.3);transition:transform .2s,background .2s}
    .float-nav-btn:hover{background:#8b3a2e;transform:scale(1.08)}
    .float-nav-panel{display:none;position:absolute;bottom:52px;right:0;background:#2c2416;border-radius:14px;padding:0;min-width:240px;max-height:65vh;overflow-y:auto;box-shadow:0 12px 40px rgba(0,0,0,.45)}
    .float-nav.open .float-nav-panel{display:block;animation:fadeUp .2s ease}
    .float-nav-panel::-webkit-scrollbar{width:3px}.float-nav-panel::-webkit-scrollbar-thumb{background:rgba(166,124,82,.35);border-radius:2px}
    .float-nav-header{padding:14px 16px 12px;border-bottom:1px solid rgba(166,124,82,.2)}
    .float-nav-header-title{font-family:"ZCOOL XiaoWei",serif;font-size:.9rem;color:#a67c52;letter-spacing:.1em}
    .float-nav-section{margin:0}
    .float-nav-section-btn{display:flex;align-items:center;justify-content:space-between;width:100%;padding:9px 16px;background:none;border:none;border-top:1px solid rgba(166,124,82,.12);cursor:pointer;color:#c4b49a;font-size:.82rem;font-family:"Noto Serif SC",serif;text-align:left;transition:background .15s,color .15s}
    .float-nav-section-btn:hover{background:rgba(139,58,46,.2);color:#f5f0e6}
    .float-nav-section-btn .arrow{font-size:.6rem;transition:transform .25s;margin-left:8px;color:#7a6a58}
    .float-nav-section-btn.open .arrow{transform:rotate(180deg)}
    .float-nav-items{display:none;padding:4px 0 8px;background:rgba(0,0,0,.15)}
    .float-nav-items.open{display:block}
    .float-nav-item{display:block;padding:5px 16px 5px 22px;font-size:.78rem;color:#9a8b7a;text-decoration:none;transition:background .12s,color .12s;white-space:nowrap}
    .float-nav-item:hover{background:rgba(139,58,46,.2);color:#f0e8d8}
    .float-nav-item.active{color:#c47a5a;font-weight:600}
"""

js_code = "function toggleFloatNav(){document.getElementById('floatNav').classList.toggle('open')}function toggleSection(btn){btn.classList.toggle('open');btn.nextElementSibling.classList.toggle('open')}document.addEventListener('click',function(e){var nav=document.getElementById('floatNav');if(!nav.contains(e.target))nav.classList.remove('open')})"

MARKERS = ["/* ── 浮动导航（两级） ── */", "/* ── 浮动导航 ── */"]

def process_file(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace CSS block
    new_content = content
    for marker in MARKERS:
        idx = content.find(marker)
        if idx == -1:
            continue
        # Find end of CSS block: count braces
        brace = 0
        end = idx
        for i, ch in enumerate(content[idx:]):
            if ch == '{':
                brace += 1
            elif ch == '}':
                brace -= 1
                if brace == 0:
                    end = idx + i + 1
                    break
        new_content = content[:idx] + nav_css.strip() + content[end:]
        break

    # Replace JS
    new_content = re.sub(
        r'function toggleFloatNav\(\).*?function toggleSection\(btn\).*?</script>',
        js_code + '</script>',
        new_content,
        flags=re.DOTALL
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)

for directory in [base, daojia]:
    if not os.path.exists(directory):
        continue
    for fname in os.listdir(directory):
        if not fname.endswith('.html'):
            continue
        try:
            process_file(os.path.join(directory, fname))
            print(f"Updated: {fname}")
        except Exception as e:
            print(f"Error {fname}: {e}")

print("Done!")
