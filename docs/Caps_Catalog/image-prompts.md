# Промти на генерацію зображень для каталогу пробок

Одна картинка **на клас**, а не на тип. Рішення власника 07-08: типи всередині
класу часто нерозрізненні на фото (алюмінієва кронен-пробка проти сталевої,
короткий ROPP проти довгого), тому чесніше показати клас із розкидом усередині,
ніж підставляти під різні підписи те саме зображення.

**Чому генерація, а не пошук.** Прогін по Wikimedia Commons 07-08 (понад десять
формулювань чотирма мовами, плюс категорії `Corks`, `Bottle stoppers`,
`Wine closures`, `Bottle closures`) показав: Т-подібної пробки й запресовуваних
кришок там **немає взагалі**. Не «шукали не тими словами» — їх просто ніхто не
клав. Зате густо вінних корків і кронен-пробок.

**Спосіб, який спрацював** (власник, 07-08): короткий промт своїми словами
плюс **референс-картинка** у вкладенні. Генерувати в Nano Banana.

---

## Спільний блок стилю

**Дописувати в кінець кожного промта, без змін.** Він і робить набір набором:
вісім картинок мають виглядати як одна серія, а не як добірка з різних сайтів.

```
Plain seamless light grey background, even soft daylight, no props and no
surface texture, a soft shadow under the objects, viewed slightly from above at
about a 30 degree angle, everything in focus, neutral colours, photorealistic,
wide horizontal frame. No text, no numbers, no labels, no logos, no branding,
no watermark, no sparkle, no hands, no packaging.
```

⚠ **Дві заборони в цьому списку не теоретичні** — вони з першої ж вашої
картинки: блискітка-артефакт у правому нижньому куті й намальований текст із
розмірами на пробці в баночці, нечитабельний зблизька. Обидва рядки в промті
знімають це заздалегідь.

⚠ **Тло — рівний світло-сірий, не дерево.** На вашій пробній картинці стіл
дерев'яний, і сам по собі кадр гарний. Але дерево читається як кухня й декор, а
сайт у нас інженерний: сірий фон збігається з кольором `Mist #F3F4F6`, на якому
стоять секції сторінок. Якщо перший кадр лишиться на дереві, а решта сім будуть
на сірому, набір розсиплеться — **Т-подібні варто перегенерувати на тому самому
сірому**.

---

## Як користуватись

По кожному класу нижче: **що має бути в кадрі** → **промт** → **яку картинку
прикріпити референсом**. Референс беріть із `images/` — це реальні фото з
Wikimedia Commons, вони задають генератору правильну форму деталі.

---

## 1. Обтискні · кронен-пробки

```
Make a photo of about twenty beer bottle crown caps of different kinds: plain
silver metal ones, ones with flat single-colour tops, a few turned upside down
so the sealing liner inside is visible, and three or four with a pull-ring tab
on top.
```
*+ спільний блок стилю*

**Референс:** `crown-cork-steel.jpg` і `ring-pull.jpg`.

---

## 2. Накатні · ROPP

```
Make a photo of smooth aluminium bottle caps of the roll-on type, before the
thread is formed: unprinted plain shells in clearly different heights, tall ones
for wine and spirits next to short squat ones for cooking oil, some standing
upright, some lying on their side showing the open bottom edge and the tear-off
band.
```
*+ спільний блок стилю*

**Референс:** `ropp-aluminum.jpg`.

⚠ Головне в цьому кадрі — **різниця висот**: саме довжина ковпачка міняє
укупорювальну головку, і картинка має це показувати.

---

## 3. Гвинтові

```
Make a photo of screw closures of several kinds together: plastic caps for PET
bottles in a few diameters and plain colours, flat wide dairy caps, one large
canister cap, a metal twist-off jar cap shown from underneath so the lugs are
visible, a sport cap with a pull spout, and one cap with a small strip still
attaching it to its tamper ring.
```
*+ спільний блок стилю*

**Референс:** `pet-screw-cap.jpg`, `tethered-cap.jpg`, `twist-off-lug.jpg`.

---

## 4. Запресовувані ⚠ клас без жодного фото

```
Make a photo of snap-on plastic closures without any thread: plain press-on
caps, press-on flip-top caps with a hinged lid — some closed, some flipped open
— and one aluminium cap with a white plastic pouring insert lying next to it.
```
*+ спільний блок стилю*

**Референсу немає** — на Commons таких фото не знайшлось. Тут генератор працює
без опори, тому кадр варто переглянути уважніше за інші.

---

## 5. Коркові

```
Make a photo of wine bottle corks: several natural one-piece corks with visible
pores, several made of pressed cork granules, two champagne corks with the
mushroom head fully expanded, and one unused straight cylindrical champagne cork
next to them for comparison.
```
*+ спільний блок стилю*

**Референс:** `natural-cork.jpg`, `straight-cork.jpg`, `mushroom-cork.jpg`.

⚠ Просити **невживаний циліндр поряд із розправленим грибом** — у цьому вся
суть: до пляшки корок циліндр, після неї гриб.

---

## 6. Т-подібні · bar top

```
Make a photo with several T-shaped bar top bottle stoppers of different kinds:
cork and synthetic bodies, round tops in wood, black plastic and white plastic,
in several diameters and head heights, some standing, some lying on their side.
```
*+ спільний блок стилю*

**Референс:** ваша перша згенерована картинка — форма в ній вийшла правильна.
Перегенерувати треба тільки тло, під сірий, і без баночки з текстом.

---

## 7. Дозувальні системи

```
Make a photo of dispensing closures: two trigger sprayers with their long dip
tubes clearly visible, two pump dispensers — one assembled, one with the pump
head detached from its collar — and one screw cap with a flexible pouring spout
pulled out.
```
*+ спільний блок стилю*

**Референс:** `spray-pump.jpg`, `trigger-sprayer.jpg`.

⚠ **Трубка має бути видна.** Саме вона робить ці вироби найважчими для подачі
розсипом, і саме про це написаний абзац у тексті.

---

## 8. Поза трактом пробки

```
Make a photo of plastic overcaps for aerosol cans in plain colours, a few
snap-on lids for yoghurt cups, and two small white plastic cup-shaped inserts
about the size of a thimble.
```
*+ спільний блок стилю*

**Референс:** `aerosol-cap.jpg`.

*Клас зібраний не за конструкцією, а за межею: це вироби, які закривають тару,
але тракту пробки в нашому розумінні не мають. На сторінці вони корисні саме як
межа нашої території.*

---

# Правила набору

1. **Спільний блок стилю не міняти між класами.** Одне тло, одне світло, один
   кут. Це єдине, що тримає вісім кадрів разом.
2. **Один кадр — один клас.** Не змішувати кронен із гвинтовими «щоб було
   багатше»: клас має читатись із першого погляду.
3. **Ніякого тексту в кадрі.** Генератор малює псевдорозміри й псевдомаркування,
   які зблизька виявляються кашею. На довідковому сайті це найгірший тип
   дефекту: виглядає як дані, а даними не є.
4. **Провенанс записувати** в `images/ATTRIBUTION.md` окремим рядком: модель і
   дата. За півроку має бути видно, де фото реальної деталі, а де ілюстрація.
5. ⬛ `[ рішення власника: як підписуємо згенеровані картинки на сторінці —
   «ілюстрація», чи ніяк ]`

*Фото з Commons і згенеровані кадри в одному ряду виглядатимуть по-різному
навіть за однакового промта. Якщо різниця муляє — простіше згенерувати **всі
вісім** в одному стилі, а знімки з Commons лишити в `verified/` як доказ форми.*
