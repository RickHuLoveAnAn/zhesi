import os, re

base = "/Users/rick/.openclaw/workspace/zhesi"
daojia = os.path.join(base, "daojia")

# Fix: change CSS selector from ".float-nav.open .float-nav-items" to ".float-nav-items.open"
fix_css = ".float-nav.open .float-nav-items{display:block}"

for d in [base, daojia]:
    if not os.path.exists(d):
        continue
    for fname in os.listdir(d):
        if not fname.endswith(".html"):
            continue
        fpath = os.path.join(d, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        if fix_css not in content:
            continue
        # Fix CSS: .float-nav.open .float-nav-items {display:block} -> .float-nav-items.open {display:block}
        new_content = content.replace(fix_css, ".float-nav-items.open{display:block}")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Fixed: {fname}")

print("Done!")
