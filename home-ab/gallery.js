/* ============================================================
   Sofon — GALLERY builder.
   Одна розмітка на всі варіанти: сторінка дає лише перелік
   зображень, варіант перемикається класом.

   SofonGal.render(rootEl, items, variant)
     items — [{src, title, sub, fit}]  fit: 'contain' | 'cover'
     variant — mosaic | pop | strip | bay | sheet
   ============================================================ */
window.SofonGal = (function () {
  var VARIANTS = {
    mosaic: 'gal--tiles gal--mosaic galh--dim',
    pop:    'gal--tiles gal--mosaic galh--pop',
    strip:  'gal--tiles4 gal--strip',
    bay:    'gal--bay',
    sheet:  'gal--sheet galh--dim'
  };
  var BAY_PER_ROW = 5;

  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
  }
  function n2(i) { return String(i + 1).padStart(2, '0'); }

  /* Поштучні поправки: bright — для рендерів, де підкладка не чисто біла
     (без неї multiply лишає сірий прямокутник); zoom — коли деталь на рендері
     дрібна й губиться у плитці. */
  function styleOf(it) {
    var v = '';
    if (it.bright) v += '--bri:' + it.bright + ';';
    if (it.zoom) v += '--z:' + it.zoom + ';--zh:' + (it.zoom * 1.08).toFixed(3) + ';';
    return v ? ' style="' + v + '"' : '';
  }

  function tile(it, i) {
    var fit = it.fit || 'cover';
    return '<figure class="gal-i" data-fit="' + fit + '"' + styleOf(it) + '>' +
      '<img src="' + esc(it.src) + '" alt="' + esc(it.title) + '" loading="lazy">' +
      '<span class="gal-veil"></span>' +
      '<span class="gal-n">' + n2(i) + '</span>' +
      '<figcaption class="gal-cap"><b>' + esc(it.title) + '</b>' +
        (it.sub ? '<i>' + esc(it.sub) + '</i>' : '') + '</figcaption>' +
    '</figure>';
  }

  /* ============================================================
     STRIP — горизонтальна смуга, якою керує курсор.
     Правила руху:
       · положення курсора по горизонталі → положення полотна, з
         уповільненням біля країв (smoothstep), тож у впор не б'є;
       · полотно доганяє курсор за ~0.3 с, а не стрибає за ним;
       · курсор пішов зі смуги — лишається де було, назад не відмотує;
       · курсор зупинився — рух завмирає і аж тоді вмикається наведення
         на плитку: підпис і затемнення решти.
     ============================================================ */
  var REST_MS = 260;      // скільки курсор має простояти, щоб це рахувалось зупинкою
  var REST_PX = 3;        // менші зсуви вважаємо тремтінням руки, а не рухом
  var EASE = 0.12;        // частка шляху за кадр — це і є ті ~0.3 с

  function initStrip(win, inner) {
    var live = window.matchMedia('(min-width:901px) and (hover:hover)');
    var calm = window.matchMedia('(prefers-reduced-motion:reduce)');
    var max = 0, target = 0, cur = 0, start = 0, raf = null, G = null;
    var restT = null, hotEl = null, lastX = 0, lastY = 0;

    /* Геометрія: повністю видно смугу завширшки з текстову колонку, обабіч —
       по --gal-fade гасіння, далі нічого. Полотно їздить рівно між зовнішніми
       межами гасіння, тож хід не залежить від ширини екрана — на широкому
       моніторі прокрутка не стає чутливішою. */
    function geom() {
      var box = win.parentElement, w = win.clientWidth, content = w;
      if (box) {
        var cs = getComputedStyle(box);
        content = box.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
      }
      var fade = parseFloat(getComputedStyle(win).getPropertyValue('--gal-fade')) || 200;
      return { w: w, content: content, fade: fade,
               inn: Math.max(0, (w - content) / 2) };  // від краю екрана до колонки тексту
    }
    function measure() {
      var g = geom();
      G = g;
      /* Полотно ходить так, щоб на початку його лівий край, а в кінці правий
         стояли рівно на межі чистої зони. Тільки за такої умови до першої й
         останньої плитки взагалі можна дістатись — інакше вони назавжди
         лишаються в гасінні. */
      start = g.inn;
      max = Math.max(0, inner.scrollWidth - g.content);
    }
    function smooth(t) { return t * t * (3 - 2 * t); }   // уповільнення на обох краях

    function paint() {
      inner.style.transform = 'translate3d(' + (start - cur).toFixed(2) + 'px,0,0)';
      /* Гасіння живе тільки з того боку, де за межею чистої зони справді щось
         є. Доїхали до кінця — край стає різким, і остання плитка читається
         повністю. Ширина смуги гасіння наростає разом зі зсувом, максимум --gal-fade. */
      var f = G ? G.fade : 200, inn = G ? G.inn : 0;
      var l = Math.min(f, cur), r = Math.min(f, max - cur);
      win.style.setProperty('--gal-in-l', inn + 'px');
      win.style.setProperty('--gal-out-l', (inn - l) + 'px');
      win.style.setProperty('--gal-in-r', inn + 'px');
      win.style.setProperty('--gal-out-r', (inn - r) + 'px');
    }
    function tick() {
      cur += (target - cur) * EASE;
      if (Math.abs(target - cur) < 0.2) cur = target;
      paint();
      raf = cur === target ? null : requestAnimationFrame(tick);
    }
    function run() { if (calm.matches) { cur = target; paint(); return; }
                     if (!raf) raf = requestAnimationFrame(tick); }

    function clearHot() {
      if (hotEl) { hotEl.classList.remove('is-hot'); hotEl = null; }
      inner.classList.remove('has-hot');
    }
    function armRest(x, y) {
      clearTimeout(restT);
      restT = setTimeout(function settle() {
        // поки полотно ще їде, зупинкою це не рахуємо — інакше підпис
        // спалахне на плитці, яка за мить поїде далі
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
      var t = (e.clientX - r.left - g.inn) / g.content;
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
    });
    // зображення довантажуються після рендера й міняють ширину полотна
    window.addEventListener('load', function () { measure(); paint(); });
    measure(); paint();

    // службове: ?sx=0..1 ставить полотно у задане положення для знімка
    var sx = parseFloat(new URLSearchParams(location.search).get('sx'));
    if (!isNaN(sx)) { target = cur = smooth(Math.max(0, Math.min(1, sx))) * max; paint(); }
  }

  function renderStrip(root, items) {
    root.className = 'gal-strip';
    var inner = document.createElement('div');
    inner.className = 'gal ' + VARIANTS.strip;
    inner.innerHTML = items.map(function (it, i) { return tile(it, i); }).join('');
    root.innerHTML = '';
    root.appendChild(inner);
    hot(inner);
    initStrip(root, inner);
  }

  function render(root, items, variant) {
    variant = VARIANTS[variant] ? variant : 'mosaic';
    root.className = 'gal ' + VARIANTS[variant];

    if (variant === 'strip') { renderStrip(root, items); return; }

    if (variant === 'bay') {
      var out = '', row = '';
      items.forEach(function (it, i) {
        row += tile(it, i);
        if ((i + 1) % BAY_PER_ROW === 0 || i === items.length - 1) {
          out += '<div class="gal-row">' + row + '</div>'; row = '';
        }
      });
      root.innerHTML = out;
      hot(root);
      return;
    }

    root.innerHTML = items.map(function (it, i) { return tile(it, i); }).join('');
    hot(root);
  }

  /* Службове: ?hi=N імітує наведення на N-ту плитку.
     Потрібне тільки для headless-знімків — :hover у них не відтворюється,
     а без цього неможливо подивитись на саму динаміку. */
  function hot(root) {
    var n = parseInt(new URLSearchParams(location.search).get('hi'), 10);
    if (isNaN(n) || n < 1) return;
    var el = root.querySelectorAll('.gal-i')[n - 1];
    if (!el) return;
    el.classList.add('is-hot');
    root.classList.add('has-hot');
  }

  return { render: render, variants: Object.keys(VARIANTS) };
})();
