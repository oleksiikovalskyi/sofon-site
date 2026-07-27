"""Збирає сторінки-варіанти шапки й випадаючої частини з home-ab/f.html.

Варіанти відрізняються лише атрибутами на <body> і (для cta-*) розміткою
випадаючої панелі, тож тримати п'ять майже однакових копій руками не варто —
після кожної правки f.html просто перезапусти:  py home-ab/gen-nav.py
"""
import io
import re
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = io.open(os.path.join(ROOT, 'f.html'), encoding='utf-8').read()


def icon(name):
    """Дістає готову іконку з розмітки f.html, щоб не дублювати SVG у коді."""
    m = re.search(r'href="[^"]*' + name + r'[^"]*">\s*(<svg.*?</svg>)', SRC, re.S)
    return m.group(1) if m else ''


TEL, MAIL = icon('tel:'), icon('mailto:')
VIB, TG, WA = icon('viber'), icon(r't\.me'), icon(r'wa\.me')
PIN = icon('/contact/')
NUM = '+380 67 293 30 66'
WARN = '<!-- ⚠ ПЕРЕВІРИТИ У ВЛАСНИКА: чи читають ці канали на цьому номері -->'

ROWS = """<div class="cta-pop" id="cta-pop" role="menu">
          <a class="cta-i" role="menuitem" href="tel:+380672933066">%s
            <span class="t"><b>Зателефонувати</b><span>%s</span></span>
          </a>
          <a class="cta-i" role="menuitem" href="mailto:les@immach.com">%s
            <span class="t"><b>Написати на пошту</b><span>les@immach.com</span></span>
          </a>
          %s
          <div class="cta-msg">
            <div class="cta-chips">
              <a class="cta-c" role="menuitem" href="viber://chat?number=%%2B380672933066">%sViber</a>
              <a class="cta-c" role="menuitem" href="https://t.me/+380672933066">%sTelegram</a>
              <a class="cta-c" role="menuitem" href="https://wa.me/380672933066">%sWhatsApp</a>
            </div>
          </div>
          <a class="cta-i cta-i--addr" role="menuitem" href="/contact/">%s
            <span class="t"><b>Приїхати до нас</b><span>Київ, вул. Бориспільська, 9, корп. 111</span></span>
          </a>
        </div>""" % (TEL, NUM, MAIL, WARN, VIB, TG, WA, PIN)

# Компоновка у дві колонки тепер базова — вона лежить прямо у f.html,
# тож окремої сторінки під неї не треба.

# name, підпис у смузі, атрибути body, розмітка панелі (None = як у f.html)
PAGES = [
    ('blend',    'Темна напівпрозора над героєм', 'data-nav="blend"', None),
    ('glass',    'Прозора над героєм',            'data-nav="glass"', None),
    ('dark',     'Темна завжди',                  'data-nav="dark"',  None),
    ('cta-rows', 'Месенджери трьома кнопками',    'data-nav="blend" data-cta="rows"', ROWS),
]
NAV = [p for p in PAGES if not p[0].startswith('cta-')]
CTA = [p for p in PAGES if p[0].startswith('cta-')]

os.makedirs(os.path.join(ROOT, 'nav'), exist_ok=True)
for name, label, attrs, pop in PAGES:
    s = SRC.replace('<body data-page="home"', '<body data-page="home" ' + attrs)
    if pop:
        s = re.sub(r'<div class="cta-pop" id="cta-pop" role="menu">.*?\n        </div>',
                   lambda m: pop, s, count=1, flags=re.S)
    group = CTA if pop else NAV
    kind = 'ВИПАДАЮЧА ЧАСТИНА' if pop else 'ШАПКА'
    links = ' '.join('<a href="/home-ab/nav/%s.html">%s</a>' % (n, l)
                     for n, l, _, _ in group if n != name)
    tail = ('<a href="/home-ab/nav/blend.html">дві колонки (базова)</a>' if pop
            else '<a href="/home-ab/f.html">світла (як зараз)</a>')
    bar = '<div class="proto-bar">%s · <b>%s</b> · %s %s</div>' % (kind, label, links, tail)
    s = re.sub(r'<div class="proto-bar">.*?</div>', lambda m: bar, s, count=1, flags=re.S)
    s = s.replace('<title>F ·', '<title>%s ·' % label)
    io.open(os.path.join(ROOT, 'nav', name + '.html'), 'w', encoding='utf-8').write(s)
    print('nav/%s.html' % name)
