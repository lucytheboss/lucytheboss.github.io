import re

with open('index.html', 'r') as f:
    content = f.read()

root_vars = """
:root {
  --fs-base: 16px;
  --fs-cap: 14px;
}
@media (max-width: 980px) {
  :root {
    --fs-base: 14px;
    --fs-cap: 12px;
  }
}
"""

if '--fs-base' not in content:
    content = content.replace("/* ── BASE ── */", root_vars + "\n/* ── BASE ── */")

def replace_size(m):
    size = int(m.group(1))
    if size <= 12:
        return 'font-size: var(--fs-cap);'
    elif size <= 16:
        return 'font-size: var(--fs-base);'
    return m.group(0)

# Replace all occurrences of `font-size: <number>px;`
# taking care of optional spaces
content = re.sub(r'font-size:\s*(\d+)px;', replace_size, content)

with open('index.html', 'w') as f:
    f.write(content)

print("Font sizes rewritten successfully!")
