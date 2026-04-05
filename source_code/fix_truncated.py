#!/usr/bin/env python3
"""修复被截断的 HTML 文件，补上缺失的 footer 和结束标签"""

import re
from pathlib import Path

BASE = Path('/Users/rick/.openclaw/workspace/zhesi')

# 统一的浮动导航 HTML（庄子根目录）
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

TAIL_TEMPLATE_ZHUANGZI = """
<footer>
    <div class="brand">庄子 · 全文导航</div>
    <div class="copy">OpenClaw 整理 &nbsp;·&nbsp; 2026</div>
  </footer>

  <script>
    const observer = new IntersectionObserver((entries) => { entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('visible'); }); }, { threshold: 0.08 });
    document.querySelectorAll('[data-reveal]').forEach(el => observer.observe(el));
  </script>
""" + NEW_JS + """
</body>
</html>"""

TAIL_TEMPLATE_DAOJIA = """
<footer>
    <div class="brand">道家经典</div>
    <div class="copy">OpenClaw 整理 &nbsp;·&nbsp; 2026</div>
  </footer>

  <script>
    const observer = new IntersectionObserver((entries) => { entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('visible'); }); }, { threshold: 0.08 });
    document.querySelectorAll('[data-reveal]').forEach(el => observer.observe(el));
  </script>
""" + NEW_JS + """
</body>
</html>"""


def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查文件是否被截断（没有 </body></html>）
    if '</body>' in content and '</html>' in content:
        return False  # 没问题，跳过

    rel = str(filepath.relative_to(BASE))
    is_daojia = str(rel).startswith('daojia/')

    nav_html = NAV_HTML_DAOJIA if is_daojia else NAV_HTML_ZHUANGZI
    tail = TAIL_TEMPLATE_DAOJIA if is_daojia else TAIL_TEMPLATE_ZHUANGZI

    # 移除已有的截断的 nav HTML（可能在文件末尾）
    content = content.rstrip()
    if content.endswith('</div>'):
        # 去掉末尾的 </div>（这是 float-nav-panel 的闭合）
        # 找到这个 </div> 属于 nav
        content = content.rstrip()
        if content.endswith('</div>'):
            content = content[:-6].rstrip()

    # 在末尾追加 nav + footer + js + body/html
    fixed = content + '\n' + nav_html + '\n' + tail

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed)
    return True


def main():
    updated = []
    for f in sorted(list(BASE.glob('*.html')) + list((BASE / 'daojia').glob('*.html'))):
        try:
            if fix_file(f):
                updated.append(str(f.relative_to(BASE)))
        except Exception as e:
            print(f"Error {f.name}: {e}")

    print(f"Fixed {len(updated)} truncated files")
    for f in updated:
        print(f"  {f}")


if __name__ == '__main__':
    main()
