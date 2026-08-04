# -*- coding: utf-8 -*-
"""
Финализация банка текстов (septimatech):
  1) проверка на запрещённые упоминания (бренды, OEM, персональные данные,
     география, корпоративные цифры, имперские единицы)
  2) простановка точного счётчика знаков в конце каждого варианта V1) V2) ...
  3) сборка всех файлов в COPY-BANK.md

Прогон идемпотентен. Запуск: py -3 _finalize.py
"""
import re
from pathlib import Path

DIR = Path(__file__).resolve().parent

FORBIDDEN = [
    # плейсхолдеры и следы источника
    (r"\[(?!\d+ chars\])[A-Za-z][^\]]*\]", "плейсхолдер/ссылка"),
    (r"https?://", "URL"),
    (r"^\s*Source:", "ссылка на источник"),
    (r"[®™]", "знак торговой марки"),
    # имя компании-источника и её продуктовые марки
    (r"septimatech|unison|productivity made easy", "имя компании/марка"),
    # производители машин из галерей источника
    (r"\bkrones\b|\bronchi\b|\bserac\b|\bsidel\b|\bacma\b|\bgroninger\b|\bzalkin\b"
     r"|\barol\b|\balcoa\b|\bus bottlers\b|\bpneumatic scale\b|\bhi.?cone\b"
     r"|\bperrier\b|\bmagnetic technologies\b|\btexion\b|\bbaldwin\b", "OEM/бренд"),
    # персональные данные
    (r"[\w.+-]+@[\w-]+\.[\w.]+", "email"),
    # география и регуляторы конкретных стран
    (r"\bfda\b|\busmca\b|\bwaterloo\b|\bontario\b|\bcanada\b|\bcanadian\b"
     r"|\bunited states\b|\bu\.?s\.?a\b|\bnorth america\b|\bcross.?border\b", "география/регулятор"),
    # корпоративные цифры
    (r"\b2,?700\b|\b50,?000 different\b|\b42 countries\b|\bsince 1993\b"
     r"|\bmore than 30 years\b|\bover 30 years\b|\bseven founding\b", "корпоративная цифра"),
    # имперские единицы
    (r"\b\d[\d,.]*\s*(feet|foot|inches|inch|gallons?|lbs?[- ]in|pounds?|ounces?|oz)\b", "имперская единица"),
    (r"\d\s*['\"](?!\w)", "фут/дюйм-символ"),
    # коммерческие условия
    (r"\d+\s*%\s*(discount|off)", "коммерческое условие"),
]

MARK = re.compile(r"\s*\[\d+ chars\]$")
START = re.compile(r"^V\d+\)\s*")
ORDER = ["00-BRIEF-AND-RULES.md", "01-change-parts.md", "02-feed-screws.md",
         "03-feed-screw-drive-units.md", "04-cap-handling.md",
         "05-magnetic-capping-headsets.md", "06-bottle-inverter.md",
         "07-adjustable-guide-rails.md", "08-tight-radius-corners.md",
         "09-multi-lane-adjustment.md", "10-cap-chute.md",
         "11-automated-guide-rail-adjustment.md", "12-storage-solutions.md",
         "13-industries.md"]


def check(paths):
    hits = []
    for p in paths:
        brief = p.name.startswith("00-")
        for i, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
            for pattern, label in FORBIDDEN:
                # в брифе правила описаны словами — пропускаем строки-правила
                if brief and line.lstrip().startswith(("-", "|", "**")):
                    continue
                m = re.search(pattern, line, re.I)
                if m:
                    hits.append((p.name, i, label, m.group(0), line.strip()[:90]))
    return hits


def annotate(path: Path) -> int:
    lines = [MARK.sub("", l) for l in path.read_text(encoding="utf-8").split("\n")]
    out, buf, n = [], [], 0

    def flush():
        nonlocal buf, n
        if not buf:
            return
        tail = []
        while buf and not buf[-1].strip():
            tail.append(buf.pop())
        if buf:
            text = START.sub("", "\n".join(buf), count=1).strip()
            buf[-1] = buf[-1].rstrip() + f"  [{len(text)} chars]"
            n += 1
        out.extend(buf)
        out.extend(reversed(tail))
        buf = []

    for line in lines:
        if START.match(line):
            flush()
            buf = [line]
        elif buf:
            if line.startswith("#") or line.startswith("---") or line.startswith("- "):
                flush()
                out.append(line)
            else:
                buf.append(line)
        else:
            out.append(line)
    flush()
    path.write_text("\n".join(out), encoding="utf-8")
    return n


def assemble(paths):
    parts = [p.read_text(encoding="utf-8").strip() for p in paths]
    dest = DIR / "COPY-BANK.md"
    dest.write_text("\n\n\n---\n\n\n".join(parts) + "\n", encoding="utf-8")
    return dest, sum(len(x) for x in parts)


def main():
    paths = [DIR / n for n in ORDER if (DIR / n).exists()]
    missing = [n for n in ORDER if not (DIR / n).exists()]
    if missing:
        print("ОТСУТСТВУЮТ ФАЙЛЫ:", ", ".join(missing))

    hits = check(paths)
    if hits:
        print(f"НАЙДЕНЫ СЛЕДЫ ИСТОЧНИКА: {len(hits)}")
        for name, i, label, bad, line in hits:
            print(f"  {name}:{i}  [{label}] <{bad}>  {line}")
    else:
        print("Проверка пройдена: брендов, OEM, персданных, географии,")
        print("корпоративных цифр и имперских единиц нет")

    total = 0
    for p in paths:
        if p.name.startswith("00-"):
            continue
        total += annotate(p)
    print(f"Счётчики знаков проставлены: вариантов {total}")

    dest, size = assemble(paths)
    print(f"Собрано: {dest.name}, {size} символов, файлов {len(paths)}")


if __name__ == "__main__":
    main()
