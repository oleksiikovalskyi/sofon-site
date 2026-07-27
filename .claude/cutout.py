# Вирізає біле тло продуктового рендера в справжню прозорість (PNG з альфою).
#
# Навіщо: рендери приходять як JPG на білому. Поки сторінка була біла, це не
# заважало. Щойно під деталь лягла штриховка — білий прямокутник почав її
# затирати, і деталь читалась як наліпка. mix-blend-mode:multiply не рятує:
# деталь світла (крем ~235), і лінії проступають крізь її тіло.
#
# Як працює: заливка від кутів по зв'язності (а не за порогом яскравості) —
# інакше світлі відблиски самої деталі теж стали б напівпрозорими. Усе, що
# заливка дістала, стає прозорим; решта лишається як є. Край трохи розмивається,
# щоб не було сходинок.
#
# Usage: py .claude/cutout.py <in.jpg> <out.png> [tolerance]
import sys
from PIL import Image, ImageDraw, ImageFilter

def cutout(src, dst, tol=12, feather=0.8):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    gray = im.convert("L")

    # маска-заготовка: заливаємо від усіх чотирьох кутів
    flood = gray.copy()
    for xy in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        ImageDraw.floodfill(flood, xy, 0, thresh=tol)

    # там, де заливка спрацювала, пікселі стали 0 — це й є тло
    px = flood.load()
    alpha = Image.new("L", (w, h), 255)
    ap = alpha.load()
    for y in range(h):
        for x in range(w):
            if px[x, y] == 0:
                ap[x, y] = 0

    if feather:
        alpha = alpha.filter(ImageFilter.GaussianBlur(feather))

    out = im.convert("RGBA")
    out.putalpha(alpha)
    out.save(dst, "PNG", optimize=True)

    opaque = sum(1 for y in range(0, h, 4) for x in range(0, w, 4) if ap[x, y] > 128)
    total = len(range(0, h, 4)) * len(range(0, w, 4))
    print("%s -> %s  %dx%d  непрозоро %.1f%%" % (src, dst, w, h, 100.0 * opaque / total))

if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit("usage: cutout.py <in> <out> [tolerance]")
    cutout(a[0], a[1], int(a[2]) if len(a) > 2 else 12)
