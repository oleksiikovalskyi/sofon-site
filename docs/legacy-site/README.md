# Legacy site archive — sofon.com.ua

Snapshot of the current live site (WordPress 6.8.6 + Elementor 4.2.0, Astra theme),
captured 2026-07-22, before the rebuild. Purpose: hard factual/asset base for the new
site's copy and imagery — per the plan (`../PLAN_brand-identity-sofon.md`, §8 Фаза 6),
we rewrite tone/structure but anchor facts on what's already published here, not
invent from scratch.

## Contents

- `pages/*.html` — raw HTML source of all 8 live pages (homepage + 7 subpages).
- `images/` — 105 of 106 unique images referenced across those pages, original
  resolution (WordPress thumbnail-size suffixes like `-300x200` stripped before
  download). One (`Untitled19-1.jpg`) is a dead link on the live site itself (404) —
  not a fetch failure on our end.
- `images-list.txt` — the deduped source URL list images were downloaded from.
- `tracking-ids.md` — Google Analytics/Ads/Tag Manager IDs found in the page source.

## Pages captured

| File | URL | Old nav label |
|---|---|---|
| `home.html` | https://sofon.com.ua/ | Паллетизатор 19 л |
| `format-parts.html` | https://sofon.com.ua/format-parts/ | Форматные части |
| `spare-parts.html` | https://sofon.com.ua/spare-parts/ | Запасные части |
| `custom-equipment.html` | https://sofon.com.ua/custom-equipment/ | Нестандартное оборудование |
| `automation.html` | https://sofon.com.ua/automation/ | Автоматика |
| `conveyors.html` | https://sofon.com.ua/conveyors/ | Конвейеры |
| `equipment.html` | https://sofon.com.ua/equipment/ | Оборудование линий розлива |
| `contacts.html` | https://sofon.com.ua/contacts/ | Контакты |

## Known gaps (this was a public-page crawl, not a full export)

- Only content reachable from these 8 pages was captured — any unpublished drafts,
  unlinked media, or pages not in the main nav are missing.
- No alt text / structured data / WordPress metadata extracted yet, only visible
  copy and images.
- If a fuller WordPress/media export becomes available, prefer it over this crawl
  and treat this folder as a fallback.
