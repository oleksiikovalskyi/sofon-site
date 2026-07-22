#!/usr/bin/env bash
# Sofon site — статичний асемблер. Джерело правди: _src/.
# Кожна сторінка = header + body(_src/pages/*.html) + footer.
# Додати сторінку: 1) створити _src/pages/<name>.html (лише вміст <main>),
#                  2) додати рядок у PAGES нижче, 3) запустити ./build.sh
set -euo pipefail
cd "$(dirname "$0")"
H=_src/header.html; F=_src/footer.html

# out_path | page_id | body | title | desc
PAGES=$(cat <<'ROWS'
index.html|home|home|Sofon — обладнання для ліній розливу напоїв і води|Проєктуємо та виготовляємо оснастку, нестандартне обладнання, конвеєри та автоматику для ліній розливу під ваше технічне завдання.
products/osnastka/index.html|osnastka|osnastka|Оснастка (форматні деталі) — Sofon|Комплекти форматних деталей для переведення лінії розливу на нову пляшку: зірки, ліри, шнеки, турнікетні групи, робота з пробкою, переносники етикетки.
contract-manufacturing/index.html|contract|contract|Контрактне виробництво — токарні та фрезерні роботи — Sofon|Механообробка на замовлення: токарні та фрезерні роботи за вашим кресленням або зразком. Власний верстатний парк.
ROWS
)

n=0
while IFS='|' read -r out page body title desc; do
  [ -z "$out" ] && continue
  mkdir -p "$(dirname "$out")"
  { sed -e "s|__PAGE__|$page|g" -e "s|__TITLE__|$title|g" -e "s|__DESC__|$desc|g" "$H"
    cat "_src/pages/$body.html"
    cat "$F"
  } > "$out"
  echo "  ✓ $out"
  n=$((n+1))
done <<< "$PAGES"
echo "Готово: $n сторінок згенеровано."
