/* ============================================================
   Набори зображень для сторінок-прикладів галереї.
   ⚠ ПІДПИСИ ЧЕРНЕТКОВІ — поставлені за виглядом рендерів, звірити з власником.
   ============================================================ */
var IMG = '/docs/legacy-site/images/';

/* Оснастка — 21 позиція. Кратність визначає розкладка: мозаїка складається зі
   смуг по 5 плиток, чотирирядна стрічка — по 7. Тому тут 21 (3 смуги стрічки),
   а мозаїка бере перші 20. Інакше край виходить рваний.
   В архіві 27 рендерів, але частина з них — той самий вузол під іншим кутом;
   майже однакові кадри прибрано, лишились різні деталі. */
window.GAL_OSN = [
  ['format-4',            'Зірка',                  'транспортна'],
  ['format-1',            'Шнек поділу потоку',     'вхід у карусель'],
  ['format-3',            'Комплект пластин',       'дугові напрямні'],
  ['format-18',           'Ланцюгове кільце',       'поворотний вузол'],
  ['format-17',           'Ліра напрямна',          'секція'],
  ['format-5',            'Зубчастий вінець',       'привід каруселі'],
  ['format-parts-24',     'Кронштейн у зборі',      'кріплення напрямної', 1.16],
  ['format-13-otmfoo694a30fu1bfu6rzdjj8m0qd5ar70nkf8pse8', 'Турнікетна група', 'поділ потоку'],
  ['format-6',            'Турнікетний вузол',      'з підпорами'],
  ['format-8',            'Переносна група',        'дві зірки'],
  ['format-12-otmfoo694a30fu1bfu6rzdjj8m0qd5ar70nkf8pse8', 'Зірка мала', 'проміжна'],
  ['format-15-otmfoo694a30fu1bfu6rzdjj8m0qd5ar70nkf8pse8', 'Подвійна зірка', 'вузол передачі'],
  ['format-7',            'Диск-платформа',         'стіл каруселі'],
  // цих двох рендерів немає білого поля — це крупні кадри впритул,
  // тому вони не «лежать на аркуші», а заповнюють плитку, як фото
  ['format-22',           'Профіль зірки',          'фрагмент', null, 'cover'],
  ['format-23',           'Кріплення столу',        'фрагмент', null, 'cover'],
  ['format-parts-22',     'Вставки напрямні',       'полімер'],
  ['format-29',           'Шнек',                   'інший крок'],
  ['format-2',            'Вузол роботи з пробкою', 'у розрізі'],
  ['format-9-otmfoo694a30fu1bfu6rzdjj8m0qd5ar70nkf8pse8',  'Переносна група', 'варіант'],
  ['format-21-otmfoo694a30fu1bfu6rzdjj8m0qd5ar70nkf8pse8', 'Секція транспортера', 'зі зірками'],
  ['format-14-otmfoo694a30fu1bfu6rzdjj8m0qd5ar70nkf8pse8', 'Група зірок', 'у зборі']
].map(function (p) {
  return { src: IMG + p[0] + '.jpg', title: p[1], sub: p[2], fit: p[4] || 'contain', bright: p[3] };
});

/* Нарізка під розкладки: мозаїка — кратно 5, стрічка — кратно 7,
   касета — 10 (два ряди по п'ять слатів). */
window.GAL_OSN20 = window.GAL_OSN.slice(0, 20);
/* Для стрічки — 14 (дві смуги по 7). Ширше не беремо: полотно має вкладатись
   приблизно у дві ширини чистої зони, інакше горизонтальна прокрутка стає
   різкою — на 21 позиції хід курсора підсилювався вже вдвічі. */
window.GAL_OSN14 = window.GAL_OSN.slice(0, 14);
window.GAL_OSN10 = window.GAL_OSN.slice(0, 10);

/* Змішаний набір: цехові фото + рендери на білому в одному блоці —
   так буде на реальних сторінках. */
window.GAL_MIX = [
  { src: IMG + '19-liter-palletizer-auxiliary-equipment01.jpg', title: 'Транспортер у цеху', sub: 'ділянка розливу', fit: 'cover' },
  { src: IMG + '19-liter-palletizer-01.jpg',                    title: 'Палетизатор 19 л',   sub: 'компонування',    fit: 'contain' },
  { src: IMG + '19-liter-palletizer-auxiliary-equipment07.jpg', title: 'Поворот транспортера', sub: 'нержавіюча сталь', fit: 'cover' },
  { src: IMG + 'bottle-inspector-8.jpg',                        title: 'Інспекційна ділянка', sub: 'у зборі',        fit: 'cover' },
  { src: IMG + 'Cancake-Conveyor-1.jpg',                        title: 'Конвеєр пакування',  sub: 'проєкт',          fit: 'contain' },
  { src: IMG + '19-liter-palletizer-auxiliary-equipment04.jpg', title: 'Лінія в роботі',     sub: 'монтаж',          fit: 'cover' },
  { src: IMG + 'al-cap-head.jpg',                               title: 'Укупорочні головки', sub: 'алюмінієвий ковпачок', fit: 'cover' },
  { src: IMG + 'conveyors-16.png',                              title: 'Сітчастий транспортер', sub: 'вузол',        fit: 'cover' },
  { src: IMG + '19-liter-palletizer-auxiliary-equipment10.jpg', title: 'Ділянка накопичення', sub: 'цех замовника',  fit: 'cover' },
  { src: IMG + 'pe-labeling-plate-1.jpg',                       title: 'Плита етикетувальника', sub: 'PE',           fit: 'contain' },
  { src: IMG + '19-liter-palletizer-auxiliary-equipment02.jpg', title: 'Ділянка транспортера', sub: 'цех замовника',  fit: 'cover' },
  { src: IMG + '19-liter-palletizer-05.jpg',                    title: 'Захват палетизатора', sub: 'вузол',           fit: 'contain' },
  { src: IMG + '19-liter-palletizer-auxiliary-equipment05.jpg', title: 'Подача пляшки',      sub: 'ділянка',          fit: 'cover' },
  { src: IMG + 'pet-head-2.jpg',                                title: 'Головка PET',        sub: 'у розрізі',        fit: 'contain' }
];
window.GAL_MIX10 = window.GAL_MIX.slice(0, 10);

/* Тільки фото — для темної секції: рендери на білому там не працюють,
   їхня підкладка не розчиняється в темному фоні. */
window.GAL_PHOTO = [
  { src: IMG + '19-liter-palletizer-auxiliary-equipment01.jpg', title: 'Транспортер у цеху', sub: 'ділянка розливу', fit: 'cover' },
  { src: IMG + '19-liter-palletizer-auxiliary-equipment07.jpg', title: 'Поворот транспортера', sub: 'нержавіюча сталь', fit: 'cover' },
  { src: IMG + 'bottle-inspector-8.jpg',                        title: 'Інспекційна ділянка', sub: 'у зборі',        fit: 'cover' },
  { src: IMG + '19-liter-palletizer-auxiliary-equipment04.jpg', title: 'Лінія в роботі',     sub: 'монтаж',          fit: 'cover' },
  { src: IMG + 'al-cap-head.jpg',                               title: 'Укупорочні головки', sub: 'ковпачок',        fit: 'cover' },
  { src: IMG + '19-liter-palletizer-auxiliary-equipment08-1.jpg', title: 'Транспортер',      sub: 'ділянка',         fit: 'cover' },
  { src: IMG + '19-liter-palletizer-auxiliary-equipment11.jpg', title: 'Накопичувач',        sub: 'цех',             fit: 'cover' },
  { src: IMG + 'manual-rinser-1.jpg',                           title: 'Ручний ополіскувач', sub: 'дрібна серія',    fit: 'cover' },
  { src: IMG + '19-liter-palletizer-auxiliary-equipment10.jpg', title: 'Ділянка накопичення', sub: 'цех замовника',  fit: 'cover' },
  { src: IMG + 'Cancake-Conveyor-2.jpg',                        title: 'Конвеєр пакування',  sub: 'компонування',    fit: 'cover' },
  { src: IMG + '19-liter-palletizer-auxiliary-equipment02.jpg', title: 'Ділянка транспортера', sub: 'цех замовника',  fit: 'cover' },
  { src: IMG + '19-liter-palletizer-auxiliary-equipment03.jpg', title: 'Транспортер',        sub: 'монтаж',           fit: 'cover' },
  { src: IMG + '19-liter-palletizer-auxiliary-equipment05.jpg', title: 'Подача пляшки',      sub: 'ділянка',          fit: 'cover' },
  { src: IMG + '19-liter-palletizer-auxiliary-equipment06.jpg', title: 'Накопичувальний стіл', sub: 'цех',            fit: 'cover' }
];
window.GAL_PHOTO10 = window.GAL_PHOTO.slice(0, 10);
