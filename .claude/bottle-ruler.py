# -*- coding: utf-8 -*-
"""Лінійка форматів тари — SVG зі СВОЇХ чисел, без чужих креслень.

Чому не з PDF-креслень пляшок (перевірено 27-07):
  · це документи чужих заводів (Glass Alliance, OMCO) — зі штампами
    затвердження, кодами ЄДРПОУ й живими підписами named-осіб;
  · назва бренду там не тільки в штампі, вона ВІДЛИТА У СКЛІ: написи по
    корпусу, тавро на дні, декоративний рельєф. Контур із фронтального
    вигляду несе її з собою, тож «обрізати штамп» проблему не вирішує.

Тому силует малюється параметрично з трьох чисел, які є нашими фактами:
  H — повна висота, A — ширина, B — глибина (bottles_cache.jsonl).
Це СХЕМА формату, а не креслення: вона чесно показує висоту й ширину
й нічого не стверджує про профіль плечей. Назв на ній немає за побудовою.

Запуск:  py .claude/bottle-ruler.py [шлях_до_bottles_cache.jsonl]
Пише:    lab/bottles.html
"""
import io, json, math, os, random, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

CACHE = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\oleks\Claude\Sophon\cache\bottles_cache.jsonl"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "lab", "bottles.html")

PX_PER_MM = 0.86      # 322 мм найвищої пляшки -> ~277 px
GAP = 26              # просвіт між силуетами
PAD_TOP, PAD_BOT = 26, 54


# ---------------------------------------------------------------------------
# ФОРМИ. Раніше тут був один архетип — циліндричний корпус під корок, і на
# лінійці всі формати виглядали однією пляшкою в різних пропорціях. Тепер
# родин шість, і вибір родини йде НЕ навмання, а з тих самих наших чисел:
#   стрункість  = H / A  (наскільки висока відносно ширини)
#   плоска      = B / A < 0.85  (флакон-фляга проти круглої)
# У наборі стрункість гуляє від 2.1 до 4.4, а плоских майже половина, тож
# різні форми — це прочитані дані, а не домальована фантазія.
# ---------------------------------------------------------------------------

# Типи вінця. Каталог склозаводу-постачальника (Vetropack) розрізняє тару не
# лише за корпусом, а й за вінцем: cork, crown, twist off, BVS, Guala, PP,
# широке горло. Саме через одне-єдине горло на всіх у мене спершу «всі пляшки
# виглядали циліндричними під корок».
# ⚠ Тип вінця в наших даних Є РІВНО В ОДНОГО запису з 63, тож вивести його з
# фактів не можна. Тут він ілюстративний і прив'язаний до родини корпусу —
# як і решта профілю, це схема, а не паспорт виробу. Висота й ширина лишаються
# справжніми, бо саме вони й важать для оснастки.
FINISH = {"squat": "wide", "flask": "twist", "burgundy": "cork",
          "bordeaux": "crown", "square": "twist", "slim": "bvs"}


def finish_nodes(kind, nw, h, fh):
    """Верхівка контуру: від верху шийки до зрізу вінця."""
    if kind == "wide":            # широке горло — банка, харчова тара
        return [(nw * 1.34, h - fh * 0.72, None), (nw * 1.34, h, None)]
    if kind == "crown":           # кроненпробка — короткий вузький валик
        return [(nw * 1.14, h - fh * 0.62, None), (nw * 1.14, h, None)]
    if kind == "twist":           # twist off — два валики, ширший зріз
        return [(nw * 1.2, h - fh * 0.8, None), (nw * 1.06, h - fh * 0.46, None),
                (nw * 1.2, h - fh * 0.34, None), (nw * 1.2, h, None)]
    if kind == "bvs":             # довга різьбова горловина під алкоголь
        return [(nw * 1.1, h - fh * 1.5, None), (nw * 1.1, h, None)]
    return [(nw * 1.2, h - fh * 0.5, None), (nw * 1.2, h, None)]   # cork


def outline(h, a, b):
    """Права половина контуру знизу вгору: список вузлів (x, y, ctrl).

    x — півширина в мм, y — висота від дна в мм, ctrl — контрольна точка
    квадратичної кривої від попереднього вузла (або None для прямої).
    Тільки прямі та Q-криві: так половину легко віддзеркалити у зворотному
    порядку й не тримати окремий опис лівого боку.
    """
    half = a / 2
    flat = (b / a) < 0.85
    slim = h / a                      # стрункість

    if slim < 2.35:
        family = "squat"              # присадкувата банка
    elif flat and slim < 2.9:
        family = "flask"              # фляга з покатими плечима
    elif slim < 2.9:
        family = "burgundy"           # плече переходить у шийку без злому
    elif flat:
        family = "square"             # прямі боки, майже горизонтальне плече
    elif slim < 3.8:
        family = "bordeaux"           # циліндр і різке плече
    else:
        family = "slim"               # висока вузька, довга шийка

    heel = min(half * 0.16, h * 0.028)

    if family == "squat":
        nw, fh = min(half * 0.55, 19), h * 0.05
        sh, nk = h * 0.70, h * 0.86
        n = [(half - heel, 0, None), (half, heel, (half, 0)),
             (half, sh, None), (nw, nk, (half, nk * .97)),
             (nw, h - fh, None)] + finish_nodes(FINISH[family], nw, h, fh)
    elif family == "flask":
        nw, fh = min(half * 0.30, 16), h * 0.05
        sh, nk = h * 0.52, h * 0.84
        n = [(half - heel, 0, None), (half, heel, (half, 0)),
             (half, sh, None),
             (nw, nk, (half * 0.99, nk * 0.93)),        # широка покала дуга
             (nw, h - fh, None)] + finish_nodes(FINISH[family], nw, h, fh)
    elif family == "burgundy":
        nw, fh = min(half * 0.34, 16), h * 0.05
        n = [(half - heel, 0, None), (half, heel, (half, 0)),
             (half, h * 0.42, None),
             (nw, h * 0.80, (half, h * 0.70)),          # суцільна дуга, без злому
             (nw, h - fh, None)] + finish_nodes(FINISH[family], nw, h, fh)
    elif family == "square":
        nw, fh = min(half * 0.32, 15), h * 0.045
        sh = h * 0.62
        n = [(half - heel * .5, 0, None), (half, heel * .5, (half, 0)),
             (half, sh, None), (half * 0.9, sh + h * .05, None),
             (nw, sh + h * 0.09, None),                 # плече майже горизонтальне
             (nw, h - fh, None)] + finish_nodes(FINISH[family], nw, h, fh)
    elif family == "bordeaux":
        nw, fh = min(half * 0.32, 15), h * 0.05
        sh = h * 0.56
        n = [(half - heel, 0, None), (half, heel, (half, 0)),
             (half, sh, None),
             (nw, sh + h * 0.16, (half * .92, sh + h * .12)),   # різке плече
             (nw, h - fh, None)] + finish_nodes(FINISH[family], nw, h, fh)
    else:  # slim
        nw, fh = min(half * 0.30, 13), h * 0.045
        sh = h * 0.44
        n = [(half - heel, 0, None), (half, heel, (half, 0)),
             (half, sh, None),
             (nw, sh + h * 0.20, (half * .85, sh + h * .15)),
             (nw, h - fh, None)] + finish_nodes(FINISH[family], nw, h, fh)
    return n, family


def path(h, a, b):
    n, _ = outline(h, a, b)

    def X(v):
        return round(v * PX_PER_MM, 2)

    def Y(v):
        return round((h - v) * PX_PER_MM, 2)

    d = ["M %s %s" % (X(-n[0][0]), Y(n[0][1])), "L %s %s" % (X(n[0][0]), Y(n[0][1]))]
    for x, y, c in n[1:]:                                   # правий бік угору
        d.append("Q %s %s %s %s" % (X(c[0]), Y(c[1]), X(x), Y(y)) if c
                 else "L %s %s" % (X(x), Y(y)))
    d.append("L %s %s" % (X(-n[-1][0]), Y(n[-1][1])))        # через вінець
    for i in range(len(n) - 1, 0, -1):                      # лівий бік униз
        x, y, c = n[i - 1][0], n[i - 1][1], n[i][2]
        d.append("Q %s %s %s %s" % (X(-c[0]), Y(c[1]), X(-x), Y(y)) if c
                 else "L %s %s" % (X(-x), Y(y)))
    d.append("Z")
    return " ".join(d)


def litres(ml):
    s = ("%g" % (ml / 1000.0)).replace(".", ",")
    return s + " л"


def widths(r):
    """Ширина й глибина формату. Де є заміри — беремо їх.

    Де є тільки висота й об'єм (таких записів удвічі більше), рахуємо
    еквівалентний діаметр: об'єм = площа × висота корпусу, корпус — приблизно
    0.58 повної висоти. Це не вигадка, а фізика; на форматах, де є обидва
    джерела, розрахунок дає 83.8 проти заміряних 81.0 і 110.3 проти 113.9.
    Для плоских флаконів розрахунок занижує (там A — широка грань, а не
    діаметр), тож такі позначаємо як похідні й на них нічого не стверджуємо.
    """
    if r.get("a") and r.get("b"):
        return r["a"], r["b"], False
    v_mm3 = r["volume_ml"] * 1000.0
    d = (4 * v_mm3 / (math.pi * 0.58 * r["h"])) ** 0.5
    return d, d, True


def band(kit):
    """Смуга «врозбіг» — під фон, а не під читання.

    Строгий стрій за висотою потрібен лінійці: там висоти порівнюють очима.
    Фону він шкодить — рівний ряд однакових інтервалів читається як частокіл.
    Тому тут навпаки: пляшки стоять не на одній базі, а гуляють по вертикалі,
    інтервали нерівні, масштаб трохи різний, а порядок перемішаний, щоб поруч
    не опинялись дві схожі. Розкид детермінований (`random.seed`), інакше кожна
    перезбірка давала б інший фон і діф було б не прочитати.
    """
    rng = random.Random(20260727)
    order = kit[:]
    rng.shuffle(order)
    # трохи більше за набір, щоб смуга була довшою за екран
    seq = order + [r for r in reversed(order[: max(1, len(order) // 2)])]

    maxh = max(r["h"] for r in seq) * PX_PER_MM
    H = round(maxh * 1.34)
    parts, x = [], 20.0
    for r in seq:
        s = rng.uniform(0.72, 1.0)                 # різний масштаб
        h = r["h"] * PX_PER_MM * s
        w = r["_a"] * PX_PER_MM * s
        # ДНО НА ОДНОМУ РІВНІ. Спершу я розкидав і по вертикалі — вийшло, що
        # пляшки висять у повітрі, і вся картинка читалась як помилка, а не як
        # розсип. Розбіг лишається в масштабі, інтервалах, формі й порядку;
        # низ у всіх спільний, як на полиці.
        y = H - h
        parts.append(
            f'  <g transform="translate({x + w / 2:.1f} {y:.1f}) scale({s:.3f})"'
            f' opacity="{rng.uniform(.5, 1):.2f}">'
            f'<path d="{path(r["h"], r["_a"], r["_b"])}"/></g>'
        )
        x += w + rng.uniform(8, 40)                # нерівні інтервали
    # Оформлення — АТРИБУТАМИ, а не класом. Смуга задумана як ассет, який
    # можна покласти і фоном, і окремим файлом; CSS сторінки туди не поїде,
    # а без `fill` контур заливається чорним за замовчуванням — саме так я
    # вперше й отримав чорний прямокутник замість силуетів.
    return (f'<svg class="btl-band" viewBox="0 0 {x + 20:.0f} {H}" '
            f'xmlns="http://www.w3.org/2000/svg" aria-hidden="true"'
            f' preserveAspectRatio="xMidYMid slice">\n'
            f'  <g fill="none" stroke="#1B1E23" stroke-width="1.6" stroke-linejoin="round">\n'
            + "\n".join(parts) + "\n  </g>\n</svg>")


def main():
    rows = [json.loads(l) for l in open(CACHE, encoding="utf-8") if l.strip()]
    kit = [r for r in rows if r.get("h") and r.get("volume_ml")]
    for r in kit:
        r["_a"], r["_b"], r["_est"] = widths(r)
    # шикуємо ЗА ВИСОТОЮ, а не за об'ємом: рядок має читатись як сходинка.
    # За об'ємом виходить пилка — 0,375 л буває вищою за 0,5 л, і замість
    # лінійки видно безлад.
    kit.sort(key=lambda r: (r["h"], r["_a"]))
    if not kit:
        sys.exit("У кеші немає жодного запису з повними H/A/B — малювати нічого.")

    maxh = max(r["h"] for r in kit)
    height = round(maxh * PX_PER_MM) + PAD_TOP + PAD_BOT
    base = PAD_TOP + round(maxh * PX_PER_MM)

    # ---- 1. Лінійка: строгий стрій за висотою, підписи об'ємом ----
    parts, cursor = [], 0
    for r in kit:
        w = round(r["_a"] * PX_PER_MM) + GAP
        cx = cursor + w / 2
        top = base - round(r["h"] * PX_PER_MM)
        parts.append(
            f'  <g class="bt" transform="translate({cx:.1f} {top:.1f})">\n'
            f'    <path d="{path(r["h"], r["_a"], r["_b"])}"/>\n'
            f'    <text class="v" y="{round(r["h"]*PX_PER_MM)+22:.0f}">{litres(r["volume_ml"])}</text>\n'
            f'  </g>'
        )
        cursor += w

    svg = (f'<svg class="ruler" viewBox="0 0 {cursor:.0f} {height}" '
           f'xmlns="http://www.w3.org/2000/svg" role="img" '
           f'aria-label="Лінійка форматів тари: силуети пляшок за висотою, підписані об\'ємом">\n'
           + "\n".join(parts)
           + f'\n  <line class="base" x1="0" y1="{base+.5}" x2="{cursor:.0f}" y2="{base+.5}"/>\n</svg>')

    html = TEMPLATE.replace("__SVG__", svg).replace("__BAND__", band(kit)) \
                   .replace("__N__", str(len(kit))) \
                   .replace("__EST__", str(sum(1 for r in kit if r["_est"]))) \
                   .replace("__TOTAL__", str(len(rows)))
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)

    print(f"lab/bottles.html — {len(kit)} форматів із {len(rows)} записів кеша")
    for r in kit:
        mark = "розрах." if r["_est"] else "заміри"
        print(f"  {litres(r['volume_ml']):>8}  H={r['h']:.0f}  A={r['_a']:.0f}  B={r['_b']:.0f}"
              f"  {mark}  {r.get('kod') or '(без коду)'}")


TEMPLATE = """<!doctype html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Лінійка форматів тари — прототип</title>
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/styles.css">
<style>
  .ruler{width:100%;height:auto;display:block}
  .ruler .bt path{fill:none;stroke:var(--graphite);stroke-width:1.1;
    vector-effect:non-scaling-stroke;stroke-linejoin:round}
  .ruler .bt .v{font-family:var(--fm);font-size:11px;fill:var(--steel);
    text-anchor:middle;letter-spacing:.06em}
  .ruler .bt:hover path{stroke:var(--amber)}
  .ruler .bt:hover .v{fill:var(--amber)}
  .ruler .base{stroke:var(--border);stroke-width:1;vector-effect:non-scaling-stroke}
  .btl-band{width:100%;height:auto;display:block}
  .btl-band path{fill:none;stroke:var(--graphite);stroke-width:1;vector-effect:non-scaling-stroke}
  .bandwrap{width:100vw;margin-left:calc(50% - 50vw);overflow:hidden;margin-bottom:var(--s48)}
  /* демонстрація «під текстом»: та сама смуга, пригашена й розмита */
  .demo{position:relative;overflow:hidden;padding:var(--s64) var(--s32);
    border:1px solid var(--border)}
  .demo-bg{position:absolute;inset:0;opacity:.3;filter:blur(.4px)}
  .demo-bg .btl-band{height:100%}
  .demo-fg{position:relative;max-width:52ch;
    background:radial-gradient(80% 90% at 40% 50%,rgba(255,255,255,.94) 45%,rgba(255,255,255,0));
    padding:var(--s24)}
  .demo-fg h3{font-size:26px;margin:var(--s8) 0}
  .demo-fg p{color:var(--steel);font-size:15px;line-height:24px}
  .why{max-width:70ch;margin-top:var(--s48)}
  .why h3{font-size:17px;margin-bottom:var(--s8)}
  .why p{color:var(--steel);font-size:15px;line-height:24px;margin-bottom:var(--s16)}
</style>
</head>
<body data-page="lab">
<main>
<section class="section">
  <div class="container">
    <div class="sec-head">
      <span class="eyebrow eyebrow--muted">Прототип · етап C-a</span>
      <h2>Лінійка форматів тари</h2>
      <p>Силуети стоять на одній базі й змасштабовані однаково, тож висоти
         порівнюються напряму. Підпис — тільки об'єм.</p>
    </div>
    __SVG__
  </div>
</section>

<!-- Смуга «врозбіг» — кандидат у фон секції, а не в самостійний блок.
     Показана двічі: як є, і в тій силі, у якій вона реально лягла б під текст. -->
<section class="section section--mist">
  <div class="container">
    <div class="sec-head">
      <span class="eyebrow eyebrow--muted">Той самий набір · врозбіг</span>
      <h2>Смуга під фон</h2>
      <p>Не стрій, а розсип: різна висота посадки, різний масштаб, нерівні
         інтервали. Так вона працює текстурою, а не переліком.</p>
    </div>
  </div>
  <div class="bandwrap">__BAND__</div>
  <div class="container">
    <div class="demo">
      <div class="demo-bg">__BAND__</div>
      <div class="demo-fg">
        <span class="eyebrow eyebrow--muted">Як це виглядає під текстом</span>
        <h3>Комплект форматних деталей під вашу пляшку</h3>
        <p>Смуга тут пригашена до тієї сили, у якій вона не сперечається
           з текстом. Це той самий ассет, що вище.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="why">
      <h3>Звідки це намальовано</h3>
      <p>Не з креслень пляшок. Ті креслення — документи чужих заводів, зі
         штампами затвердження й підписами; до того ж назва бренду там відлита
         просто у склі: написи по корпусу, тавро на дні. Контур із такого
         аркуша ніс би назву з собою, тож «обрізати штамп» нічого не давало б.</p>
      <p>Тут силует побудований із трьох наших чисел — повна висота, ширина,
         глибина. Це схема формату: висота й ширина справжні, профіль плечей
         узагальнений. Плоскі формати й круглі малюються по-різному, бо саме
         через цю різницю оснастка під однаковий об'єм буває не та сама.</p>
      <p><b>Показано __N__ форматів із __TOTAL__ записів бази</b>
         (з них __EST__ — з розрахованою шириною: у базі є висота й об'єм,
         але немає замірів A/B). Решта записів поки без висоти — не тому, що таких форматів немає, а тому, що
         H/A/B у них не заповнені. Скільки форматів заявляємо цифрою — окреме
         питання до власника, без підтвердження цифру на сайт не ставимо.</p>
    </div>
  </div>
</section>
</main>
</body>
</html>
"""

if __name__ == "__main__":
    main()
