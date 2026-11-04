(function () {
  'use strict';

  // menu mobile
  var burger = document.querySelector('.burger');
  var nav = document.getElementById('site-nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.textContent = open ? '✕' : '☰';
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { nav.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); burger.textContent = '☰'; }
    });
  }

  // filtros da galeria
  var filters = document.querySelectorAll('[data-filter]');
  if (filters.length) {
    filters.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var cat = btn.getAttribute('data-filter');
        filters.forEach(function (b) { b.classList.toggle('on', b === btn); b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
        document.querySelectorAll('.gal figure').forEach(function (f) {
          f.hidden = !(cat === 'all' || f.getAttribute('data-cat') === cat);
        });
      });
    });
  }

  // formulários de orçamento
  var forms = document.querySelectorAll('form[data-lead]');
  var params = new URLSearchParams(window.location.search);
  forms.forEach(function (form) {
    var pageField = form.querySelector('[name="page"]');
    if (pageField) pageField.value = window.location.pathname;
    ['utm_source', 'utm_medium', 'utm_campaign', 'gclid', 'fbclid'].forEach(function (k) {
      var f = form.querySelector('[name="' + k + '"]');
      if (f && params.get(k)) f.value = params.get(k);
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = form.querySelector('.fmsg');
      var btn = form.querySelector('button[type="submit"]');
      msg.textContent = ''; msg.className = 'fmsg';
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = v; });
      btn.disabled = true; var label = btn.textContent; btn.textContent = 'Sending...';
      fetch(form.getAttribute('action') || '/api/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }).then(function (r) {
        if (!r.ok) throw new Error('http ' + r.status);
        window.location.href = '/thank-you/';
      }).catch(function () {
        msg.className = 'fmsg err';
        msg.innerHTML = 'We could not send your request right now. Please text or call us at <a href="tel:+19788096279">978-809-6279</a> or email <a href="mailto:deck@newenglandcarpenters.com">deck@newenglandcarpenters.com</a>.';
        btn.disabled = false; btn.textContent = label;
      });
    });
  });
})();

/* testimonials carousel: arrows, a new card every 3s in a loop, "More" opens the full review */
(function () {
  var box = document.querySelector('[data-rv]');
  if (!box) return;
  var wrap = box.querySelector('.rv-wrap'), track = box.querySelector('.rv-track');
  var slides = [].slice.call(track.children), n = slides.length, K = 3;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* "More" buttons only where the text is actually cut */
  function checkMore() {
    box.querySelectorAll('.rv').forEach(function (f) {
      var p = f.querySelector('.clamp'), m = f.querySelector('.more');
      m.hidden = !(p.scrollHeight > p.clientHeight + 1);
    });
  }
  var dlg = document.createElement('dialog');
  dlg.className = 'rv-modal';
  dlg.setAttribute('aria-label', 'Full review');
  document.body.appendChild(dlg);
  dlg.addEventListener('click', function (ev) { if (ev.target === dlg) dlg.close(); });
  box.addEventListener('click', function (ev) {
    var m = ev.target.closest('.more');
    if (!m) return;
    var f = m.closest('.rv'), av = f.querySelector('.av');
    dlg.innerHTML = '<button type="button" class="x" aria-label="Close">\u00d7</button>'
      + f.querySelector('.g').outerHTML
      + '<div class="who"><div class="av" style="' + av.getAttribute('style') + '">' + av.textContent + '</div><div><b>'
      + f.querySelector('b').textContent + '</b><div class="src">Google review</div></div></div>'
      + '<div class="st" aria-label="5 stars">\u2605\u2605\u2605\u2605\u2605</div><div class="body">' + f.querySelector('.full').innerHTML + '</div>';
    dlg.querySelector('.x').addEventListener('click', function () { dlg.close(); });
    dlg.showModal();
  });
  checkMore();
  window.addEventListener('resize', checkMore);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(checkMore);

  if (reduce) {
    [].forEach.call(box.querySelectorAll('.rv-arrow'), function (a) {
      a.addEventListener('click', function () {
        wrap.scrollBy({ left: (a.classList.contains('next') ? 1 : -1) * slides[0].offsetWidth });
      });
    });
    return;
  }

  /* clones on both ends make the loop seamless */
  slides.slice(-K).forEach(function (s) { var c = s.cloneNode(true); c.setAttribute('aria-hidden', 'true'); track.insertBefore(c, track.firstChild); });
  slides.slice(0, K).forEach(function (s) { var c = s.cloneNode(true); c.setAttribute('aria-hidden', 'true'); track.appendChild(c); });
  box.classList.add('on');
  checkMore();
  var p = 0, busy = false, paused = false, timer;
  function move(animate) {
    track.style.transition = animate ? '' : 'none';
    track.style.transform = 'translateX(-' + ((p + K) * slides[0].offsetWidth) + 'px)';
  }
  function step(d) {
    if (busy) return;
    busy = true; p += d; move(true);
    setTimeout(function () {
      busy = false;
      if (p >= n) { p -= n; move(false); } else if (p < 0) { p += n; move(false); }
    }, 950);
  }
  function restart() { clearInterval(timer); timer = setInterval(function () { if (!paused && !document.hidden) step(1); }, 3000); }
  box.querySelector('.prev').addEventListener('click', function () { step(-1); restart(); });
  box.querySelector('.next').addEventListener('click', function () { step(1); restart(); });
  box.addEventListener('mouseenter', function () { paused = true; });
  box.addEventListener('mouseleave', function () { paused = false; });
  box.addEventListener('focusin', function () { paused = true; });
  box.addEventListener('focusout', function () { paused = false; });
  box.addEventListener('click', function (ev) { if (ev.target.closest('.more')) paused = true; });
  dlg.addEventListener('close', function () { paused = false; });
  window.addEventListener('resize', function () { move(false); });
  move(false);
  restart();
})();

/* falling snow over the home hero (skipped for "reduce motion") */
(function () {
  var hero = document.querySelector('.hero:not(.sm)');
  if (!hero || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var cv = document.createElement('canvas');
  cv.className = 'snow';
  cv.setAttribute('aria-hidden', 'true');
  hero.appendChild(cv);
  var ctx = cv.getContext('2d'), W = 0, H = 0, dpr = 1, flakes = [], t = 0, raf = 0, visible = true;
  function make(first) {
    var r = 0.8 + Math.random() * Math.random() * 3.2;
    return { x: Math.random() * W, y: first ? Math.random() * H : -r * 2, r: r,
             vy: 18 + r * 14 + Math.random() * 10, ph: Math.random() * 6.28, sw: 8 + Math.random() * 18,
             a: 0.45 + Math.min(r / 4, 0.5) };
  }
  function size() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = hero.clientWidth; H = hero.clientHeight;
    cv.width = W * dpr; cv.height = H * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var want = Math.min(Math.round(W * H / 7000), 170);
    while (flakes.length < want) flakes.push(make(true));
    flakes.length = want;
  }
  var last = 0;
  function frame(ts) {
    raf = 0;
    if (!visible || document.hidden) { last = 0; return; }
    var dt = last ? Math.min((ts - last) / 1000, 0.05) : 0.016;
    last = ts; t += dt;
    ctx.clearRect(0, 0, W, H);
    for (var i = 0; i < flakes.length; i++) {
      var f = flakes[i];
      f.y += f.vy * dt;
      var x = f.x + Math.sin(t * 0.8 + f.ph) * f.sw;
      if (f.y > H + f.r * 2) { flakes[i] = make(false); continue; }
      ctx.globalAlpha = f.a;
      ctx.fillStyle = '#fff';
      ctx.beginPath(); ctx.arc(x, f.y, f.r, 0, 6.2832); ctx.fill();
    }
    raf = requestAnimationFrame(frame);
  }
  function run() { if (!raf && visible && !document.hidden) raf = requestAnimationFrame(frame); }
  size();
  window.addEventListener('resize', size);
  document.addEventListener('visibilitychange', run);
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (en) { visible = en[0].isIntersecting; run(); }).observe(hero);
  }
  run();
})();
