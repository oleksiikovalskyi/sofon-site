# -*- coding: utf-8 -*-
"""
Финализация банка текстов:
  1) проверка на запрещённые упоминания (имена клиентов, бренды, коммерческие условия)
  2) простановка точного счётчика знаков в конце каждого варианта V1) V2) ...
  3) сборка всех файлов в EXPO-COPY-BANK.md

Прогон идемпотентен. Запуск: py -3 _finalize.py
"""
import re
from pathlib import Path

DIR = Path(__file__).resolve().parent

# Банк обезличен: ни имён компаний, ни торговых марок, ни географии, ни ссылок
# на исходные документы. Проверка ищет следы, а не конкретные названия.
FORBIDDEN = [
    r"\[(?!\d+ chars\])[A-Za-z][^\]]*\]",   # плейсхолдеры в квадратных скобках
    r"^\s*Source:",                          # ссылка на исходный документ
    r"[®™]",                                 # знаки торговой марки
    r"\d+\s*%\s*(discount|off)",             # коммерческие условия
]

MARK = re.compile(r"\s*\[\d+ chars\]$")
START = re.compile(r"^V\d+\)\s*")
ORDER = ["00-BRIEF-AND-RULES.md", "01-change-parts.md", "02-timing-screws.md",
         "03-down-bottle-rejects.md", "04-screw-drive-units.md",
         "05-custom-engineered-to-order.md", "06-engineering-and-integration.md",
         "07-contract-manufacturing.md", "08-aftermarket-service.md",
         "09-oem-partnership.md", "10-industries.md"]


def check(paths):
    hits = []
    for p in paths:
        for i, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
            for pattern in FORBIDDEN:
                m = re.search(pattern, line, re.I)
                if m:
                    hits.append((p.name, i, m.group(0), line.strip()[:90]))
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
    parts = []
    for p in paths:
        text = p.read_text(encoding="utf-8").strip()
        parts.append(text)
    dest = DIR / "EXPO-COPY-BANK.md"
    dest.write_text("\n\n\n---\n\n\n".join(parts) + "\n", encoding="utf-8")
    return dest, sum(len(x) for x in parts)


def main():
    paths = [DIR / n for n in ORDER if (DIR / n).exists()]
    missing = [n for n in ORDER if not (DIR / n).exists()]
    if missing:
        print("ОТСУТСТВУЮТ ФАЙЛЫ:", ", ".join(missing))

    hits = check(paths)
    if hits:
        print(f"НАЙДЕНЫ СЛЕДЫ ИСТОЧНИКА ИЛИ БРЕНДОВ: {len(hits)}")
        for name, i, bad, line in hits:
            print(f"  {name}:{i}  <{bad}>  {line}")
    else:
        print("Проверка пройдена: плейсхолдеров, ссылок на источник и знаков ТМ нет")

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
