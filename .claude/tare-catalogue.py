# -*- coding: utf-8 -*-
"""Каталог типів тари — силуети з укупоркою, ковпачками й етикетками.

Навіщо окремо від `bottle-ruler.py`. Лінійка малює НАШІ заміряні формати:
кожен силует там стоїть за реальними H/A/B із бази, і підпис — реальний об'єм.
Цей файл про інше: показати ШИРИНУ типів тари, з якими працює оснастка —
від пивної кронен-пробки до помпи на рідкому милі. Тут розміри типові для
категорії, а не наші заміри, і жодна позиція не стверджує «ми робили саме цю».
Дві різні заяви, тому й два різні файли: щоб ілюстрація ніколи не поїхала
в блок, який має бути фактом.

Що вміє: корпуси за категоріями напою/продукту, укупорка надіта (кронен,
твіст-офф, дозатор-носик, гвинтовий алюмінієвий, ПЕТ, помпа, фліп-топ),
термоусадковий ковпачок, мюзле, наклеєні етикетки (корпусна й кільєретка).

Запуск: py .claude/tare-catalogue.py
Пише:   lab/tare.html
"""
import io, os, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "lab", "tare.html")
K = 0.62                      # мм -> px


def X(v):
    return round(v * K, 2)


def Y(h, v):
    return round((h - v) * K, 2)


def mirror(h, n):
    """Замкнений контур із правої половини (вузли (x, y, ctrl) знизу вгору)."""
    d = ["M %s %s" % (X(-n[0][0]), Y(h, n[0][1])), "L %s %s" % (X(n[0][0]), Y(h, n[0][1]))]
    for x, y, c in n[1:]:
        d.append("Q %s %s %s %s" % (X(c[0]), Y(h, c[1]), X(x), Y(h, y)) if c
                 else "L %s %s" % (X(x), Y(h, y)))
    d.append("L %s %s" % (X(-n[-1][0]), Y(h, n[-1][1])))
    for i in range(len(n) - 1, 0, -1):
        x, y, c = n[i - 1][0], n[i - 1][1], n[i][2]
        d.append("Q %s %s %s %s" % (X(-c[0]), Y(h, c[1]), X(-x), Y(h, y)) if c
                 else "L %s %s" % (X(-x), Y(h, y)))
    d.append("Z")
    return " ".join(d)


# ---------------------------------------------------------------------------
# КОРПУСИ. Кожен — список вузлів правої половини знизу вгору; повертає також
# півширину горла, щоб укупорка сіла точно на нього.
# ---------------------------------------------------------------------------

def body(kind, h, a):
    half, heel = a / 2, min(a / 2 * 0.15, h * 0.025)

    if kind == "beer":                       # довга шийка, циліндр
        nw, sh = min(half * 0.28, 12), h * 0.46
        n = [(half - heel, 0, None), (half, heel, (half, 0)), (half, sh, None),
             (nw, sh + h * 0.22, (half * .9, sh + h * .16)), (nw, h, None)]
    elif kind == "bordeaux":                 # різке плече
        nw, sh = min(half * 0.31, 14), h * 0.58
        n = [(half - heel, 0, None), (half, heel, (half, 0)), (half, sh, None),
             (nw, sh + h * 0.15, (half * .93, sh + h * .11)), (nw, h, None)]
    elif kind == "burgundy":                 # суцільна дуга
        nw = min(half * 0.33, 15)
        n = [(half - heel, 0, None), (half, heel, (half, 0)), (half, h * 0.40, None),
             (nw, h * 0.82, (half, h * 0.70)), (nw, h, None)]
    elif kind == "sparkling":                # товсте похиле плече
        nw = min(half * 0.32, 15)
        n = [(half - heel, 0, None), (half, heel, (half, 0)), (half, h * 0.46, None),
             (nw, h * 0.80, (half * .96, h * 0.68)), (nw, h, None)]
    elif kind == "square":                   # прямі боки, плече майже горизонтальне
        nw, sh = min(half * 0.30, 14), h * 0.64
        n = [(half - heel * .4, 0, None), (half, heel * .4, (half, 0)), (half, sh, None),
             (half * .88, sh + h * .05, None), (nw, sh + h * 0.10, None), (nw, h, None)]
    elif kind == "flask":                    # покаті плечі фляги
        nw, sh = min(half * 0.28, 13), h * 0.54
        n = [(half - heel, 0, None), (half, heel, (half, 0)), (half, sh, None),
             (nw, sh + h * 0.26, (half * .98, sh + h * .19)), (nw, h, None)]
    elif kind == "straight":                 # вода й лимонади
        nw, sh = min(half * 0.42, 17), h * 0.66
        n = [(half - heel, 0, None), (half, heel, (half, 0)), (half, sh, None),
             (nw, sh + h * 0.13, (half * .9, sh + h * .09)), (nw, h, None)]
    elif kind == "jar":                      # харчова банка, широке горло
        nw, sh = half * 0.72, h * 0.72
        n = [(half - heel, 0, None), (half, heel, (half, 0)), (half, sh, None),
             (nw, sh + h * 0.14, (half * .95, sh + h * .10)), (nw, h, None)]
    elif kind == "waist":                    # засіб для миття посуду: талія
        nw, sh = min(half * 0.34, 15), h * 0.70
        n = [(half - heel, 0, None), (half, heel, (half, 0)), (half, h * 0.30, None),
             (half * 0.80, h * 0.52, (half * .86, h * .42)),
             (half * 0.96, sh, (half * .92, h * .62)),
             (nw, sh + h * 0.16, (half * .8, sh + h * .11)), (nw, h, None)]
    elif kind == "oval":                     # рідке мило, флакон під помпу
        nw, sh = min(half * 0.32, 14), h * 0.62
        n = [(half - heel, 0, None), (half, heel, (half, 0)), (half, h * 0.42, None),
             (half * .94, sh, (half, h * .55)),
             (nw, sh + h * 0.19, (half * .78, sh + h * .13)), (nw, h, None)]
    else:                                    # canister — побутова хімія, ручка збоку
        nw, sh = min(half * 0.34, 15), h * 0.74
        n = [(half - heel * .3, 0, None), (half, heel * .3, (half, 0)), (half, sh, None),
             (half * .82, sh + h * .06, None), (nw, sh + h * 0.11, None), (nw, h, None)]
    return n, n[-1][0]


# ---------------------------------------------------------------------------
# УКУПОРКА. Малюється ОКРЕМИМ контуром поверх горла — так само, як її й
# надівають. Кожна повертає список шляхів і нову «стелю» (докуди сягає верх).
# ---------------------------------------------------------------------------

def cap(kind, h, nw):
    p, top = [], h

    def rect(x0, y0, x1, y1):
        return ("M %s %s L %s %s L %s %s L %s %s Z"
                % (X(x0), Y(h, y0), X(x1), Y(h, y0), X(x1), Y(h, y1), X(x0), Y(h, y1)))

    if kind == "crown":                       # кронен: коронка з зубцями
        w, hh = nw * 1.34, 9
        p.append(rect(-w, h - 2, w, h + hh))
        for i in range(-4, 5):                # зубці
            p.append("M %s %s L %s %s" % (X(w * i / 4.5), Y(h, h - 2),
                                          X(w * i / 4.5), Y(h, h + hh * .55)))
        top = h + hh
    elif kind == "twist":                     # твіст-офф: ковпачок із насічкою
        w, hh = nw * 1.3, 14
        p.append(rect(-w, h - 3, w, h + hh))
        for i in range(-3, 4):
            p.append("M %s %s L %s %s" % (X(w * i / 3.4), Y(h, h - 1),
                                          X(w * i / 3.4), Y(h, h + hh)))
        top = h + hh
    elif kind == "ropp":                      # гвинтовий алюмінієвий, довгий
        w, hh = nw * 1.22, 30
        p.append(rect(-w, h - 6, w, h + hh))
        p.append("M %s %s L %s %s" % (X(-w), Y(h, h + hh * .3), X(w), Y(h, h + hh * .3)))
        top = h + hh
    elif kind == "pet":                       # ПЕТ-ковпачок, високий із ребрами
        w, hh = nw * 1.26, 20
        p.append(rect(-w, h - 3, w, h + hh))
        for i in range(-4, 5):
            p.append("M %s %s L %s %s" % (X(w * i / 4.4), Y(h, h - 3),
                                          X(w * i / 4.4), Y(h, h + hh)))
        top = h + hh
    elif kind == "pump":                      # помпа з носиком — рідке мило
        w, hh = nw * 1.2, 26
        p.append(rect(-w, h - 4, w, h + hh))                       # муфта
        p.append(rect(-nw * .5, h + hh, nw * .5, h + hh + 26))     # шток
        p.append("M %s %s L %s %s L %s %s L %s %s"                 # носик
                 % (X(-nw * .5), Y(h, h + hh + 26), X(-nw * 2.5), Y(h, h + hh + 26),
                    X(-nw * 2.5), Y(h, h + hh + 14), X(-nw * 1.3), Y(h, h + hh + 14)))
        top = h + hh + 26
    elif kind == "flip":                      # фліп-топ із носиком
        w, hh = nw * 1.24, 22
        p.append(rect(-w, h - 3, w, h + hh))
        p.append("M %s %s L %s %s" % (X(-w), Y(h, h + hh * .55), X(w), Y(h, h + hh * .55)))
        p.append(rect(-nw * .45, h + hh, nw * .45, h + hh + 9))
        top = h + hh + 9
    elif kind == "spout":                     # дозатор із витягнутим носиком
        w, hh = nw * 1.2, 16
        p.append(rect(-w, h - 3, w, h + hh))
        p.append("M %s %s L %s %s L %s %s L %s %s Z"
                 % (X(-nw * .55), Y(h, h + hh), X(nw * .55), Y(h, h + hh),
                    X(nw * .3), Y(h, h + hh + 22), X(-nw * .3), Y(h, h + hh + 22)))
        top = h + hh + 22
    elif kind == "shrink":                    # термоусадковий ковпачок по шийці
        w, hh = nw * 1.16, 12
        p.append(rect(-w, h - 46, w, h + hh))
        p.append("M %s %s L %s %s" % (X(-w), Y(h, h - 46), X(w), Y(h, h - 46)))
        top = h + hh
    elif kind == "muselet":                   # мюзле: корок-гриб і дротяна вуздечка
        w = nw * 1.5
        p.append("M %s %s Q %s %s %s %s L %s %s Q %s %s %s %s Z"
                 % (X(-w), Y(h, h + 6), X(-w), Y(h, h + 20), X(-w * .55), Y(h, h + 20),
                    X(w * .55), Y(h, h + 20), X(w), Y(h, h + 20), X(w), Y(h, h + 6)))
        p.append(rect(-w * 1.02, h - 12, w * 1.02, h + 6))          # обичайка
        p.append("M %s %s L %s %s" % (X(-w), Y(h, h - 2), X(w), Y(h, h - 2)))
        for i in (-.5, 0, .5):                                       # дріт
            p.append("M %s %s L %s %s" % (X(w * i * 1.9), Y(h, h - 12),
                                          X(w * i * 1.9), Y(h, h + 6)))
        top = h + 20
    return p, top


def label(kind, h, a):
    """Наклеєна етикетка — прямокутник просто на корпусі."""
    half = a / 2
    out = []

    def rect(x0, y0, x1, y1):
        return ("M %s %s L %s %s L %s %s L %s %s Z"
                % (X(x0), Y(h, y0), X(x1), Y(h, y0), X(x1), Y(h, y1), X(x0), Y(h, y1)))

    if kind in ("body", "both"):
        out.append(rect(-half * .88, h * 0.16, half * .88, h * 0.44))
    if kind in ("neck", "both"):
        out.append(rect(-half * .40, h * 0.72, half * .40, h * 0.80))
    return out


# ---------------------------------------------------------------------------
# НАБІР. Розміри типові для категорії, не наші заміри (див. шапку файлу).
# ---------------------------------------------------------------------------
GROUPS = [
    ("Пиво й слабоалкогольне", [
        ("Пиво 0,33", "beer", 232, 57, "crown", ""),
        ("Пиво 0,5", "beer", 265, 63, "twist", "body"),
        ("Сидр 0,5", "bordeaux", 255, 70, "crown", "both"),
    ]),
    ("Вино й ігристе", [
        ("Вино 0,75 бордо", "bordeaux", 300, 76, "shrink", "both"),
        ("Вино 0,75 бургунді", "burgundy", 295, 82, "shrink", "body"),
        ("Ігристе 0,75", "sparkling", 310, 88, "muselet", "body"),
    ]),
    ("Міцний алкоголь", [
        ("Горілка 0,5", "square", 225, 80, "ropp", "both"),
        ("Віскі 0,7", "flask", 245, 92, "ropp", "body"),
        ("Настоянка 0,7", "bordeaux", 300, 72, "shrink", "both"),
    ]),
    ("Вода, лимонади, соки", [
        ("Вода 0,5", "straight", 225, 68, "twist", "body"),
        ("Лимонад 1,0", "straight", 280, 84, "pet", "body"),
        ("Сік 1,0", "square", 270, 85, "pet", "both"),
    ]),
    ("Харчова тара", [
        ("Банка 0,5", "jar", 130, 95, "twist", "body"),
        ("Соус 0,25", "waist", 165, 58, "spout", "body"),
    ]),
    ("Побутова хімія й гігієна", [
        ("Рідке мило 0,3", "oval", 190, 70, "pump", "body"),
        ("Для миття посуду 0,5", "waist", 250, 70, "flip", "body"),
        ("Побутова хімія 1,0", "canister", 255, 96, "pet", "body"),
    ]),
]


def tile(name, kind, h, a, capkind, lab):
    n, nw = body(kind, h, a)
    paths = ['<path class="glass" d="%s"/>' % mirror(h, n)]
    cp, top = cap(capkind, h, nw)
    for d in cp:
        paths.append('<path class="cap" d="%s"/>' % d)
    for d in label(lab, h, a):
        paths.append('<path class="lab" d="%s"/>' % d)
    w = max(a, nw * 4) * K + 26
    vb_top = -(top - h) * K - 10
    return (f'<figure class="t">\n'
            f'  <svg viewBox="{-w/2:.0f} {vb_top:.0f} {w:.0f} {(h*K)-vb_top+8:.0f}" '
            f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{name}">\n'
            f'    <g fill="none" stroke="#1B1E23" stroke-width="1.4" '
            f'stroke-linejoin="round" vector-effect="non-scaling-stroke">\n      '
            + "\n      ".join(paths)
            + f'\n    </g>\n  </svg>\n  <figcaption>{name}</figcaption>\n</figure>')


def main():
    secs, total = [], 0
    for title, items in GROUPS:
        tiles = "\n".join(tile(*i) for i in items)
        total += len(items)
        secs.append(f'<h3 class="grp">{title} <b>{len(items)}</b></h3>\n'
                    f'<div class="row">\n{tiles}\n</div>')
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(TEMPLATE.replace("__BODY__", "\n".join(secs)).replace("__N__", str(total)))
    print("lab/tare.html — %d типів у %d категоріях" % (total, len(GROUPS)))


TEMPLATE = """<!doctype html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Каталог типів тари — прототип</title>
<meta name="robots" content="noindex">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/styles.css">
<style>
  .grp{font-size:15px;font-weight:600;margin:var(--s48) 0 var(--s16);
    padding-bottom:var(--s8);border-bottom:1px solid var(--border)}
  .grp b{font-family:var(--fm);font-size:11px;color:var(--amber);
    font-weight:600;margin-left:8px}
  .row{display:flex;align-items:flex-end;gap:var(--s32);flex-wrap:wrap}
  .t{margin:0;text-align:center}
  .t svg{width:auto;display:block;overflow:visible}
  .t .glass{stroke-width:1.4}
  .t .cap{stroke-width:1.2}
  .t .lab{stroke-width:1;stroke:var(--steel)}
  .t figcaption{font-family:var(--fm);font-size:10.5px;letter-spacing:.05em;
    color:var(--steel);margin-top:10px;text-transform:uppercase}
  .t:hover .glass,.t:hover .cap{stroke:var(--amber)}
</style>
</head>
<body data-page="lab">
<main>
<section class="section">
  <div class="container">
    <div class="sec-head">
      <span class="eyebrow eyebrow--muted">Прототип · типи тари</span>
      <h2>З якою тарою працює оснастка</h2>
      <p>__N__ типів: корпус, надіта укупорка й наклеєна етикетка — усе, що
         проходить крізь лінію і що має «взяти» форматна деталь.</p>
    </div>
    __BODY__
    <div style="max-width:70ch;margin-top:var(--s48);color:var(--steel);font-size:15px;line-height:24px">
      <p><b>Це вітрина типів, а не наш перелік замовлень.</b> Розміри тут типові
         для категорії. Наші заміряні формати — окремо, на сторінці лінійки:
         там кожен силует стоїть за реальними H/A/B із бази.</p>
    </div>
  </div>
</section>
</main>
</body>
</html>
"""

if __name__ == "__main__":
    main()
