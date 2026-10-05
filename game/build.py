"""Build a single self-contained game file for publishing.

Inlines the background photos and, if present, the test-only hero art
(hero-art.js is git-ignored). Output: dist/level1.html (also git-ignored).
"""
import base64, os

here = os.path.dirname(os.path.abspath(__file__))
html = open(os.path.join(here, 'level1.html')).read()

art = os.path.join(here, 'hero-art.js')
tag = '<script src="hero-art.js"></script>'
html = html.replace(tag, '<script>\n' + open(art).read() + '</script>' if os.path.exists(art) else '')

for name in ('kitchen', 'pantry', 'sink'):
    path = 'assets/bg-%s.jpg' % name
    data = base64.b64encode(open(os.path.join(here, path), 'rb').read()).decode()
    html = html.replace("'%s'" % path, "'data:image/jpeg;base64,%s'" % data)

os.makedirs(os.path.join(here, 'dist'), exist_ok=True)
out = os.path.join(here, 'dist', 'level1.html')
open(out, 'w').write(html)
print('wrote', out, '%d KB' % (len(html) // 1024))
