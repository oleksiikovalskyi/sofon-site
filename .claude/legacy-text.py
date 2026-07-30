# Витягує текстовий шар зі збережених сторінок старого сайту.
# Elementor лишає по 150-200 КБ розмітки на сторінку; читати це очима неможливо,
# а сам текст — єдине, що нам звідти потрібно (факти для нових сторінок).
#   py .claude/legacy-text.py            -> docs/legacy-site/text/*.txt
#   py .claude/legacy-text.py format-parts  -> друкує одну сторінку в консоль
import html
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "legacy-site" / "pages"
OUT = ROOT / "docs" / "legacy-site" / "text"


def extract(path: Path) -> str:
    s = path.read_text(encoding="utf-8", errors="replace")
    s = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?is)<!--.*?-->", " ", s)
    # блокові теги -> перенос рядка, щоб абзаци не злипались в одну стрічку
    s = re.sub(r"(?i)<(br|/p|/div|/h[1-6]|/li|/td|/tr)[^>]*>", "\n", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html.unescape(s)
    lines = [re.sub(r"[ \t\xa0]+", " ", ln).strip() for ln in s.split("\n")]
    return "\n".join(ln for ln in lines if ln)


def main() -> None:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(sys.argv) > 1:
        print(extract(SRC / f"{sys.argv[1]}.html"))
        return
    OUT.mkdir(exist_ok=True)
    for page in sorted(SRC.glob("*.html")):
        text = extract(page)
        (OUT / f"{page.stem}.txt").write_text(text, encoding="utf-8")
        print(f"{page.stem:20} {len(text.splitlines()):4} рядків")


if __name__ == "__main__":
    main()
