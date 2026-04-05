import os

base = "/Users/rick/.openclaw/workspace/zhesi"
daojia = os.path.join(base, "daojia")

css_rule = ".float-nav-items.open{display:block}"

for d in [base, daojia]:
    if not os.path.exists(d):
        continue
    for fname in os.listdir(d):
        if not fname.endswith(".html"):
            continue
        fpath = os.path.join(d, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        if ".float-nav-items.open" in content:
            print(f"Already has rule: {fname}")
            continue
        # Find where to insert: after ".float-nav.open .float-nav-panel" rule
        target = ".float-nav.open .float-nav-panel { display: block; animation: fadeUp 0.2s ease; }"
        if target not in content:
            # Try to find any .float-nav.open rule
            import re
            m = re.search(r'\.float-nav\.open[^{]+\{[^}]+\}', content)
            if m:
                old = m.group()
                new = old + "\n    " + css_rule
                content = content.replace(old, new)
                print(f"Fixed (regex): {fname}")
            else:
                print(f"Could not find target in: {fname}")
                continue
        else:
            content = content.replace(target, target + "\n    " + css_rule)
            print(f"Added rule: {fname}")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)

print("Done!")
