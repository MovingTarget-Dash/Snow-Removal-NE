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
