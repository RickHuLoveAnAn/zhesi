#!/usr/bin/env python3
"""使用 daojia/index.html 的原始 CSS 重建所有文件的 <style> 块，并更新浮动导航为统一样式"""

import re
from pathlib import Path

BASE = Path('/Users/rick/.openclaw/workspace/zhesi')

# 从 daojia/index.html 提取原始页面 CSS（:root 到 @media 结束）
ORIGINAL_PAGE_CSS = """
    :root { --ink: #1a1208; --ink-light: #4a3f2f; --paper: #f5f0e6; --vermilion: #b83a2e; --gold: #a67c52; --muted: #8a7a68; --border: #d4c9b8; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    ::selection { background: var(--vermilion); color: var(--paper); }
    html { scroll-behavior: smooth; }
    body { font-family: "Noto Serif SC", serif; background: var(--paper); color: var(--ink); line-height: 2.2; }
    body::before { content: ''; position: fixed; inset: 0; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='0.02'/%3E%3C/svg%3E"); pointer-events: none; z-index: 0; }
    .side-rule { position: fixed; left: 44px; top: 0; bottom: 0; width: 1px; background: linear-gradient(to bottom, transparent, var(--border) 12%, var(--border) 88%, transparent); z-index: 1; }
    .side-rule::before { content: ''; position: absolute; top: 50%; left: -3px; width: 7px; height: 7px; background: var(--vermilion); border-radius: 50%; transform: translateY(-50%); }
    .hero { min-height: 80vh; display: flex; flex-direction: column; justify-content: center; padding: 0 80px; position: relative; overflow: hidden; }
    .hero::after { content: '道'; position: absolute; right: -30px; top: 50%; transform: translateY(-50%); font-family: "ZCOOL XiaoWei", serif; font-size: 42vw; color: var(--ink); opacity: 0.022; line-height: 1; pointer-events: none; }
    .hero-label { font-size: 0.68rem; letter-spacing: 0.45em; color: var(--muted); margin-bottom: 28px; opacity: 0; animation: fadeUp 0.8s ease forwards 0.25s; }
    .hero-title { font-family: "ZCOOL XiaoWei", serif; font-size: clamp(3rem, 6vw, 5.5rem); font-weight: 400; letter-spacing: 0.18em; line-height: 1.1; margin-bottom: 20px; opacity: 0; animation: fadeUp 0.9s ease forwards 0.4s; }
    .hero-sub { font-size: 0.82rem; color: var(--muted); letter-spacing: 0.28em; margin-bottom: 0; opacity: 0; animation: fadeUp 0.8s ease forwards 0.6s; }
    .cards-area { position: relative; z-index: 1; max-width: 1100px; margin: 0 auto; padding: 72px 48px 80px; }
    .cards-header { font-size: 0.62rem; letter-spacing: 0.4em; color: var(--muted); margin-bottom: 32px; padding-bottom: 14px; border-bottom: 1px solid var(--border); }
    .cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
    .card { background: rgba(247,242,232,0.7); border: 1px solid var(--border); border-radius: 4px; padding: 28px 24px; text-decoration: none; color: var(--ink); display: block; transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s; opacity: 0; animation: fadeUp 0.7s ease forwards; }
    .card:hover { transform: translateY(-3px); box-shadow: 0 8px 28px rgba(0,0,0,0.08); border-color: var(--vermilion); }
    .card:nth-child(1) { animation-delay: 0.1s; }
    .card:nth-child(2) { animation-delay: 0.18s; }
    .card:nth-child(3) { animation-delay: 0.26s; }
    .card:nth-child(4) { animation-delay: 0.34s; }
    .card:nth-child(5) { animation-delay: 0.42s; }
    .card:nth-child(6) { animation-delay: 0.50s; }
    .card:nth-child(7) { animation-delay: 0.58s; }
    .card-title { font-family: "ZCOOL XiaoWei", serif; font-size: 1.25rem; letter-spacing: 0.1em; color: var(--ink); margin-bottom: 8px; }
    .card-en { font-size: 0.62rem; letter-spacing: 0.2em; color: var(--gold); margin-bottom: 14px; }
    .card-desc { font-size: 0.83rem; line-height: 1.9; color: var(--ink-light); }
    footer { position: relative; z-index: 1; margin-top: 40px; padding: 32px 80px; border-top: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
    footer .brand { font-family: "ZCOOL XiaoWei", serif; font-size: 1.1rem; letter-spacing: 0.18em; }
    footer .copy { font-size: 0.72rem; color: var(--muted); letter-spacing: 0.1em; }
    @keyframes fadeUp { to { opacity: 1; transform: translateY(0); } }
    @media (max-width: 860px) { .hero { padding: 0 24px; } .side-rule { left: 14px; } .cards-area { padding: 48px 20px 60px; } footer { padding: 24px 20px; flex-direction: column; gap: 8px; text-align: center; } }
    @media (max-width: 480px) { .side-rule { display: none; } }
"""

# 统一的浮动导航 CSS
FLOAT_NAV_CSS = ".float-nav{position:fixed;bottom:28px;right:28px;z-index:100}.float-nav-btn{width:44px;height:44px;border-radius:50%;background:#1a1208;color:#f5f0e6;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 16px rgba(0,0,0,.3);transition:transform .2s,background .2s}.float-nav-btn:hover{background:#8b3a2e;transform:scale(1.08)}.float-nav-panel{display:none;position:absolute;bottom:52px;right:0;background:#2c2416;border-radius:14px;padding:0;min-width:240px;max-height:65vh;overflow-y:auto;box-shadow:0 12px 40px rgba(0,0,0,.45)}.float-nav.open .float-nav-panel{display:block;animation:fadeUp .2s ease}.float-nav-panel::-webkit-scrollbar{width:3px}.float-nav-panel::-webkit-scrollbar-thumb{background:rgba(166,124,82,.35);border-radius:2px}.float-nav-header{padding:14px 16px 12px;border-bottom:1px solid rgba(166,124,82,.2)}.float-nav-header-title{font-family:\"ZCOOL XiaoWei\",serif;font-size:.9rem;color:#a67c52;letter-spacing:.1em}.float-nav-section{margin:0}.float-nav-section-btn{display:flex;align-items:center;justify-content:space-between;width:100%;padding:9px 16px;background:none;border:none;border-top:1px solid rgba(166,124,82,.12);cursor:pointer;color:#c4b49a;font-size:.82rem;font-family:\"Noto Serif SC\",serif;text-align:left;transition:background .15s,color .15s}.float-nav-section-btn:hover{background:rgba(139,58,46,.2);color:#f5f0e6}.float-nav-section-btn .arrow{font-size:.6rem;transition:transform .25s;margin-left:8px;color:#7a6a58}.float-nav-section-btn.open .arrow{transform:rotate(180deg)}.float-nav-items{display:none;padding:4px 0 8px;background:rgba(0,0,0,.15)}.float-nav-items.open{display:block}.float-nav-item{display:block;padding:5px 16px 5px 22px;font-size:.78rem;color:#9a8b7a;text-decoration:none;transition:background .12s,color .12s;white-space:nowrap}.float-nav-item:hover{background:rgba(139,58,46,.2);color:#f0e8d8}.float-nav-item.active{color:#c47a5a;font-weight:600}"

NAV_HTML_ZHUANGZI = """
    <!-- 浮动导航 -->
  <div class="float-nav" id="floatNav">
  <button class="float-nav-btn" onclick="toggleFloatNav()" title="哲思经典导航">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
  </button>
  <div class="float-nav-panel" id="floatNavPanel">
    <div class="float-nav-header">
      <div class="float-nav-header-title">哲思经典</div>
    </div>

    <div class="float-nav-section">
      <button class="float-nav-section-btn" onclick="toggleSection(this)">
        <span>庄子·内篇（7篇）</span>
        <span class="arrow">&#9660;</span>
      </button>
      <div class="float-nav-items">
        <a class="float-nav-item" href="xiaoyao-you.html">逍遥游</a>
        <a class="float-nav-item" href="qi-wu-lun.html">齐物论</a>
        <a class="float-nav-item" href="yang-sheng-zhu.html">养生主</a>
        <a class="float-nav-item" href="ren-jian-shi.html">人间世</a>
        <a class="float-nav-item" href="de-chong-fu.html">德充符</a>
        <a class="float-nav-item" href="da-zong-shi.html">大宗师</a>
        <a class="float-nav-item" href="ying-di-wang.html">应帝王</a>
      </div>
    </div>

    <div class="float-nav-section">
      <button class="float-nav-section-btn" onclick="toggleSection(this)">
        <span>庄子·外篇（15篇）</span>
        <span class="arrow">&#9660;</span>
      </button>
      <div class="float-nav-items">
        <a class="float-nav-item" href="pian-mu.html">骈拇</a>
        <a class="float-nav-item" href="ma-ti.html">马蹄</a>
        <a class="float-nav-item" href="qu-qie.html">胠箧</a>
        <a class="float-nav-item" href="zai-you.html">在宥</a>
        <a class="float-nav-item" href="tian-di.html">天地</a>
        <a class="float-nav-item" href="tian-dao.html">天道</a>
        <a class="float-nav-item" href="tian-yun.html">天运</a>
        <a class="float-nav-item" href="ke-yi.html">刻意</a>
        <a class="float-nav-item" href="shan-xing.html">缮性</a>
        <a class="float-nav-item" href="qiu-shui.html">秋水</a>
        <a class="float-nav-item" href="zhi-le.html">至乐</a>
        <a class="float-nav-item" href="da-sheng.html">达生</a>
        <a class="float-nav-item" href="shan-mu.html">山木</a>
        <a class="float-nav-item" href="tian-zi-fang.html">田子方</a>
        <a class="float-nav-item" href="zhi-bei-you.html">知北游</a>
      </div>
    </div>

    <div class="float-nav-section">
      <button class="float-nav-section-btn" onclick="toggleSection(this)">
        <span>庄子·杂篇（11篇）</span>
        <span class="arrow">&#9660;</span>
      </button>
      <div class="float-nav-items">
        <a class="float-nav-item" href="geng-sang-chu.html">庚桑楚</a>
        <a class="float-nav-item" href="xu-wu-gui.html">徐无鬼</a>
        <a class="float-nav-item" href="ze-yang.html">则阳</a>
        <a class="float-nav-item" href="wai-wu.html">外物</a>
        <a class="float-nav-item" href="yu-yan.html">寓言</a>
        <a class="float-nav-item" href="rang-wang.html">让王</a>
        <a class="float-nav-item" href="dao-zhi.html">盗跖</a>
        <a class="float-nav-item" href="shuo-jian.html">说剑</a>
        <a class="float-nav-item" href="yu-fu.html">渔父</a>
        <a class="float-nav-item" href="lie-yu-kou.html">列御寇</a>
        <a class="float-nav-item" href="tian-xia.html">天下</a>
      </div>
    </div>

    <div class="float-nav-section">
      <button class="float-nav-section-btn" onclick="toggleSection(this)">
        <span>道家经典（7篇）</span>
        <span class="arrow">&#9660;</span>
      </button>
      <div class="float-nav-items">
        <a class="float-nav-item" href="daojia/index.html">导航页</a>
        <a class="float-nav-item" href="daojia/qing-jing-jing.html">太上老君说常清静经</a>
        <a class="float-nav-item" href="daojia/taiyi-jinhua.html">太乙金华宗旨</a>
        <a class="float-nav-item" href="daojia/dao-de-jing.html">道德经</a>
        <a class="float-nav-item" href="daojia/wen-zi.html">文子</a>
        <a class="float-nav-item" href="daojia/lie-zi.html">列子</a>
        <a class="float-nav-item" href="daojia/huainan-zi.html">淮南子</a>
        <a class="float-nav-item" href="daojia/bao-pu-zi.html">抱朴子</a>
      </div>
    </div>
  </div>
</div>"""

NAV_HTML_DAOJIA = """
    <!-- 浮动导航 -->
  <div class="float-nav" id="floatNav">
  <button class="float-nav-btn" onclick="toggleFloatNav()" title="哲思经典导航">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
  </button>
  <div class="float-nav-panel" id="floatNavPanel">
    <div class="float-nav-header">
      <div class="float-nav-header-title">哲思经典</div>
    </div>

    <div class="float-nav-section">
      <button class="float-nav-section-btn" onclick="toggleSection(this)">
        <span>庄子·内篇（7篇）</span>
        <span class="arrow">&#9660;</span>
      </button>
      <div class="float-nav-items">
        <a class="float-nav-item" href="../xiaoyao-you.html">逍遥游</a>
        <a class="float-nav-item" href="../qi-wu-lun.html">齐物论</a>
        <a class="float-nav-item" href="../yang-sheng-zhu.html">养生主</a>
        <a class="float-nav-item" href="../ren-jian-shi.html">人间世</a>
        <a class="float-nav-item" href="../de-chong-fu.html">德充符</a>
        <a class="float-nav-item" href="../da-zong-shi.html">大宗师</a>
        <a class="float-nav-item" href="../ying-di-wang.html">应帝王</a>
      </div>
    </div>

    <div class="float-nav-section">
      <button class="float-nav-section-btn" onclick="toggleSection(this)">
        <span>庄子·外篇（15篇）</span>
        <span class="arrow">&#9660;</span>
      </button>
      <div class="float-nav-items">
        <a class="float-nav-item" href="../pian-mu.html">骈拇</a>
        <a class="float-nav-item" href="../ma-ti.html">马蹄</a>
        <a class="float-nav-item" href="../qu-qie.html">胠箧</a>
        <a class="float-nav-item" href="../zai-you.html">在宥</a>
        <a class="float-nav-item" href="../tian-di.html">天地</a>
        <a class="float-nav-item" href="../tian-dao.html">天道</a>
        <a class="float-nav-item" href="../tian-yun.html">天运</a>
        <a class="float-nav-item" href="../ke-yi.html">刻意</a>
        <a class="float-nav-item" href="../shan-xing.html">缮性</a>
        <a class="float-nav-item" href="../qiu-shui.html">秋水</a>
        <a class="float-nav-item" href="../zhi-le.html">至乐</a>
        <a class="float-nav-item" href="../da-sheng.html">达生</a>
        <a class="float-nav-item" href="../shan-mu.html">山木</a>
        <a class="float-nav-item" href="../tian-zi-fang.html">田子方</a>
        <a class="float-nav-item" href="../zhi-bei-you.html">知北游</a>
      </div>
    </div>

    <div class="float-nav-section">
      <button class="float-nav-section-btn" onclick="toggleSection(this)">
        <span>庄子·杂篇（11篇）</span>
        <span class="arrow">&#9660;</span>
      </button>
      <div class="float-nav-items">
        <a class="float-nav-item" href="../geng-sang-chu.html">庚桑楚</a>
        <a class="float-nav-item" href="../xu-wu-gui.html">徐无鬼</a>
        <a class="float-nav-item" href="../ze-yang.html">则阳</a>
        <a class="float-nav-item" href="../wai-wu.html">外物</a>
        <a class="float-nav-item" href="../yu-yan.html">寓言</a>
        <a class="float-nav-item" href="../rang-wang.html">让王</a>
        <a class="float-nav-item" href="../dao-zhi.html">盗跖</a>
        <a class="float-nav-item" href="../shuo-jian.html">说剑</a>
        <a class="float-nav-item" href="../yu-fu.html">渔父</a>
        <a class="float-nav-item" href="../lie-yu-kou.html">列御寇</a>
        <a class="float-nav-item" href="../tian-xia.html">天下</a>
      </div>
    </div>

    <div class="float-nav-section">
      <button class="float-nav-section-btn" onclick="toggleSection(this)">
        <span>道家经典（7篇）</span>
        <span class="arrow">&#9660;</span>
      </button>
      <div class="float-nav-items">
        <a class="float-nav-item" href="index.html">导航页</a>
        <a class="float-nav-item" href="qing-jing-jing.html">太上老君说常清静经</a>
        <a class="float-nav-item" href="taiyi-jinhua.html">太乙金华宗旨</a>
        <a class="float-nav-item" href="dao-de-jing.html">道德经</a>
        <a class="float-nav-item" href="wen-zi.html">文子</a>
        <a class="float-nav-item" href="lie-zi.html">列子</a>
        <a class="float-nav-item" href="huainan-zi.html">淮南子</a>
        <a class="float-nav-item" href="bao-pu-zi.html">抱朴子</a>
      </div>
    </div>
  </div>
</div>"""

NEW_JS = """<script>
    function toggleFloatNav(){document.getElementById('floatNav').classList.toggle('open')}
    function toggleSection(btn){
      var items = btn.nextElementSibling;
      var isOpen = btn.classList.contains('open');
      document.querySelectorAll('.float-nav-section-btn').forEach(function(b){b.classList.remove('open')});
      document.querySelectorAll('.float-nav-items').forEach(function(i){i.classList.remove('open')});
      if(!isOpen){btn.classList.add('open');items.classList.add('open')}
    }
    document.addEventListener('click',function(e){var nav=document.getElementById('floatNav');if(!nav.contains(e.target))nav.classList.remove('open')})
</script>"""

# 完整的 style 块（原始页面 CSS + 浮动导航 CSS）
COMBINED_CSS = "<style>\n" + ORIGINAL_PAGE_CSS + "\n    " + FLOAT_NAV_CSS + "\n  </style>"


def fix_file(filepath):
    """修复单个 HTML 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    rel = str(filepath.relative_to(BASE))
    is_daojia_chapter = str(rel).startswith('daojia/') and filepath.name != 'index.html'

    # 1. 替换 <style> 块为完整 CSS
    style_pattern = re.compile(r'<style[^>]*>[\s\S]*?</style>')
    if style_pattern.search(content):
        content = style_pattern.sub(COMBINED_CSS, content)
    else:
        # 找不到 style 块，在 </head> 前插入
        content = content.replace('</head>', COMBINED_CSS + '\n</head>')

    # 2. 移除旧的 float-nav HTML
    old_nav_pattern = re.compile(
        r'\s*<!--[^-]*浮动导航[^-]*-->[\s]*<div class="float-nav"[^>]*>[\s\S]*?</div>\s*</div>\s*',
    )
    content = old_nav_pattern.sub('', content)

    # 3. 插入新的 nav HTML（在 </div><footer 或 </body> 前面）
    nav_html = NAV_HTML_DAOJIA if is_daojia_chapter else NAV_HTML_ZHUANGZI

    m = re.search(r'(</div>)(\s*)(<footer)', content)
    if m:
        content = content[:m.end(1)] + nav_html + m.group(2) + m.group(3) + content[m.end(3):]
    else:
        m2 = re.search(r'(</div>)(\s*)(</body>)', content)
        if m2:
            content = content[:m2.end(1)] + nav_html + m2.group(2) + m2.group(3) + content[m2.end(3):]

    # 4. 替换 JS
    old_js = re.compile(r'<script>[\s\S]*?toggleFloatNav[\s\S]*?</script>')
    content = old_js.sub(NEW_JS, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    updated = []
    for f in sorted(list(BASE.glob('*.html')) + list((BASE / 'daojia').glob('*.html'))):
        try:
            if fix_file(f):
                updated.append(str(f.relative_to(BASE)))
        except Exception as e:
            print(f"Error {f.name}: {e}")

    print(f"Rebuilt {len(updated)} files")
    for f in updated:
        print(f"  {f}")


if __name__ == '__main__':
    main()
