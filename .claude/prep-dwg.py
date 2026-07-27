# Готує креслення-складання до вебу: обрізає білі поля, вирізає зовнішнє біле
# тло в альфу, зводить розмір і кладе у images/products/osnastka/dwg/
# під іменами dwg-01…NN.png.
#
# Чому саме альфа, а не multiply по білому:
#   1) Палітрове квантування (перша спроба) зсуває біле з 255 на 250-253, і
#      multiply лишає замість чистого тла світло-сірий прямокутник — на сторінці
#      це видно як бліді коробки навколо креслень.
#   2) Заливка від кутів по зв'язності лишає БІЛИМ те, що всередині контурів
#      деталей, — і це правильно: суцільне тіло деталі має затуляти те, що під
#      ним, а не просвічувати.
#
# Usage: py .claude/prep-dwg.py "<src dir>" [max_px]
import os, sys
from PIL import Image, ImageDraw, ImageFilter

DST = os.path.join("images", "products", "osnastka", "dwg")

def trim(im, bg=255, tol=6):
    g = im.convert("L")
    mask = g.point(lambda p: 255 if p < bg - tol else 0)
    box = mask.getbbox()
    return im.crop(box) if box else im

def alpha_from_corners(im, tol=14, feather=0.6):
    w, h = im.size
    flood = im.convert("L")
    for xy in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        ImageDraw.floodfill(flood, xy, 0, thresh=tol)
    px = flood.load()
    alpha = Image.new("L", (w, h), 255)
    ap = alpha.load()
    for y in range(h):
        for x in range(w):
            if px[x, y] == 0:
                ap[x, y] = 0
    if feather:
        alpha = alpha.filter(ImageFilter.GaussianBlur(feather))
    # LA (сірий + альфа) замість RGBA: креслення й так чорно-біле, а вага
    # падає в рази — RGBA-версія важила ~200 КБ на аркуш, це 7 МБ на набір.
    out = im.convert("L")
    out.putalpha(alpha)
    return out

def main(src, maxpx=1000):
    os.makedirs(DST, exist_ok=True)
    files = sorted(f for f in os.listdir(src) if f.lower().endswith((".png", ".jpg")))
    tot = 0
    for i, f in enumerate(files, 1):
        im = Image.open(os.path.join(src, f)).convert("RGB")
        im = trim(im)
        im.thumbnail((maxpx, maxpx), Image.LANCZOS)
        out = alpha_from_corners(im)
        p = os.path.join(DST, "dwg-%02d.png" % i)
        out.save(p, "PNG", optimize=True)
        kb = os.path.getsize(p) // 1024
        # Дрібна копія для колажу на тлі: там аркуш малюється завширшки
        # 200–350px і на 28% прозорості, повний розмір там марно висить у мережі.
        os.makedirs(os.path.join(DST, "sm"), exist_ok=True)
        sm = out.copy()
        sm.thumbnail((420, 420), Image.LANCZOS)
        ps = os.path.join(DST, "sm", "dwg-%02d.png" % i)
        sm.save(ps, "PNG", optimize=True)
        kbs = os.path.getsize(ps) // 1024
        tot += kb + kbs
        print("dwg-%02d  %dx%d  %d KB  (sm %d KB)" % (i, out.size[0], out.size[1], kb, kbs))
    print("разом %d KB у %d файлах" % (tot, len(files)))

if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1000)
