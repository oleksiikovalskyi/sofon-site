/* ============================================================
   Каркас сторінки-прикладу. Сторінка оголошує лише GAL_PAGE =
   {v:'mosaic', title:…, note:…} — решта (три набори зображень
   під одним і тим самим варіантом) збирається тут.
   Один варіант = одна сторінка, без параметрів в адресі.
   ============================================================ */
(function () {
  var P = window.GAL_PAGE;
  var LINKS = [
    ['mosaic', 'Мозаїка'],
    ['pop',    'Мозаїка + підйом'],
    ['strip',  'Стрічка від курсора'],
    ['bay',    'Касета']
  ];

  function bar() {
    return '<div class="proto-bar">ГАЛЕРЕЯ · <b>' + P.name + '</b> · ' +
      LINKS.filter(function (l) { return l[0] !== P.v; })
           .map(function (l) { return '<a href="/home-ab/gal/' + l[0] + '.html">' + l[1] + '</a>'; })
           .join(' ') +
      ' · <a href="/home-ab/f.html">головна-прототип</a></div>';
  }

  function head(eyebrow, h, note, dark) {
    return '<div class="gh"><div><span class="eyebrow' + (dark ? '' : ' eyebrow--muted') + '">' +
      eyebrow + '</span><h2>' + h + '</h2></div><div><p class="' + (dark ? 'on-dark' : 'muted') + '">' +
      note + '</p></div></div>';
  }

  function section(cls, inner) {
    var s = document.createElement('section');
    s.className = 'section ' + cls;
    s.innerHTML = '<div class="container">' + inner + '<div class="gal" data-slot></div></div>';
    return s;
  }

  document.body.insertAdjacentHTML('afterbegin', bar());

  var main = document.createElement('main');
  document.body.appendChild(main);

  var s1 = section('section--mist', head('Головний напрям',
    'Оснастка для переведення лінії на нову пляшку', P.note));
  var s2 = section('', head('Перевірка компонента',
    'Той самий блок на звичайних фото',
    'Тут навмисно змішані цехові знімки й рендери на білому — так буде на реальних сторінках. ' +
    'Розкладка й поведінка ті самі, змінюється лише спосіб посадки зображення: фото кадруємо, ' +
    'рендер вписуємо цілком.'));
  var s3 = section('section--dark', head('Та сама галерея на темній секції',
    'Кольори бере зі сторінки',
    'Аркуш і лінії — окремі змінні, тож блок не переробляється, а перефарбовується. ' +
    'Рендери на білому сюди не годяться: їхня підкладка не розчиняється в темному.', true));

  main.appendChild(s1); main.appendChild(s2); main.appendChild(s3);

  // Кожна розкладка вимагає своєї кратності набору, інакше край рваний:
  // стрічка — по 7 у смузі, мозаїка — по 5, касета — 5 слатів у ряду.
  var strip = P.v === 'strip', mos = P.v === 'mosaic' || P.v === 'pop';
  var osn   = strip ? GAL_OSN14 : mos ? GAL_OSN20   : GAL_OSN10;
  var mix   = strip ? GAL_MIX   : GAL_MIX10;
  var photo = strip ? GAL_PHOTO : GAL_PHOTO10;

  SofonGal.render(s1.querySelector('[data-slot]'), osn, P.v);
  SofonGal.render(s2.querySelector('[data-slot]'), mix, P.v);
  SofonGal.render(s3.querySelector('[data-slot]'), photo, P.v);
})();
