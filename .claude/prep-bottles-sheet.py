# -*- coding: utf-8 -*-
"""Контактний аркуш пляшок -> ассет під розмитий фон.

Джерело — `Downloads/site docs/Screenshot_2025-11-10_000430.png`: знімок усієї
бібліотеки тари, ~72 формати в комірках, на кожному наша рукописна маркування
з кодом і розмірами. Це наші власні фото порожнього скла на світлому тлі —
на відміну від креслень, їх використовувати можна (рішення власника 27-07).

Що робимо і навіщо:
  · у чорно-біле. На аркуші п'ять пляшок зеленого скла, і в кольорі вони
    вистрибують плямою — під фоном це читається як брак, а не як фактура;
  · трохи піднімаємо контраст, бо після розмиття світле скло на світлому тлі
    зникає зовсім;
  · у JPEG. Вихідний PNG — 931 КБ, а це фон, який поїде на кожного відвідувача.

Запуск: py .claude/prep-bottles-sheet.py
"""
import io, os, sys
from PIL import Image, ImageOps, ImageEnhance

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SRC = r"C:\Users\oleks\Downloads\site docs\Screenshot_2025-11-10_000430.png"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "images", "products", "osnastka")


def main():
    if not os.path.exists(SRC):
        sys.exit("Немає вихідного аркуша: " + SRC)
    im = Image.open(SRC).convert("L")
    im = ImageOps.autocontrast(im, cutoff=1)
    im = ImageEnhance.Contrast(im).enhance(1.18)
    os.makedirs(OUT, exist_ok=True)

    for name, width, q in (("bottles-sheet.jpg", im.width, 82),
                           ("bottles-sheet-sm.jpg", 900, 78)):
        v = im if width == im.width else im.resize(
            (width, round(im.height * width / im.width)), Image.LANCZOS)
        p = os.path.join(OUT, name)
        v.save(p, "JPEG", quality=q, optimize=True, progressive=True)
        print("%-22s %dx%d  %d КБ" % (name, v.width, v.height, os.path.getsize(p) // 1024))

    print("джерело: %dx%d  %d КБ" % (im.width, im.height, os.path.getsize(SRC) // 1024))


if __name__ == "__main__":
    main()
