/* ============================================================
   Шапка: 1) вкладене меню «Продукти» — відкривається наведенням,
   клік по самому пункту веде на /products/; 2) плавний перехід фону:
   рахуємо --np (0…1) від прокрутки так, щоб він дійшов до 1 рівно
   тоді, коли герой уходить під шапку. Ніяких перемикачів на 24px —
   саме через них шапка «вивалювалась» у біле ще над фото.
   ============================================================ */
(function () {
  /* --- вкладене меню --- */
  document.querySelectorAll('.nav-item.has-sub').forEach(function (it) {
    var t = null;
    function set(v) { it.dataset.open = v ? '1' : '0'; }
    it.addEventListener('mouseenter', function () { clearTimeout(t); set(1); });
    it.addEventListener('mouseleave', function () { t = setTimeout(function () { set(0); }, 160); });
    it.addEventListener('focusin', function () { set(1); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(0); });
    // службове: ?sub=1 — знімок відкритої панелі
    if (new URLSearchParams(location.search).get('sub')) set(1);
  });

  /* --- перехід фону --- */
  var mode = document.body.dataset.nav;
  if (mode !== 'glass' && mode !== 'blend') return;
  var HEAD = 72, WIN = 170;               // WIN — довжина переходу в пікселях прокрутки
  var LITE = 0.62;                        // після цієї межі текст стає темним
  var hero = document.querySelector('.hf');
  var raf = null;

  /* Службове (тільки для знімків): ?np=0..1 фіксує точку переходу.
     Читаємо ДО підписки на події — інакше resize, який headless-браузер
     робить на старті, перерахує --np назад із прокрутки. */
  var forced = parseFloat(new URLSearchParams(location.search).get('np'));
  if (!isNaN(forced)) {
    document.body.style.setProperty('--np', forced);
    document.body.classList.toggle('np-lite', forced > LITE);
    return;
  }
  function calc() {
    raf = null;
    var np = 1;
    if (hero) {
      var end = hero.offsetTop + hero.offsetHeight - HEAD;   // герой пішов під шапку
      np = (window.scrollY - (end - WIN)) / WIN;
      np = np < 0 ? 0 : np > 1 ? 1 : np;
    }
    document.body.style.setProperty('--np', np.toFixed(3));
    // текст перекидаємо не на півдорозі, а коли планка вже переважно світла
    document.body.classList.toggle('np-lite', np > LITE);
  }
  function onScroll() { if (!raf) raf = requestAnimationFrame(calc); }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  calc();
})();
