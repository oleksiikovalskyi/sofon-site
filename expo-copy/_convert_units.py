# -*- coding: utf-8 -*-
"""
Перевод банка текстов в метрику и в «контейнеров в час».

1) CPM (containers per minute) -> containers per hour, число x 60.
   В строке первое вхождение раскрывается полностью («48,000 containers per hour»),
   последующие сокращённо («36,000 per hour») — иначе фраза не читается.
2) Имперские единицы -> метрические. Габариты тары считаются по номиналу:
   жидкие унции -> мл/л, унции веса (дезодорант) -> граммы, кварта US -> 0.95 л,
   галлон US -> 3.8 л, пинта -> 0.5 л, 1/64 дюйма -> 0.4 мм.

Запуск: py -3 _convert_units.py [--dry]
"""
import re
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
SKIP = {"00-BRIEF-AND-RULES.md", "EXPO-COPY-BANK.md"}

# --- 1. Точечные замены, которые общее правило не разберёт -------------------
LITERALS = [
    # заголовки и подзаголовки со словами вместо аббревиатуры
    ("Over 2,000 Containers a Minute", "Over 120,000 Containers an Hour"),
    ("speeds above 2,000 containers per minute", "speeds above 120,000 containers per hour"),
    ("running over 2,000 containers a minute", "running over 120,000 containers an hour"),
    # диапазон и перечисление — общее правило берёт только последнее число
    ("660–700 CPM", "39,600–42,000 containers per hour"),
    ("at 500, 700 and 900 CPM per lane",
     "at 30,000, 42,000 and 54,000 containers per hour per lane"),
    # микрокопия: на плашке нужна короткая форма
    ("- 700 CPM, two lanes", "- 42,000/hour, two lanes"),
    ("- 2,000+ per minute", "- 120,000+ per hour"),
    ("- 330 CPM", "- 19,800/hour"),
    ("- 900 CPM per lane", "- 54,000/hour per lane"),
    ("- 800 CPM", "- 48,000/hour"),
    ("- 1,200 CPM", "- 72,000/hour"),
    ("- 480 CPM combined", "- 28,800/hour combined"),
    ("- Up to 300 CPM · synchro bar", "- Up to 18,000/hour · synchro bar"),
    ("- 300 CPM+ · servo", "- 18,000/hour+ · servo"),

    # --- габариты тары ---
    ("covering 8 oz, 14 oz and 32 oz containers",
     "covering 240 ml, 415 ml and 950 ml containers"),
    ("8 oz, 14 oz and 32 oz containers", "240 ml, 415 ml and 950 ml containers"),
    ("6.8 oz through 12 oz brick and oblong", "200 ml through 355 ml brick and oblong"),
    ("in 64 oz and 170", "in 1.9 L and 170"),
    ("in 96 oz", "in 2.8 L"),
    ("30 oz sealant tubes", "890 ml sealant tubes"),
    ("1.7 oz and 2.6 oz", "48 g and 74 g"),
    ("in 20 oz and 25 oz", "in 590 ml and 740 ml"),
    ("16 oz tubs", "470 ml tubs"),
    ("48 oz milk bottle", "1.4 L milk bottle"),
    ("up to 48 oz", "up to 1.4 L"),
    ("105 oz laundry detergent", "3.1 L laundry detergent"),
    ("across 9.5 oz and 17 oz", "across 280 ml and 500 ml"),
    ("across 4 oz, 8 oz, 16 oz and 32 oz", "across 120 ml, 240 ml, 470 ml and 950 ml"),

    # --- кварты, галлоны, пинты, дюймы ---
    ("F-style quarts and gallons", "F-style 0.95 L and 3.8 L containers"),
    ("F-style quarts to gallons", "F-style 0.95 L to 3.8 L"),
    ("F-style quarts, gallons and aerosol cans",
     "F-style 0.95 L and 3.8 L containers and aerosol cans"),
    ("F-style quarts and gallon containers", "F-style 0.95 L and 3.8 L containers"),
    ("One-quart oil bottles", "0.95 L oil bottles"),
    ("Quart oil bottles", "0.95 L oil bottles"),
    ("quart oil metered", "0.95 L oil metered"),
    ("Gallon oil containers", "3.8 L oil containers"),
    ("gallon containers turned", "3.8 L containers turned"),
    ("Heavy quart and gallon containers", "Heavy 0.95 L and 3.8 L containers"),
    ("ice cream in pints, quarts and gallons", "ice cream in 0.5 L, 1 L and 3.8 L formats"),
    ("ice cream in pints through gallons", "ice cream from 0.5 L to 3.8 L"),
    ("ice cream pints metered", "470 ml ice cream tubs metered"),
    ("Gable-top half-gallon cartons", "Gable-top 1.9 L cartons"),
    ("Cups, Tubs, Cartons, Pints", "Cups, Tubs and Gable-Tops"),
    ("From Quarts to Aerosols", "From Oil Bottles to Aerosols"),
    ("to 1/64\" rotation", "to 0.4 mm of rotation"),
]

# --- 2. Общее правило по CPM -------------------------------------------------
CPM = re.compile(
    r"(\d{1,3}(?:,\d{3})*)\s*(?:CPM|[Cc]ontainers per [Mm]inute|containers a minute)"
)


def to_hour(line: str) -> str:
    seen = {"n": 0}

    def repl(m):
        value = int(m.group(1).replace(",", "")) * 60
        seen["n"] += 1
        unit = "containers per hour" if seen["n"] == 1 else "per hour"
        return f"{value:,} {unit}"

    return CPM.sub(repl, line)


LEFTOVER = re.compile(
    r"\bCPM\b|\bcontainers per minute\b|\d\s*oz\b|\bquarts?\b(?!er)|\bgallons?\b|"
    r"\bpints?\b|\binch(es)?\b|\d\s*ft\b|\bfeet\b|\blbs?\b|\bpsi\b",
    re.I,
)


def main(dry=False):
    changed_total = 0
    leftovers = []
    for path in sorted(DIR.glob("*.md")):
        if path.name in SKIP:
            continue
        text = original = path.read_text(encoding="utf-8")
        for old, new in LITERALS:
            text = text.replace(old, new)
        text = "\n".join(to_hour(l) for l in text.split("\n"))
        if text != original:
            changed_total += 1
            if not dry:
                path.write_text(text, encoding="utf-8")
        for i, line in enumerate(text.split("\n"), 1):
            for m in LEFTOVER.finditer(line):
                frag = line[max(0, m.start() - 40):m.end() + 40].strip()
                leftovers.append((path.name, i, m.group(0), frag))

    print(f"файлов изменено: {changed_total}" + (" (пробный прогон)" if dry else ""))
    if leftovers:
        print(f"ОСТАЛИСЬ ИМПЕРСКИЕ/МИНУТНЫЕ ЕДИНИЦЫ: {len(leftovers)}")
        for name, i, unit, frag in leftovers:
            print(f"  {name}:{i}  <{unit}>  …{frag}…")
    else:
        print("Имперских единиц и CPM не осталось")


if __name__ == "__main__":
    main(dry="--dry" in sys.argv)
