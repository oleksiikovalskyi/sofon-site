/* ============================================================
   Sofon — стрічка галереї (варіант gal--strip).
   Решта розкладок — чистий CSS, скрипт їм не потрібен; цей файл
   оживляє тільки горизонтальну стрічку, і якщо її на сторінці немає,
   нічого не робить.

   Правила руху (обговорено й затверджено, див. docs/gallery-variants.md):
     · положення курсора по горизонталі → положення полотна, з
       уповільненням біля країв, тож у впор не б'є;
     · полотно доганяє курсор за ~0.3 с, а не стрибає;
     · курсор пішов зі смуги — полотно лишається де було;
     · курсор зупинився — рух завмирає і аж тоді вмикається наведення
       на плитку: підпис і затемнення решти;
     · перша й остання плитки виходять із гасіння повністю, інакше до
       них не дотягнутись.
   ============================================================ */
(function () {
  var REST_MS = 260;   // скільки курсор має простояти, щоб це рахувалось зупинкою
  var REST_PX = 3;     // менші зсуви — тремтіння руки, а не рух
  var EASE = 0.12;     // частка шляху за кадр: це і є ті ~0.3 с

  function initStrip(win) {
    var inner = win.querySelector('.gal--strip');
    if (!inner) return;
    var live = window.matchMedia('(min-width:901px) and (hover:hover)');
    var calm = window.matchMedia('(prefers-reduced-motion:reduce)');
    var max = 0, target = 0, cur = 0, start = 0, raf = null, G = null;
    var restT = null, hotEl = null, lastX = 0, lastY = 0;

    function geom() {
      var box = win.parentElement, w = win.clientWidth, content = w;
      if (box) {
        var cs = getComputedStyle(box);
        content = box.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
      }
      var fade = parseFloat(getComputedStyle(win).getPropertyValue('--gal-fade')) || 200;
      return { w: w, content: content, fade: fade, inn: Math.max(0, (w - content) / 2) };
    }
    function measure() {
      G = geom();
      // на початку лівий край полотна, у кінці правий — рівно на межі чистої зони
      start = G.inn;
      max = Math.max(0, inner.scrollWidth - G.content);
    }
    function smooth(t) { return t * t * (3 - 2 * t); }

    function paint() {
      inner.style.transform = 'translate3d(' + (start - cur).toFixed(2) + 'px,0,0)';
      // гасіння живе тільки з того боку, де за межею справді щось є
      var f = G ? G.fade : 200, inn = G ? G.inn : 0;
      win.style.setProperty('--gal-in-l', inn + 'px');
      win.style.setProperty('--gal-out-l', (inn - Math.min(f, cur)) + 'px');
      win.style.setProperty('--gal-in-r', inn + 'px');
      win.style.setProperty('--gal-out-r', (inn - Math.min(f, max - cur)) + 'px');
    }
    function tick() {
      cur += (target - cur) * EASE;
      if (Math.abs(target - cur) < 0.2) cur = target;
      paint();
      raf = cur === target ? null : requestAnimationFrame(tick);
    }
    function run() {
      if (calm.matches) { cur = target; paint(); return; }
      if (!raf) raf = requestAnimationFrame(tick);
    }

    function clearHot() {
      if (hotEl) { hotEl.classList.remove('is-hot'); hotEl = null; }
      inner.classList.remove('has-hot');
    }
    function armRest(x, y) {
      clearTimeout(restT);
      restT = setTimeout(function settle() {
        // поки полотно ще їде, зупинкою це не рахуємо: підпис спалахнув би
        // на плитці, яка за мить поїде далі
        if (Math.abs(target - cur) > 1.5) { restT = setTimeout(settle, 80); return; }
        var el = document.elementFromPoint(x, y);
        el = el && el.closest ? el.closest('.gal-i') : null;
        if (!el) return;
        hotEl = el; el.classList.add('is-hot'); inner.classList.add('has-hot');
      }, REST_MS);
    }

    win.addEventListener('pointermove', function (e) {
      if (!live.matches) return;
      var r = win.getBoundingClientRect(), g = G || geom();
      var t = (e.clientX - r.left - g.inn) / g.content;   // ведемо в межах чистої зони
      target = smooth(t < 0 ? 0 : t > 1 ? 1 : t) * max;
      if (Math.abs(e.clientX - lastX) > REST_PX || Math.abs(e.clientY - lastY) > REST_PX) clearHot();
      lastX = e.clientX; lastY = e.clientY;
      armRest(e.clientX, e.clientY);
      run();
    });
    win.addEventListener('pointerleave', function () { clearTimeout(restT); clearHot(); });
    window.addEventListener('resize', function () {
      measure();
      if (!live.matches) { inner.style.transform = ''; cur = target = 0; }
      paint();
    });
    // зображення довантажуються після розбору розмітки й міняють ширину полотна
    window.addEventListener('load', function () { measure(); paint(); });
    measure(); paint();
  }

  document.querySelectorAll('.gal-strip').forEach(initStrip);
})();
