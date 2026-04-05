import os

base = "/Users/rick/.openclaw/workspace/zhesi"
daojia = os.path.join(base, "daojia")

for d in [base, daojia]:
    if not os.path.exists(d):
        continue
    for fname in os.listdir(d):
        if not fname.endswith(".html"):
            continue
        fpath = os.path.join(d, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        if "float-nav-items{display:none}" in content:
            continue
        if ".float-nav-items.open{display:block}" in content:
            content = content.replace(
                ".float-nav-items.open{display:block}",
                ".float-nav-items{display:none}\n    .float-nav-items.open{display:block}"
            )
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Fixed: {fname}")
        else:
            print(f"Missing rule in: {fname}")

print("Done!")
