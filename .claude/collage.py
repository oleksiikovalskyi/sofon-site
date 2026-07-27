# Збирає з креслень-складань ОДНЕ щільне полотно для використання тлом.
#
# Вимоги власника (26-07):
#   • білого тла немає — на виході PNG з альфою;
#   • аркуші стоять максимально щільно, але НЕ налазять один на одного.
#
# Чому не проста сітка: у складань дуже нерівний силует — виноски й балони
# стирчать далеко за габарит деталі. Укладка по прямокутниках лишає між ними
# величезні дірки, і виходить рідкий розсип (саме на цьому завалилась перша
# спроба секції «Конструкція»). Тому пакування йде ПО МАСЦІ: кожен аркуш
# приміряється по справжній непрозорій площі, як розкрій на аркуші металу.
#
# Алгоритм: аркуші сортуються від більшого, кожен ставиться в найвищу-найлівішу
# позицію, де його маска не перетинається з уже покладеними. Перевірка йде на
# зменшеній у GRID разів сітці — інакше приміряння коштує години.
#
# Usage: py .claude/collage.py [out.png] [width] [height] [gap_px]
import os, sys
import numpy as np
from PIL import Image

SRC = os.path.join("images", "products", "osnastka", "dwg")
GRID = 8          # у скільки разів дрібніша сітка зіткнень
ALPHA_HIT = 24    # від якої альфи піксель вважається зайнятим


def load_sheets():
    out = []
    for f in sorted(os.listdir(SRC)):
        if not f.endswith(".png"):
            continue
        im = Image.open(os.path.join(SRC, f)).convert("LA")
        out.append((f, im))
    return out


def mask_of(im, gap):
    """Бінарна маска на дрібній сітці, роздута на gap — так між аркушами
    лишається гарантований просвіт, і вони не торкаються."""
    a = np.array(im.split()[-1])
    small = (a[::GRID, ::GRID] > ALPHA_HIT)
    if gap > 0:
        r = max(1, gap // GRID)
        m = small.copy()
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                m |= np.roll(np.roll(small, dy, 0), dx, 1)
        small = m
    return small


def place(canvas_occ, m):
    """Найвища-найлівіша позиція, де маска m не перетинає зайняте."""
    CH, CW = canvas_occ.shape
    mh, mw = m.shape
    if mh > CH or mw > CW:
        return None
    for y in range(0, CH - mh + 1):
        row = canvas_occ[y:y + mh]
        for x in range(0, CW - mw + 1):
            if not (row[:, x:x + mw] & m).any():
                return (x, y)
    return None


def main(out="images/products/osnastka/collage.png", W=2000, H=900, gap=10,
         rows=3.2, seed=7):
    """rows — скільки аркушів має вкладатись у висоту полотна. Цим і задається
    щільність: більше рядів — дрібніші аркуші й густіше поле."""
    sheets = load_sheets()
    if not sheets:
        sys.exit("немає підготовлених креслень — спершу .claude/prep-dwg.py")

    # Масштаб рахуємо від бажаної кількості рядів, а не від сумарної площі:
    # силует у складань рваний, і площа не передбачає, скільки реально влізе.
    avg_h = sum(im.height for _, im in sheets) / len(sheets)
    k = (H / rows) / avg_h
    scaled = []
    for f, im in sheets:
        w = max(40, int(im.width * k))
        h = max(40, int(im.height * k))
        scaled.append((f, im.resize((w, h), Image.LANCZOS), mask_of(im.resize((w, h)), gap)))
    print("аркушів %d, масштаб %.3f (висота ~%d px)" % (len(sheets), k, H / rows))

    occ = np.zeros((H // GRID, W // GRID), dtype=bool)
    canvas = Image.new("LA", (W, H), (255, 0))

    # Кілька проходів. Перший кладе всі 36 аркушів у натуральну величину,
    # далі кожен наступний прохід дрібнішає — дрібні аркуші затикають дірки,
    # які лишились між великими.
    #
    # Два правила проти «близнюків»: у першому проході кожен аркуш іде рівно
    # один раз, а в повторних той самий аркуш не можна ставити ближче ніж
    # MIN_DIST до вже покладеного свого ж примірника. Без цього поруч опинялись
    # дві однакові турнікетні групи — і це читалось як помилка, а не як фактура.
    MIN_DIST = int(min(W, H) * 0.55)
    rng = np.random.default_rng(seed)
    placed = 0
    used = []                                  # (індекс, x, y) у пікселях
    order = list(range(len(scaled)))
    order.sort(key=lambda i: -(scaled[i][1].width * scaled[i][1].height))

    for p_no in range(8):
        f_scale = 0.78 ** p_no
        if f_scale < 0.4:
            break
        put_this_pass = 0
        if p_no:
            rng.shuffle(order)
        for i in order:
            f, im0, m0 = scaled[i]
            if p_no:
                im = im0.resize((max(30, int(im0.width * f_scale)),
                                 max(30, int(im0.height * f_scale))), Image.LANCZOS)
                m = mask_of(im, gap)
            else:
                im, m = im0, m0
            pos = place(occ, m)
            if pos is None:
                continue
            gx, gy = pos
            px, py = gx * GRID, gy * GRID
            if any(j == i and abs(px - ux) < MIN_DIST and abs(py - uy) < MIN_DIST
                   for j, ux, uy in used):
                continue
            occ[gy:gy + m.shape[0], gx:gx + m.shape[1]] |= m
            canvas.paste(im, (px, py), im)
            used.append((i, px, py))
            placed += 1
            put_this_pass += 1
        if put_this_pass == 0:
            break

    canvas.save(out, "PNG", optimize=True)
    a = np.array(canvas.split()[-1])
    fill = (a > ALPHA_HIT).mean() * 100
    print("покладено аркушів: %d" % placed)
    print("%s  %dx%d  заповнення %.1f%%  %d КБ"
          % (out, W, H, fill, os.path.getsize(out) // 1024))


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0] if a else "images/products/osnastka/collage.png",
         int(a[1]) if len(a) > 1 else 2000,
         int(a[2]) if len(a) > 2 else 900,
         int(a[3]) if len(a) > 3 else 10,
         float(a[4]) if len(a) > 4 else 3.2)
