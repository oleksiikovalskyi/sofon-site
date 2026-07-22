# PLAN — Полная айдентика Sofon + пересборка сайта

> **Status:** IN PROGRESS — Фазы 2 (brand guide), 3 (макет сайта) и 5 (информационная
> архитектура, v2) ЗАКРЫТЫ и проверены. Фаза 1 (знак/символ) на паузе — результаты слабые,
> отвязана от критического пути, идём с wordmark-only логотипом (см. §7, п.0). Фаза 5
> прошла через пивот позиционирования: флагман — Оснастка (не паллетизатор), добавлена
> новая линия «Контрактное производство», паллетизатор переехал в «Нестандартное
> оборудование» как кейс (см. §8, Фаза 5 v2). **Следующий шаг:** Фаза 6 — сначала обновить
> бриф §1 под новое позиционирование (Оснастка = флагман), затем полный UA/EN рерайт
> контента по карте сайта из §8. Блокера нет — сессия закрывается по решению пользователя
> («выносим в отдельную сессию»), продолжение — Фаза 6 в новой сессии.
> **Создан:** 2026-06-20. **Расширен:** 2026-07-22 (трек «сайт» §8; знак отвязан от
> критического пути; Фаза 5 пересмотрена дважды — глубина нав + пивот позиционирования).
> **Направление:** отдельное (вне бухгалтерской очереди MASTER-PLAN — не деловой/скиловый
> процесс, а брендинг/сайт; в MASTER-PLAN сознательно не выносится, см. ниже).
> **Цель следующей сессии:** обновить §1 (бриф) под новое позиционирование → прогнать
> рерайт контента (Фаза 6, UA+EN) по карте сайта из §8 → перед версткой (Фаза 7) зафиксировать
> URL-схему двуязычности (открытый вопрос в §8).

---

## 0. Решения по scope

**Зафиксировано 20-06 (айдентика):**

| Вопрос | Решение |
|---|---|
| Что выдаёт claude.ai/design | **Логотип + знак**, **Brand guide (дизайн-код)**, **Макет сайта** |
| Язык бренда и носителей | **Двуязычный UA + EN** (UA — основной, EN — экспортная версия) |
| Наследие | Сохраняем **только имя «Софон / Sofon»**. Знак, палитра, типографика — с нуля |
| Референсы | arol.com, kosme.com, khs.com — индустриальный B2B-язык розливного оборудования |

**Что это значит на практике:** полный редизайн визуала. Дизайнеру не задаём ограничений по
старому логотипу/цвету (текущий — белый wordmark из WordPress-шаблона, наследовать нечего).
Единственный инвариант — нейминг: кириллическое «Софон» + латиница «Sofon» должны работать
вместе (двуязычный логотип или две согласованные версии).

**Зафиксировано 22-07 (сайт — расширение scope на «полную айдентику + сайт»):**

| Вопрос | Решение |
|---|---|
| Платформа сайта | **Пересборка на новой платформе** (не остаёмся на текущем WP/Elementor) |
| Формат сборки | **Голый HTML/CSS, без CMS** — статические страницы, без бэкенда. Пробуем этот подход первым, по ходу смотрим, где упрёмся |
| Объём рерайта контента | **Полный рерайт UA + EN** — не перевод текущего RU, новый текст под тон бренда |
| Публикация | **Пользователь публикует сам** — Claude готовит макет/контент/сборку, деплой на хостинг делает пользователь |

Текущий сайт (справка): sofon.com.ua, WordPress + Elementor, тема с 2020 года, контент
только RU, структура по видам оборудования (Паллетизатор / Форматные части / Запчасти /
Нестандартное / Автоматика / Конвейеры / Оборудование линий розлива / Контакты), аналитика
через GTM (GTM-TD87WM8), контактный email les@immach.com.

**Зафиксировано 22-07 вечер (Фаза 1 — знак/символ, попытка неудачна):**

| Вопрос | Решение |
|---|---|
| Итог первой попытки (Промт A, kite/dart, Sonnet 5) | **Слабо/мимо** — результаты не читались как логотип, не держали концепцию мозаики Пенроуза (со слов пользователя: «неудача»), не «грязные варианты», а именно не туда |
| Приоритет: знак vs остальная айдентика | **Отвязать.** Знак — НЕ блокирует Фазу 2/3. Идём в brand guide и макет сайта с **wordmark-only** («Sofon» / «Софон» одной типографикой, без отдельного символа) |
| Судьба Промта A / идеи kite/dart | Не отменяется — в резерве как отдельная задача (см. §7), возврат к ней позже: другая модель (Opus, если доступна), более узкий промт (один концепт за раз вместо 3–5), либо человек-дизайнер |

---

## 1. Краткое описание компании (бриф для дизайнера)

> Это «company brief», который вставляется в каждый промт к дизайнеру как контекст.
> Ниже три версии: рабочая (RU — для нас), и две «боевые» (EN + UA — для вставки в инструмент).

### 1.1 Рабочая версия (RU, для понимания)

Sofon (ТОВ «СОФОН») — украинский инженерно-производственный завод, проектирующий и
изготавливающий оборудование для линий розлива напитков и воды. Делаем как **серийные
машины** (флагман — паллетизатор для бутылей 19 л, производительность 1400 бут/час), так
и **нестандартное оборудование под ТЗ заказчика**: конвейерные системы, форматные детали
для перевода линий на новую бутылку, запасные части, системы автоматики и управления,
подбор/восстановление/запуск оборудования линий розлива. Работаем со стеклом, PET, бутылью
5 л и 19 л, флаконами, банкой. Сильные стороны: инженерная кастомизация, компактные
решения под конкретный цех, качественная компонентная база (автоматика Delta Electronics,
пневматика Camozzi). Позиционирование, к которому идём, — украинский аналог Arol/KHS/Kosme:
серьёзный нишевой производитель розливного оборудования с инженерной экспертизой.

### 1.2 EN brief (вставлять в claude.ai/design)

```
COMPANY: Sofon (Софон)
INDUSTRY: Industrial machinery for beverage & water bottling/filling lines (B2B)
WHAT WE DO: We design and manufacture equipment for bottling lines — both standard
machines and fully custom, engineered-to-spec solutions. Flagship product: an automatic
palletizer for 19-liter water bottles (1,400 bottles/hour). We also build conveyor
systems, format/change parts (to switch a line to a new bottle), spare parts, automation
and control systems, and we select, refurbish and commission complete filling lines.
We work with glass, PET, 5L and 19L bottles, flacons and cans.
STRENGTHS: engineering customization, compact in-plant layouts, premium components
(Delta Electronics automation, Camozzi pneumatics), responsive support.
POSITIONING: a serious Ukrainian specialist in bottling-line equipment — the local
counterpart to international players like Arol, KHS and Kosme.
PERSONALITY: engineering-grade, precise, reliable, no-nonsense, modern-industrial.
NOT: cheap, flashy, consumer, playful.
AUDIENCE: technical buyers and plant managers at beverage/water producers.
NAME CONSTRAINT: keep the name "Sofon" (Latin) / "Софон" (Cyrillic) — bilingual brand.
```

### 1.3 UA brief (для UA-версии носителей)

```
КОМПАНІЯ: Sofon (ТОВ «СОФОН»)
ГАЛУЗЬ: Промислове обладнання для ліній розливу напоїв та води (B2B)
ЩО РОБИМО: Проєктуємо та виготовляємо обладнання для ліній розливу — серійні машини
та нестандартні рішення під ТЗ замовника. Флагман: автоматичний палетизатор для
19-літрових бутлів (1400 пляшок/год). Також: конвеєрні системи, форматні деталі,
запасні частини, системи автоматики й керування, підбір/відновлення/запуск ліній
розливу. Працюємо зі склом, PET, бутлями 5 л і 19 л, флаконами, банкою.
СИЛЬНІ СТОРОНИ: інженерна кастомізація, компактні рішення під цех, якісна
компонентна база (Delta Electronics, Camozzi).
ХАРАКТЕР БРЕНДУ: інженерний, точний, надійний, сучасно-промисловий.
```

---

## 2. Анализ референсов — общий дизайн-код

Что объединяет Arol, KHS и Kosme (визуальная ДНК ниши, которую перенимаем):

**Палитра.** Минимализм: белый/светло-серый фон + один сильный акцент. KHS — холодный
сине-зелёный «инженерный» акцент; Arol — нейтральный с тёмным графитом; общий принцип —
много воздуха, акцент дозировано (кнопки, заголовки, иконки), без «радуги». Kosme — контр-
пример внутри той же ниши: фирменный тёплый оранж-красный (~#E85D1D), причём насыщенный
и заметно более смелый, чем у Arol/KHS (сплошной оранжевый фон на fullscreen-меню). Вывод
для Sofon: оба полюса легитимны внутри ниши — «сдержанный инженерный» (синий/графит) и
«энергичный» (насыщенный оранж/янтарь) — что подтверждает гипотезу варианта B в §3, а не
отменяет вариант A.

**Типографика.** Промышленный гротеск (sans-serif): чистый, геометричный, хорошо читается
в верхнем регистре заголовков. Крупные уверенные заголовки + спокойный текст. Никаких
засечек и декоративных шрифтов. Kosme подтверждает паттерн: геометричный гротеск, лёгкое
начертание в hero-заголовках, мелкий капс для лейблов разделов.

**Фотография.** Главный носитель доверия — продуктовые фото машин на нейтральном/seamless
фоне + кадры с производства/линий. Видео-герой на главной (Arol). Реальное железо, не
рендеры-картинки. Kosme здесь расходится с Arol/KHS: наряду с реальными фото завода и цеха
использует стилизованные 3D-рендеры продукта (бутылки в брызгах на тёмном фоне с неоновым
контуром) — приём более «маркетинговый»/consumer-style. Для Sofon это НЕ берём — держим
курс на реальное железо (см. §3), рендер-эстетика противоречит инженерному позиционированию.

**Навигация — по применениям.** Сильнейший приём: меню строится вокруг отраслей/продуктов
клиента (Beverage / Water / Juice / Dairy / Beer …) и решений (машины / конвейеры /
запчасти / автоматика). Плитки секторов с иконками (Arol). Kosme — тот же принцип: раздел
Products организован по отраслям (Water, CSD, Beer, Wine, Spirits, Milk & Dairy, Oil,
Personal Care, Home Care, Chemicals), не по типам оборудования. Sofon уже фактически так
устроен (паллетизатор / форматные / запчасти / нестандарт / автоматика / конвейеры).

**Сигналы доверия.** Крупные числа (Arol: «700+ машин/год, 25 000 установлено»; KHS:
«150 лет»), сертификации, отзывы клиентов, участие в выставках, «единый источник /
turnkey». Kosme — отдельный паттерн: почти не показывает собственных цифр, доверие строит
через принадлежность к материнской группе (Krones — «Krones Solutions», «Krones magazine»
в футере) и текст про глобальную сеть филиалов. Для Sofon такой вариант не подходит (нет
материнского бренда) — держим курс на собственные цифры/факты, как заложено ниже.
Sofon-эквиваленты: производительность 1400 бут/час, кастомизация под ТЗ,
премиум-компоненты, полный цикл (проект→изготовление→монтаж→запуск).

**Тон.** «Надёжный партнёр», «эксперты в…», «решение под любую задачу». Спокойная
уверенность инженеров, без маркетингового шума.

**Структура главной (паттерн для макета Sofon):**
1. Hero: видео/фото машины + слоган + 1 строка позиционирования + CTA.
2. Сетка секторов/продуктов (плитки с иконками).
3. Блок «почему мы» / числа.
4. Флагман (паллетизатор 19 л) — выделенный блок.
5. Отзывы/кейсы (когда появятся).
6. Новости/выставки.
7. Контакты + футер с реквизитами.

(Kosme.com подтверждает общую логику: hero с CTA → блок о компании/миссии → блок
производства/цеха с CTA → блок сервиса (Life Cycle Service) → футер с теглайном и
ссылками на связанные бренды/ресурсы. У Sofon вместо «связанных брендов» — контакты
и реквизиты.)

---

## 3. Дизайн-направление для Sofon (синтез — гипотеза, проверить на дизайнере)

- **Идея знака (приоритетная, от пользователя, 22-07):** мотив тайлов Пенроуза — «kite and
  dart» (апериодическая мозаика: «змей»/kite и «дротик»/dart), стилизованных под стрелку/
  указатель вперёд. Референс-эскизы — `Sophon/brand/references/sofon-logo-idea_kite-dart_*`
  (собственный набросок пользователя в SolidWorks, 2 файла: 3D-вид и плоская развёртка):
  верхняя часть — dart с V-образной вырезкой снизу, читается как наконечник стрелы/шеврон
  вверх; под ним — две половины kite, формирующие основание/«крылья». Идея сильная сама по
  себе: апериодическая мозаика — устоявшийся визуальный код точной геометрии/инженерии
  (ассоциация с квазикристаллами), а форма дротика естественно читается как стрелка —
  что попадает в мотив «направление потока» (розлив/конвейер/паллетизация), уже
  предполагавшийся ниже как альтернатива. Это ведущее направление для Промта A; побочные
  идеи (буква «S», мотив бутылки/потока/звезды-турникета) — как запасные для сравнения.
- Побочные идеи знака: буква «S»; мотив бутылки/потока/паллеты/механического узла
  (звезда-турникет, шнек). Знак простой, читается в монохроме и в фавиконе.
- **Двуязычность:** латиница «Sofon» как основной wordmark (международно), кириллическая
  «Софон» — согласованная версия тем же шрифтом. Знак — общий.
- **Палитра-гипотеза:** графит/тёмно-стальной + чистый белый + один акцент (вариант A:
  индустриальный синий «вода/инженерия»; вариант B: насыщенный оранжевый/янтарный
  «энергия/механика» для отстройки от сине-белого KHS). Дать дизайнеру оба варианта.
- **Типографика:** свободный геометрический/индустриальный гротеск с поддержкой кириллицы
  и латиницы (критично для UA+EN) — напр. семейства уровня Inter / IBM Plex Sans /
  Manrope / Space Grotesk. Просить варианты с обязательной кириллицей.
- **Тон визуала:** воздух, сетка, крупные фото железа, дозированный акцент.

---

## 4. План выполнения (следующая сессия)

> claude.ai/design — внешний инструмент (открывается в браузере). Эта сессия его не
> запускает; здесь — готовый «боезапас». В сессии-выполнении: либо пользователь вставляет
> промты сам, либо просит провести через Claude in Chrome.

**Фаза 1 — Логотип и знак. СТАТУС: остановлена, отвязана от критического пути (22-07).**
1. Промт A (раздел 5.1) прогнан на Sonnet 5 — результаты слабые/мимо концепции kite/dart.
2. Не блокирует Фазы 2–3. Возврат к знаку — отдельная задача, см. §7 (другая модель/более
   узкий промт/человек-дизайнер).

**Фаза 2 — Brand guide (дизайн-код), wordmark-only. СТАТУС: ГОТОВО (22-07), проверено.**
3. Промт B прогнан, результат — `Sofon Brand Guidelines` v1.0. Проверено по чек-листу:
   все 8 секций (Logo / Logo usage / Color / Typography / Iconography / Photography /
   Layout / Tone) присутствуют содержательно, не для галочки — кириллица подтверждена
   реальным рендером «Sofon Софон», фото-раздел явно требует «real steel, not renders»
   (созвучно с решением по Kosme в §2), tone of voice дан на EN+UA, wordmark помечен как
   «symbol slot reserved». Единственный пробел — нет точного пиксельного брейкпоинта для
   mobile (только качественно «collapses on phones») — не критично, зададим сами в Фазе 7.
4. Файлы сохранены: `Sophon/brand/Sofon-Brand-Guidelines-v1.0.html` (полный экспорт) +
   `Sophon/brand/Sofon-Brand-Tokens-v1.0.md` (плоский манифест токенов — HEX, шрифты,
   type scale, spacing, сетка/радиус) — это источник правды для Фазы 3 и для ручной
   вёрстки в Фазе 7.
5. **Акцент НЕ зафиксирован.** Design рекомендует Amber `#F07C1A` (обоснование: отстройка
   от синего KHS, перекликается с тёплым акцентом Kosme); альтернатива — Engineering Blue
   `#1466D8`. Пользователь пока не решил — идём в Фазу 3 с Amber как рабочим дефолтом
   (рекомендация инструмента), финальный выбор можно переключить позже (документ
   интерактивный, оба варианта уже собраны).

**Фаза 3 — Макет сайта.**
6. Вставить Промт C (5.3) с дизайн-кодом из Фазы 2 (токены — `Sofon-Brand-Tokens-v1.0.md`,
   акцент — Amber как рабочий дефолт). Получить макет главной (по структуре из §2) +
   шаблон страницы продукта (паллетизатор 19 л) + карточку оборудования. Header —
   с wordmark-only логотипом (без знака).
7. Итерации по hero, сетке секторов, мобильной версии.

**Фаза 4 — Сборка и сохранение.**
8. Собрать результаты (экспорт из инструмента) в `Sophon/brand/`: wordmark, brand-guide
   (уже там, v1.0), скрины макетов.
9. Обновить этот план статусом DONE / вынести остаток (включая нерешённую задачу знака и
   финальный выбор акцента).

**Бюджет/риски:** итеративный визуальный процесс — закладывать несколько проходов на
каждую фазу; не пытаться получить финал с первого промта. Brand guide — ДО макета (каждая
фаза наследует предыдущую). Знак больше не в критическом пути — можно доделать в любой
момент и подставить в уже готовый brand guide/сайт задним числом.

---

## 5. Готовые промты для claude.ai/design

> Язык промтов — английский (инструмент так стабильнее), плюс явное требование кириллицы.
> Перед каждым промтом вставляется **EN brief из §1.2**. Плейсхолдеры в `<…>` заполнить.

### 5.1 Промт A — Логотип и знак

```
You are a senior brand identity designer for industrial B2B companies.

[PASTE COMPANY BRIEF FROM §1.2 HERE]

TASK: Design a logo system for "Sofon".

LEAD CONCEPT (explore this first, most thoroughly — see attached reference sketches):
A mark built from Penrose tiling geometry — the two aperiodic tiling shapes known as
"kite" and "dart" — stylized into a simple forward-pointing arrow / chevron. In the
attached sketch, a dart shape (a concave quadrilateral with a V-notch) forms an
upward/forward-pointing arrowhead, sitting above two kite-half shapes that form a base
or "wings". Explore this as: (a) close to the attached sketch, (b) more abstracted/
simplified variations of the same kite+dart arrow idea (different proportions, fewer
facets, alternate arrow directions). The Penrose-tiling reference should read as precise,
mathematical, engineering-grade — not decorative. The arrow/forward motion also doubles
as a metaphor for line flow / product moving through the line.

ALSO EXPLORE (secondary directions, for comparison only):
- The letter "S".
- A bottling motif (bottle / liquid flow / palletized stack / a mechanical detail like a
  star-wheel, worm-screw or guide rail).
Keep all directions abstract and timeless, not literal/clip-art.

REQUIREMENTS:
- A distinctive, simple brand mark (symbol) + a wordmark.
- Bilingual: the primary wordmark is Latin "Sofon"; also produce a matching Cyrillic
  version "Софон" in the SAME typeface. The mark must work with both.
- Must be legible in a single color (black on white AND white on dark) and as a 16px
  favicon.
- Style: modern-industrial, engineering-grade, precise, confident. Reference the visual
  language of Arol, KHS and Kosme (clean, restrained, premium). NOT playful, NOT
  consumer, NOT gradient-heavy.

DELIVER:
- 3 to 5 distinct logo concepts, with the Penrose kite/dart arrow direction as the lead
  concept (show 2-3 variations of it) plus 1-2 from the secondary directions for
  comparison. For each: the mark alone, the mark + Latin wordmark (horizontal lock-up),
  and a one-line rationale.
- For the strongest concept, also show: vertical lock-up, Cyrillic "Софон" version,
  monochrome version, and a favicon-size preview.
- Suggest the typeface used (must support both Latin and Cyrillic).

ATTACH: sofon-logo-idea_kite-dart_3d-sketch.png and sofon-logo-idea_kite-dart_flat.png
(the user's own reference sketches for the lead concept, from Sophon/brand/references/).
```

### 5.2 Промт B — Brand guide (дизайн-код)

```
You are a senior brand designer building a brand guideline.

[PASTE COMPANY BRIEF FROM §1.2 HERE]

CONTEXT: We do NOT have a finished symbol/mark yet (an earlier attempt at a bespoke mark
did not work out and is on hold as a separate track). For now the logo is WORDMARK-ONLY:
the name "Sofon" set in a strong, precise, geometric sans-serif, plus a matching Cyrillic
"Софон" version in the same typeface. Do not invent a new symbol/icon-mark — treat the
wordmark itself (with careful letter-spacing/weight) as the logo for this system. Build a
complete visual identity system ("design code") around this wordmark-only logo. Leave
clear room in the system (spacing, favicon slot, lock-up rules) for a symbol/mark to be
added later without breaking the system.

DELIVER a brand guide covering:
1. Color palette — primary, secondary and one accent, with HEX/RGB values, light & dark
   usage, and accessible text/background pairings. Propose TWO accent options:
   (A) an engineering blue, (B) a strong amber/orange — and recommend one with reasoning.
   Keep the system minimal (white/light + graphite + one accent), in line with Arol/KHS.
2. Typography — a type family supporting BOTH Latin and Cyrillic (e.g. Inter / IBM Plex
   Sans / Manrope / Space Grotesk class). Define a type scale: H1–H4, body, caption,
   with weights and use cases. Show sample headings in EN and UA. Also show the wordmark
   itself set in this family as the logo lock-up (Latin + Cyrillic versions).
3. Logo usage — clear space, minimum size, correct/incorrect usage, on photo, mono. Note
   where a future symbol/mark would attach (e.g. favicon, left of wordmark) once designed.
4. Iconography — a thin/medium line icon style for product sectors (palletizer,
   conveyors, format parts, spare parts, automation, custom equipment). Show ~6 sample
   icons.
5. Photography & imagery style — direction for machine/product shots on neutral seamless
   backgrounds and factory-floor context shots (per Arol/KHS).
6. Layout system — grid, spacing scale, button styles, card styles.
7. Tone of voice — short EN + UA, engineering-grade and reliable ("expert partner").

OUTPUT as a clean, presentable brand-guide layout.
```

### 5.3 Промт C — Макет сайта

```
You are a senior web/UI designer for industrial B2B manufacturers.

[PASTE COMPANY BRIEF FROM §1.2 HERE]

CONTEXT: Apply this brand design code: <ВСТАВИТЬ палитру HEX + шрифты + кнопки/карточки
из Фазы 2>. Design a modern website for Sofon, bilingual UA/EN (design in EN, note where
the UA toggle lives).

PAGES / SCREENS TO DESIGN:
1. HOMEPAGE, with this section order:
   - Hero: full-width machine photo or video, headline ("Equipment for bottling lines"
     / engineering tagline), one supporting line, primary CTA (Contact / Get a quote),
     EN/UA language switch.
   - Sector/product grid: tiles with icons — Palletizer 19L, Conveyor systems, Format
     parts, Spare parts, Automation & control, Custom equipment, Filling-line equipment.
   - "Why Sofon" / key numbers strip (e.g. 1400 bottles/hour, engineered-to-spec,
     premium components Delta/Camozzi, full cycle: design→build→install→commission).
   - Flagship spotlight: the 19L palletizer (photo + key specs).
   - News / trade shows placeholder.
   - Contact block + footer with company details.
2. PRODUCT PAGE template — using the 19L palletizer (hero, description, specifications
   table, gallery, auxiliary equipment, CTA).
3. A product/sector CARD component (reused in the grid).

REQUIREMENTS:
- Visual language: clean, spacious, white/light + accent, large product photography —
  match the seriousness of arol.com / khs.com / kosme.com.
- Show DESKTOP and MOBILE versions of the homepage hero + sector grid.
- Use realistic placeholder copy from the brief (not lorem ipsum where possible).

DELIVER high-fidelity mockups for the screens above.
```

---

## 6. Критерии приёмки

- [ ] Wordmark читается в моно, на тёмном/светлом, в фавиконе; есть кириллическая «Софон».
      (Символ/знак — отдельно, см. §7, п.0; не входит в критерии этой фазы.)
- [ ] Палитра задана в HEX; выбран один акцент; система минималистична (как у референсов).
- [ ] Шрифт поддерживает кириллицу И латиницу (проверить на «Софон»/«Sofon»).
- [ ] Макет главной собран по структуре §2; есть desktop + mobile; есть шаблон продукта.
- [ ] Всё выглядит на уровне Arol/KHS/Kosme: чисто, дорого, инженерно.
- [ ] Результаты сохранены в `Sophon/brand/`.

## 7. Открытые вопросы (решить в сессии-выполнении или с пользователем)

0. **Знак/символ (backlog, отвязан 22-07).** Первая попытка (Промт A, kite/dart, Sonnet 5)
   дала слабые/нецелевые результаты. Идём дальше без символа (wordmark-only), к этой задаче
   возвращаемся отдельно, когда будет время. Варианты для повторной попытки: (a) другая
   модель в дропдауне Claude Design, если доступен Opus; (b) сузить промт — просить ОДИН
   концепт за раз вместо 3–5 сразу, с более пошаговым уточнением; (c) отдать символ
   отдельно человеку-дизайнеру/фрилансеру, а brand guide и сайт продолжать через
   claude.ai/design. Референс-эскизы пользователя остаются в
   `Sophon/brand/references/sofon-logo-idea_kite-dart_*` — годятся для любого из вариантов.
1. Акцентный цвет — синий (как KHS, «вода/инженерия») или оранжевый/янтарный (отстройка)?
   Дизайнер предложит оба; финальный выбор — за пользователем.
2. Слоган/тэглайн — нужен ли единый («Equipment for bottling lines» / инженерный девиз)?
3. Есть ли качественные фото машин в высоком разрешении для макета (или брать с текущего
   сайта/со съёмки)?
4. Домен/нейм латиницей: «Sofon» против текущего «sofon.com.ua» — оставляем как есть.

> Сайт (реализация после этой фазы) — см. §8.

---

## 8. Трек «Сайт» — план действий (зафиксирован 22-07)

> Отдельный от айдентики поток работ. Стартует ПОСЛЕ Фазы 2 (brand guide утверждён) —
> контент и сборка наследуют палитру/типографику/тон, определённые в §5.2. Макет из Фазы 3
> (§5.3) — визуальная основа для сборки, не финальный html/css.

**Фаза 5 — Информационная архитектура. СТАТУС: ГОТОВО, v2 (22-07 ночь, пересмотрено дважды).**

Первый заход (v1) пересмотрел только глубину меню (группировка вместо плоского списка) и
добавил About/News. Второй, более важный пересмотр — **позиционирование**: пользователь
уточнил реальную структуру бизнеса, и она отличается от того, что было зашито в бриф с
20-06 (там флагманом считался паллетизатор 19 л — это унаследовано ВЕЗДЕ: brand guide
«Why Sofon», мокап «Flagship spotlight», product-page template). Реальная картина:

| Линия бизнеса | Было на старом сайте | Статус |
|---|---|---|
| **Оснастка** для оборудования линий розлива | «Форматные детали» | **Флагман, хлеб с маслом** (новое позиционирование) |
| Подбор и поставка оборудования линий розлива | «Оборудование линий розлива» | сохраняется как есть |
| Производство конвейерных систем | «Конвейеры» | сохраняется как есть |
| Разработка систем автоматизации | «Автоматика» | сохраняется как есть |
| Производство запчастей | «Запасные части» | сохраняется как есть |
| Разработка и изготовление нестандартного оборудования | «Нестандартное оборудование» | сохраняется; **паллетизатор 19 л переезжает сюда как кейс/пример**, теряет статус флагмана |
| **Контрактное производство** (токарные/фрезерные работы) | не было вообще | **новая линия, отдельный пункт навигации** — другой сегмент клиентов (заказчики механообработки, не розлив) |

**Финальная карта сайта v2** (UA — основной язык на корневых путях, EN — под `/en/`):

- `/` — Home (flagship-spotlight теперь про Оснастку, не паллетизатор)
- `/products/` — Products hub (сетка из 6 линий, без паллетизатора отдельной плиткой)
- `/products/osnastka/` — **Оснастка** — флагман (+ отдельный шорткат в шапке, замена
  бывшего шортката «Palletizer 19L»)
- `/products/equipment-supply/` — подбор и поставка оборудования линий розлива
- `/products/conveyor-systems/`
- `/products/automation/`
- `/products/spare-parts/`
- `/products/custom-equipment/` — нестандартное оборудование; здесь же кейс/пример
  «Паллетизатор для бутылей 19 л» (переиспользуем уже готовый Product Page Template из
  Фазы 3 — только теперь это витрина-кейс внутри раздела, а не отдельная флагманская
  страница верхнего уровня)
- `/contract-manufacturing/` — **новая страница**, вне `/products/` (другая аудитория):
  hero-позиционирование, перечень работ (токарные/фрезерные), возможности/оборудование,
  отдельный CTA («Разместить заказ» / «Запросить расчёт», не общий «Get a quote» —
  разные сегменты клиентов)
- `/about/`
- `/news/` (лендинг-листинг; отдельные посты `/news/<slug>/` — по мере появления контента,
  не блокирует запуск)
- `/contact/`

Зеркально то же самое под `/en/...` для EN-версии. Итого 12 страниц × 2 языка = 24 файла
(было 12 в v1 — состав линий изменился, количество совпало случайно).

**Навигация в шапке v2:** `Sofon (лого→Home) · Products ▾ (дропдаун: Оснастка вверху
списка + остальные 5 линий) · Оснастка (шорткат на флагман) · Контрактне виробництво ·
About · News · Contact · [EN/UA] · [Get a quote → /contact/]`. Шорткат «Custom equipment»
из v1 убран — вместо него теперь два top-level пункта (Оснастка + Контрактне виробництво),
и нав не разрастается сверх меры.

**Главная страница — что меняется по контенту (детали в Фазе 6):**
- Flagship spotlight → про Оснастку, не паллетизатор.
- Sector grid → 6 плиток (без отдельной плитки «Palletizer 19L»).
- Под сеткой — отдельная не-затерянная полоса/CTA про контрактное производство (другая
  аудитория, не мешаем с розливным продуктовым рядом, но и не прячем).

**Открыто (решить в Фазе 7, не блокирует копирайтинг):** URL-схема двуязычности — мокап
просил только «отметить где живёт переключатель», без выбора между отдельными файлами на
язык (`/en/...`, рекомендуется — статике проще, лучше для SEO, никакого JS) и
JS-переключением текста на одной странице (меньше файлов, но плохо для SEO статики и
добавляет JS-зависимость, которой мы хотели избежать). Рабочая рекомендация — раздельные
файлы, `/en/` — зафиксировать явно перед стартом вёрстки.

**Хвост в §1 (бриф компании):** текст брифа (§1.1–1.3) всё ещё называет паллетизатор
флагманом — это унаследовано в brand guide и мокапе на уровне КОПИРАЙТИНГА (не визуала:
палитра/шрифты/layout не завязаны на то, что именно флагман). Не блокирует остальное, но
бриф стоит обновить в начале Фазы 6, чтобы копирайтинг сразу шёл от правильного
позиционирования (Оснастка — флагман), а не от старого текста.

**Принцип на будущее — новые направления уровня флагмана (зафиксировано 22-07 ночь).**
Стресс-тест на гипотетическом примере (сценические лебёдки — вертикаль вне розлива):
- Если новое направление **той же отрасли/аудитории**, что и текущие продукты (розлив/
  инженерия под ТЗ клиента) — размещаем внутри `/products/custom-equipment/`
  («Нестандартное оборудование») как ещё один кейс/пример, ничего не перестраивая.
- Если новое направление — **другая вертикаль/аудитория** (другой тон, другие клиенты,
  как гипотетические лебёдки) — **НЕ впихиваем в этот сайт и в этот бренд.** Отдельный
  сайт под отдельным брендом, с этого сайта — только ссылка (паттерн «семьи брендов»,
  который мы уже видели у KHS/Kosme в футере: competence.khs.com, connect.khs.com и т.д.
  — см. §2). Не строим сейчас (гипотеза), просто фиксируем как решение на случай, если
  материализуется — чтобы не перестраивать нав/структуру задним числом.

**Фаза 6 — Контент (полный рерайт UA + EN).**
3. Для каждой страницы карты сайта — новый текст на UA (основной) и EN (экспортная версия),
   в тоне бренда из brand guide (§5.2, п.7 tone of voice). НЕ перевод текущего RU-текста —
   новый копирайтинг с нуля, RU-контент используется только как источник фактов
   (характеристики, комплектация, позиционирование по продуктам).
4. Проверить факты по каждому продукту с пользователем перед финализацией (парсер не
   угадывает: если характеристики из старого сайта устарели/неполны — уточнить, не
   додумывать).

**Фаза 7 — Сборка.**
5. Собрать сайт голым HTML/CSS (без CMS/фреймворка/бэкенда) на основе макета Фазы 3 и
   текста Фазы 6 — multi-page статические файлы с UA/EN переключателем (JS по минимуму,
   только там где без него не обойтись — переключатель языка, мобильное меню). Пробуем
   этот подход первым; если упрёмся в ограничение (например форма обратной связи — см.
   открытые вопросы ниже), решаем по месту, не меняя подход заранее.
6. Адаптивная вёрстка (desktop + mobile) по референсам из макета.

**Фаза 8 — Передача.**
7. Финальная сборка (файлы + brand-guide + исходники логотипа) передаётся пользователю
   через `present_files`/сохранение в `Sophon/brand/` — публикацию и выбор хостинга
   пользователь делает сам.
8. Обновить этот план статусом DONE / вынести хвосты (если будут) в ESCALATIONS-BACKLOG.

**Открытые вопросы трека «сайт» (решить перед Фазой 7):**
- Нужны ли на сайте формы (заявка/контакты) — если да, на чём (mailto, сторонний форм-сервис
  типа Formspree/Getform, простой backend) — голый HTML/CSS форму сам не обработает.
- Домен: остаётся ли sofon.com.ua при пересборке, или меняется хостинг вместе с платформой.
