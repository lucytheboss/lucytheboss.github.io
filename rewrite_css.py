import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Replace tokens
old_tokens = r"""\[data-theme="light"\] \{
  --bg:         #F2F2F2;
  --bg2:        #FFFFFF;
  --surface:    #FFFFFF;
  --ink:        #404040;
  --ink2:       #595959;
  --ink3:       #808080;
  --line:       #BFA38A;
  --line-bold:  #404040;
  --accent1:    #F20519;
  --accent2:    #F22248;
  --accent1-glow: rgba\(242, 5, 25, 0\.15\);
  --accent2-glow: rgba\(242, 34, 72, 0\.15\);
  --tog-bg:     #404040;
  --tog-fg:     #F2F2F2;
\}
\[data-theme="dark"\] \{
  --bg:         #1A1A1A;
  --bg2:        #242424;
  --surface:    #2A2A2A;
  --ink:        #F2F2F2;
  --ink2:       #D9D9D9;
  --ink3:       #A6A6A6;
  --line:       #BFA38A;
  --line-bold:  #F2F2F2;
  --accent1:    #F20519;
  --accent2:    #F22248;
  --accent1-glow: rgba\(242, 5, 25, 0\.2\);
  --accent2-glow: rgba\(242, 34, 72, 0\.2\);
  --tog-bg:     #F2F2F2;
  --tog-fg:     #1A1A1A;
\}"""

new_tokens = """[data-theme="light"] {
  --bg:         #F2F2F2;
  --bg2:        #FFFFFF;
  --surface:    #FFFFFF;
  --ink:        #404040;
  --ink2:       #7A7A7A;
  --line:       #BFA38A;
  --line-bold:  #BFA38A;
  --accent1:    #FE22FF;
  --accent2:    #FAE75C;
  --tog-bg:     #404040;
  --tog-fg:     #F2F2F2;
}
[data-theme="dark"] {
  --bg:         #1A1A1A;
  --bg2:        #404040;
  --surface:    #404040;
  --ink:        #F2F2F2;
  --ink2:       #BFA38A;
  --line:       #555555;
  --line-bold:  #555555;
  --accent1:    #FAE75C;
  --accent2:    #FE22FF;
  --tog-bg:     #F2F2F2;
  --tog-fg:     #1A1A1A;
}"""

content = re.sub(old_tokens, new_tokens, content)

# Remove any usages of --ink3 since we removed it, replacing with --ink2
content = content.replace('var(--ink3)', 'var(--ink2)')

# 2. Box shadows
content = content.replace('box-shadow: 0 4px 12px rgba(0,0,0,0.2);', 'box-shadow: 0 4px 16px rgba(0,0,0,0.08);')
content = content.replace('box-shadow: 0 6px 16px rgba(0,0,0,0.3);', 'box-shadow: 0 8px 24px rgba(0,0,0,0.12);')
content = content.replace('box-shadow: 0 2px 8px rgba(0,0,0,0.1);', 'box-shadow: 0 2px 8px rgba(0,0,0,0.05);')
content = content.replace('box-shadow: 6px 6px 0 var(--line-bold);', 'box-shadow: 0 12px 32px rgba(0,0,0,0.05);')
content = content.replace('box-shadow: 4px 4px 0 var(--line-bold);', 'box-shadow: 0 8px 24px rgba(0,0,0,0.05);')
content = content.replace('box-shadow: 12px 12px 0 var(--accent2);', 'box-shadow: 0 24px 64px rgba(0,0,0,0.15);')
content = content.replace('box-shadow: 8px 8px 0 rgba(0,0,0,0.5);', 'box-shadow: 0 16px 40px rgba(0,0,0,0.1);')
content = content.replace('box-shadow: 6px 6px 0 var(--accent2);', 'box-shadow: 0 12px 32px rgba(0,0,0,0.15);')

# 3. Gradients & glows
# hero name gradient
content = re.sub(r'background: linear-gradient\(90deg, var\(--accent1\), var\(--accent2\)\);\n\s+-webkit-background-clip: text; -webkit-text-fill-color: transparent;', 'color: var(--accent1);', content)

# img-main::after (delete the whole rule)
content = re.sub(r'\.img-main::after \{\s*content:\'\'[^\}]+\}\n?', '', content)
# ux-img::before (delete the whole rule)
content = re.sub(r'\.ux-img::before \{[^\}]+\}\n?', '', content)

# 4. Hardcoded black/white colors that should use vars
# .insight-band
content = content.replace('border-bottom: 2px solid var(--line-bold); background: var(--accent1); color: #000;', 'border-bottom: 2px solid var(--line-bold); background: var(--accent1); color: var(--bg);')
# wait, if background is magenta/yellow, we should just use var(--ink) or var(--bg) to let them pop. If accent1 is Magenta in Light (#FE22FF) and Yellow in Dark (#FAE75C).
# Actually, the user says "Let the solid Magenta and Yellow colors stand on their own."
content = content.replace('border-right: 2px solid #000;', 'border-right: 2px solid var(--line-bold);')
content = content.replace('border-bottom: 2px solid #000;', 'border-bottom: 2px solid var(--line-bold);')
content = content.replace('color: #000;', 'color: var(--ink);')
content = content.replace('color: #fff;', 'color: var(--bg);')
content = content.replace('background: #000;', 'background: var(--ink);')
content = content.replace('background: #fff;', 'background: var(--bg);')
content = content.replace('border: 2px solid #000;', 'border: 2px solid var(--line-bold);')

# rgba fixes
content = content.replace('color: rgba(0,0,0,0.8);', 'color: var(--ink);')
content = content.replace('color: rgba(255,255,255,0.7);', 'color: var(--ink2);')
content = content.replace('color: rgba(255,255,255,0.9);', 'color: var(--bg);')
content = content.replace('color: rgba(255,255,255,0.6);', 'color: var(--ink2);')

# border colors hardcoded
content = content.replace('-webkit-text-stroke: 0.5px #000;', '-webkit-text-stroke: 0.5px var(--ink);')

# Write back
with open('index.html', 'w') as f:
    f.write(content)
