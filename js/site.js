/* ============================================================
   Sofon — поведінка шапки й головної. Один невеликий файл на весь сайт;
   усе всередині мовчки виходить, якщо потрібного блоку на сторінці немає.

   1) Вкладене меню «Продукти» — розкривається наведенням, клік по самому
      пункту веде на хаб /products/.
   2) Кнопка «Зв'язатися» — наведення розкриває швидкі канали, клік веде
      на /contact/ (тому окремого пункту «Контакти» в меню немає).
   3) Фон шапки: над героєм темна напівпрозора, нижче світла напівпрозора.
      Перехід тягне число --np (0…1) від прокрутки і завершується рівно
      там, де герой уходить під шапку. Прив'язка до фіксованих 24px тут
      уже пробувалась — шапка вивалювалась у біле, ще стоячи над фото.
      На сторінках без героя --np одразу 1, тобто шапка світла.
   4) Перемикач напрямів на головній: усі шість панелей лежать у розмітці,
      перемикається клас. Раніше панель перезбиралась на кожне наведення,
      і браузер щоразу заново тягнув фото — звідси була пауза.
   ============================================================ */
(function () {

  /* ---------- 1. вкладене меню ---------- */
  document.querySelectorAll('.nav-item.has-sub').forEach(function (it) {
    var t = null;
    function set(v) { it.dataset.open = v ? '1' : '0'; }
    it.addEventListener('mouseenter', function () { clearTimeout(t); set(1); });
    it.addEventListener('mouseleave', function () { t = setTimeout(function () { set(0); }, 160); });
    it.addEventListener('focusin', function () { set(1); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(0); });
  });

  /* ---------- 2. кнопка зв'язку ---------- */
  (function () {
    var cta = document.getElementById('cta');
    if (!cta) return;
    var btn = cta.querySelector('.cta-btn'), t = null;
    function set(v) {
      cta.dataset.open = v ? '1' : '0';
      if (btn) btn.setAttribute('aria-expanded', v ? 'true' : 'false');
    }
    cta.addEventListener('mouseenter', function () { clearTimeout(t); set(1); });
    cta.addEventListener('mouseleave', function () { t = setTimeout(function () { set(0); }, 160); });
    // клік не перехоплюємо: кнопка — посилання на розділ контактів.
    // На тачскріні, де наведення немає, тап веде туди ж.
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(0); });
    document.addEventListener('click', function (e) { if (!cta.contains(e.target)) set(0); });
  })();

  /* ---------- 3. фон шапки ---------- */
  (function () {
    var HEAD = 72, WIN = 170, LITE = 0.62;
    var hero = document.querySelector('.hf');
    var raf = null;
    if (!hero) {                       // сторінка без героя — шапка світла одразу
      document.body.style.setProperty('--np', 1);
      document.body.classList.add('np-lite');
      return;
    }
    function calc() {
      raf = null;
      var end = hero.offsetTop + hero.offsetHeight - HEAD;
      var np = (window.scrollY - (end - WIN)) / WIN;
      np = np < 0 ? 0 : np > 1 ? 1 : np;
      document.body.style.setProperty('--np', np.toFixed(3));
      // текст перекидаємо не на півдорозі, а коли планка вже переважно світла:
      // інакше і текст, і фон сходяться в один сірий і пункти провалюються
      document.body.classList.toggle('np-lite', np > LITE);
    }
    function onScroll() { if (!raf) raf = requestAnimationFrame(calc); }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    calc();
  })();

  /* ---------- 5. прожектор за курсором ----------
     Пляма щільнішої фактури йде за вказівником, як лампа над кульманом.
     Механізм СПІЛЬНИЙ, а не власність шапки: той самий ефект просили і на
     смузі з колажем посеред сторінки, тож блоки перелічені селектором, кожен
     дістає свій шар і свої --mx/--my, а що саме проявляється — вирішує CSS
     конкретного блоку. `?fx=off` вимикає — лишено для порівняння.
     Пробувались і зняті власником (26-07): візир у дві лінії через усю смугу
     і паралакс деталі. Обидва виглядали гірше за спокійний прожектор.

     Уся геометрія віддається в CSS змінних, JS нічого не малює.
     `?mx=&my=` (частка 0…1) ставить пляму вручну — це для headless-знімків:
     у панелі браузера rAF не працює і курсора немає, тож інакше ефект не
     побачити. Той самий прийом, що `?sx=` для стрічки-галереї. */
  (function () {
    var q = new URLSearchParams(location.search);

    // Тло шапки більше не перемикається параметром: сітку власник відхилив
    // остаточно (26-07), колаж вмикається класом .phead--collage у розмітці —
    // так він лишається лише там, де креслення справді про цей розділ.
    var zones = document.querySelectorAll('.phead--sheet, .cband');
    if (!zones.length) return;
    var off = q.get('fx') === 'off';
    var forced = q.get('mx');

    zones.forEach(function (zone) {
      zone.dataset.fx = off ? 'off' : 'spot';
      if (off) return;

      var fx = document.createElement('span');
      fx.className = 'spot-fx';
      fx.setAttribute('aria-hidden', 'true');
      zone.insertBefore(fx, zone.firstChild);

      function put(x, y) {
        zone.style.setProperty('--mx', x.toFixed(1) + 'px');
        zone.style.setProperty('--my', y.toFixed(1) + 'px');
      }

      if (forced !== null) {                  // режим знімка: курсора немає
        var r0 = zone.getBoundingClientRect();
        put(parseFloat(forced) * r0.width, parseFloat(q.get('my') || 0.5) * r0.height);
        return;
      }

      var raf = null, lx = 0, ly = 0;
      function apply() { raf = null; put(lx, ly); }
      zone.addEventListener('pointermove', function (e) {
        // тільки миша: на тачскріні «курсора» немає, а тап лишив би пляму висіти
        if (e.pointerType && e.pointerType !== 'mouse') return;
        var r = zone.getBoundingClientRect();
        lx = e.clientX - r.left; ly = e.clientY - r.top;
        if (!raf) raf = requestAnimationFrame(apply);
      }, { passive: true });
      zone.addEventListener('pointerleave', function () {
        zone.style.setProperty('--mx', '-999px');
        zone.style.setProperty('--my', '-999px');
      });
    });
  })();


  /* ---------- 6. службове: примусове наведення для знімків ----------
     `?hot=N` вмикає стан наведення на N-й плитці галереї (нумерація з 1).
     Потрібне тільки для headless-знімків: у панелі браузера курсора немає,
     тож інакше розкриту касету не побачити. На бойовій сторінці параметра
     немає — код мовчки виходить. */
  (function () {
    var n = parseInt(new URLSearchParams(location.search).get('hot'), 10);
    if (!n) return;
    var tiles = document.querySelectorAll('.gal .gal-i');
    var el = tiles[n - 1];
    if (!el) return;
    el.classList.add('is-hot');
    // у стрічці пригасання сусідів вмикає клас на полотні — без нього знімок
    // показував би підйом, але не показував фокус
    if (el.parentElement) el.parentElement.classList.add('has-hot');
  })();

  /* ---------- 4. напрями на головній ---------- */
  (function () {
    var list = document.getElementById('idx-list');
    if (!list) return;
    var rows = list.querySelectorAll('.idx-row');
    var panes = document.querySelectorAll('.idx-prev-in');
    function show(i) {
      rows.forEach(function (r, j) { r.setAttribute('aria-current', j === i ? 'true' : 'false'); });
      panes.forEach(function (p, k) { p.classList.toggle('on', k === i); });
      // панелі не перестворюються, тож поява підпису сама не повториться —
      // перезапускаємо анімацію вручну (reflow між зняттям і поверненням)
      ['.idx-prev-veil', '.idx-prev-body'].forEach(function (sel) {
        var el = panes[i] && panes[i].querySelector(sel);
        if (!el) return;
        el.style.animation = 'none'; void el.offsetWidth; el.style.animation = '';
      });
    }
    rows.forEach(function (r, i) {
      r.addEventListener('mouseenter', function () { show(i); });
      r.addEventListener('focus', function () { show(i); });
    });
    show(0);
  })();

})();
