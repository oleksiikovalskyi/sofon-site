#!/usr/bin/env bash
# Sofon site — статичний асемблер. Джерело правди: _src/.
# Кожна сторінка = header + body(_src/pages/*.html) + footer.
# Додати сторінку: 1) створити _src/pages/<name>.html (лише вміст <main>),
#                  2) додати рядок у PAGES нижче, 3) запустити ./build.sh
# Побічно генерує sitemap.xml із того ж масиву PAGES — щоб карта сайту
# не розʼїжджалася з реальним набором сторінок.
set -euo pipefail
cd "$(dirname "$0")"
H=_src/header.html; F=_src/footer.html

# Кінцевий домен. Використовується в canonical, og:url і sitemap.xml.
# ⚠ Поки сайт стоїть на staging-адресі Vercel — індексація закрита в robots.txt.
SITE_URL="https://sofon.com.ua"
OG_DEFAULT="$SITE_URL/images/og/og-default.jpg"

# out_path | page_id | body | title | desc
PAGES=$(cat <<'ROWS'
index.html|home|home|Sofon — обладнання для ліній розливу напоїв і води|Проєктуємо та виготовляємо оснастку, нестандартне обладнання, конвеєри та автоматику для ліній розливу під ваше технічне завдання.
products/osnastka/index.html|osnastka|osnastka|Оснастка (форматні деталі) — Sofon|Комплекти форматних деталей для переведення лінії розливу на нову пляшку: зірки, ліри, шнеки, турнікетні групи, робота з пробкою, переносники етикетки.
products/osnastka/screws/index.html|osnastka-screws|osnastka-screws|Шнеки поділу потоку пляшок — Sofon|Шнеки поділу потоку під вашу тару: геометрія за замірами обладнання, матеріал під умови ділянки, відтворення зношеного зразка 3D-скануванням.
products/osnastka/turnstiles/index.html|osnastka-turnstiles|osnastka-turnstiles|Турнікетні групи, зірки, ліри й направляючі — Sofon|Турнікетні групи під ваше обладнання: зірки, ліри й направляючі в межах однієї машини, форма кишень під вашу пляшку, заміна плити за замовним номером.
products/osnastka/caps/index.html|osnastka-caps|osnastka-caps|Оснастка системи роботи з пробкою — Sofon|Форматні деталі тракту пробки: змінні елементи орієнтатора, канали подачі, роздавальні диски Pick and Place. Де в тракті ми входимо і чим.
products/osnastka/labeling/index.html|osnastka-labeling|osnastka-labeling|Форматні деталі етикетування — Sofon|Переносники паперової етикетки, столики з донним орієнтатором, центрувальні дзвіночки, щітки й ролики розгладжування — під вашу етикетувальну машину.
products/osnastka/holding/index.html|osnastka-holding|osnastka-holding|Захвати й упори — утримання пляшки — Sofon|Упори під горло PET-пляшок зі сталі 95Х18, вставки проти провертання, подовжувачі захватів горла — під конструкцію вашого автомата.
contract-manufacturing/index.html|contract|contract|Контрактне виробництво — токарні та фрезерні роботи — Sofon|Механообробка на замовлення: токарні, фрезерні та роботи на ЧПК-роутері за вашим кресленням або зразком. Власний верстатний парк.
brand/index.html|brand|brand|Бренд-гайд Sofon — внутрішній довідник|Довідник з бренд-системи Sofon: кольори, типографіка, сітка та компоненти сайту.
products/custom-equipment/index.html|custom-equipment|custom-equipment|Нестандартное оборудование линий розлива — Sofon|Нестандартное оборудование под ТЗ: паллетизатор для бутылей 19 л и другие решения для линий розлива.
products/conveyor-systems/index.html|conveyor|conveyor|Конвейерные системы — Sofon|Конвейерные системы для линий розлива: проект компоновки в цеху, изготовление и поставка конвейеров, шефмонтаж и запуск.
contact/index.html|contact|contact|Контакти — ТОВ «СОФОН» — Sofon|Телефон, пошта, заїзд на виробництво на Бориспільській, відвантаження, реквізити та напрями роботи ТОВ «СОФОН».
ROWS
)

# сторінки, які НЕ мають потрапляти в sitemap.xml (внутрішні/службові)
NOINDEX="brand/index.html"

SITEMAP=sitemap.xml
{
  echo '<?xml version="1.0" encoding="UTF-8"?>'
  echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
} > "$SITEMAP.tmp"

n=0
while IFS='|' read -r out page body title desc; do
  [ -z "$out" ] && continue
  mkdir -p "$(dirname "$out")"

  # канонічний URL: index.html прибираємо, щоб адреса була «чистою»
  url_path="${out%index.html}"
  url="$SITE_URL/${url_path#/}"
  url="${url%/}/"
  [ "$url_path" = "" ] && url="$SITE_URL/"

  { sed -e "s|__PAGE__|$page|g" -e "s|__TITLE__|$title|g" -e "s|__DESC__|$desc|g" \
        -e "s|__URL__|$url|g" -e "s|__OGIMG__|$OG_DEFAULT|g" "$H"
    cat "_src/pages/$body.html"
    cat "$F"
  } > "$out"
  echo "  ✓ $out"
  n=$((n+1))

  case " $NOINDEX " in
    *" $out "*) ;;
    *) printf '  <url><loc>%s</loc></url>\n' "$url" >> "$SITEMAP.tmp" ;;
  esac
done <<< "$PAGES"

echo '</urlset>' >> "$SITEMAP.tmp"
mv "$SITEMAP.tmp" "$SITEMAP"

echo "Готово: $n сторінок згенеровано, sitemap.xml оновлено."
