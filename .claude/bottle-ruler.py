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
import io, json, os, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

CACHE = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\oleks\Claude\Sophon\cache\bottles_cache.jsonl"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "lab", "bottles.html")

PX_PER_MM = 0.86      # 322 мм найвищої пляшки -> ~277 px
GAP = 26              # просвіт між силуетами
PAD_TOP, PAD_BOT = 26, 54


def profile(h, a, b):
    """Півконтур пляшки: список (y_від_дна, півширина) знизу вгору.

    Дві родини. Кругла (B≈A) має вужчі плечі й довшу шийку; плоска
    (B значно менше за A) — широкі похилі плечі, як у фляги. Різницю
    видно на лінійці, і вона справжня: саме через неї оснастка під
    однаковий об'єм буває різна.
    """
    flat = (b / a) < 0.85
    nw = min(a * 0.34, 32) / 2          # півширина шийки
    fw = nw * 1.22                      # півширина вінця
    hb = h * (0.50 if flat else 0.55)   # де закінчується корпус
    hs = h * (0.76 if flat else 0.72)   # де починається шийка
    fh = h * 0.055                      # висота вінця
    return dict(flat=flat, nw=nw, fw=fw, hb=hb, hs=hs, fh=fh, half=a / 2)


def path(h, a, b):
    p = profile(h, a, b)
    half, nw, fw, hb, hs, fh = p["half"], p["nw"], p["fw"], p["hb"], p["hs"], p["fh"]
    heel = min(half * 0.18, h * 0.03)   # завал п'ятки
    top = h - fh

    def y(v):  # мм від дна -> координата SVG (вісь вниз)
        return round((h - v) * PX_PER_MM, 2)

    def x(v):
        return round(v * PX_PER_MM, 2)

    # права половина знизу вгору, потім дзеркало
    d = []
    d.append(f"M {x(-half + heel)} {y(0)}")
    d.append(f"L {x(half - heel)} {y(0)}")
    d.append(f"Q {x(half)} {y(0)} {x(half)} {y(heel)}")       # п'ятка
    d.append(f"L {x(half)} {y(hb)}")                          # корпус
    # плечі: у плоскої — крутіша дуга, у круглої — м'якша
    cy = hb + (hs - hb) * (0.62 if p["flat"] else 0.5)
    d.append(f"C {x(half)} {y(cy)} {x(nw)} {y(cy)} {x(nw)} {y(hs)}")
    d.append(f"L {x(nw)} {y(top - h * 0.012)}")               # шийка
    d.append(f"L {x(fw)} {y(top)}")                           # вінець
    d.append(f"L {x(fw)} {y(h)}")
    d.append(f"L {x(-fw)} {y(h)}")
    d.append(f"L {x(-fw)} {y(top)}")
    d.append(f"L {x(-nw)} {y(top - h * 0.012)}")
    d.append(f"L {x(-nw)} {y(hs)}")
    d.append(f"C {x(-nw)} {y(cy)} {x(-half)} {y(cy)} {x(-half)} {y(hb)}")
    d.append(f"L {x(-half)} {y(heel)}")
    d.append(f"Q {x(-half)} {y(0)} {x(-half + heel)} {y(0)}")
    d.append("Z")
    return " ".join(d)


def litres(ml):
    s = ("%g" % (ml / 1000.0)).replace(".", ",")
    return s + " л"


def main():
    rows = [json.loads(l) for l in open(CACHE, encoding="utf-8") if l.strip()]
    kit = [r for r in rows if r.get("h") and r.get("a") and r.get("b") and r.get("volume_ml")]
    # шикуємо ЗА ВИСОТОЮ, а не за об'ємом: рядок має читатись як сходинка.
    # За об'ємом виходить пилка — 0,375 л буває вищою за 0,5 л, і замість
    # лінійки видно безлад.
    kit.sort(key=lambda r: (r["h"], r["a"]))
    if not kit:
        sys.exit("У кеші немає жодного запису з повними H/A/B — малювати нічого.")

    maxh = max(r["h"] for r in kit)
    height = round(maxh * PX_PER_MM) + PAD_TOP + PAD_BOT
    base = PAD_TOP + round(maxh * PX_PER_MM)

    parts, cursor = [], 0
    for r in kit:
        w = round(r["a"] * PX_PER_MM) + GAP
        cx = cursor + w / 2
        top = base - round(r["h"] * PX_PER_MM)
        parts.append(
            f'  <g class="bt" transform="translate({cx:.1f} {top:.1f})">\n'
            f'    <path d="{path(r["h"], r["a"], r["b"])}"/>\n'
            f'    <text class="v" y="{round(r["h"]*PX_PER_MM)+22:.0f}">{litres(r["volume_ml"])}</text>\n'
            f'  </g>'
        )
        cursor += w
    svg_w = cursor

    svg = (f'<svg class="ruler" viewBox="0 0 {svg_w:.0f} {height}" '
           f'xmlns="http://www.w3.org/2000/svg" role="img" '
           f'aria-label="Лінійка форматів тари: силуети пляшок за висотою, підписані об\'ємом">\n'
           + "\n".join(parts)
           + f'\n  <line class="base" x1="0" y1="{base+.5}" x2="{svg_w:.0f}" y2="{base+.5}"/>\n</svg>')

    html = TEMPLATE.replace("__SVG__", svg).replace("__N__", str(len(kit))) \
                   .replace("__TOTAL__", str(len(rows)))
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)

    print(f"lab/bottles.html — {len(kit)} форматів із {len(rows)} записів кеша")
    for r in kit:
        print(f"  {litres(r['volume_ml']):>8}  H={r['h']:.0f}  A={r['a']:.0f}  B={r['b']:.0f}  {r['kod']}")


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
      <p><b>Показано __N__ форматів із __TOTAL__ записів бази.</b> Решта записів
         поки без розмірів — не тому, що таких форматів немає, а тому, що
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
