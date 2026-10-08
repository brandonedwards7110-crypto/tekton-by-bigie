/* South Walton Academy draft: mobile menu + reading settings. No autoplay, no tracking. */
(function () {
  var root = document.documentElement;
  var KEY = 'swa-reading-settings';
  var S = { size: '1', contrast: 'normal', calm: 'off', spacing: 'normal' };

  function load() {
    try { var v = JSON.parse(localStorage.getItem(KEY) || 'null'); if (v) for (var k in S) if (v[k]) S[k] = v[k]; } catch (e) {}
  }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} }
  function apply() {
    root.setAttribute('data-size', S.size);
    if (S.contrast === 'high') root.setAttribute('data-contrast', 'high'); else root.removeAttribute('data-contrast');
    if (S.calm === 'on') root.setAttribute('data-calm', 'on'); else root.removeAttribute('data-calm');
    if (S.spacing === 'roomy') root.setAttribute('data-spacing', 'roomy'); else root.removeAttribute('data-spacing');
    var map = {
      'size-1': S.size === '1', 'size-2': S.size === '2', 'size-3': S.size === '3',
      'contrast': S.contrast === 'high', 'calm': S.calm === 'on', 'spacing': S.spacing === 'roomy'
    };
    for (var id in map) { var b = document.querySelector('[data-rs="' + id + '"]'); if (b) b.setAttribute('aria-pressed', map[id] ? 'true' : 'false'); }
  }
  load(); apply();

  var panel = document.getElementById('rs');
  var btn = document.getElementById('rsBtn');
  function setPanel(open) {
    if (!panel || !btn) return;
    panel.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) { var f = panel.querySelector('button'); if (f) f.focus(); }
  }
  if (btn && panel) {
    btn.addEventListener('click', function () { setPanel(!panel.classList.contains('open')); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && panel.classList.contains('open')) { setPanel(false); btn.focus(); } });
    panel.addEventListener('click', function (e) {
      var t = e.target.closest('[data-rs]'); if (!t) return;
      var id = t.getAttribute('data-rs');
      if (id.indexOf('size-') === 0) S.size = id.slice(5);
      else if (id === 'contrast') S.contrast = S.contrast === 'high' ? 'normal' : 'high';
      else if (id === 'calm') S.calm = S.calm === 'on' ? 'off' : 'on';
      else if (id === 'spacing') S.spacing = S.spacing === 'roomy' ? 'normal' : 'roomy';
      else if (id === 'reset') S = { size: '1', contrast: 'normal', calm: 'off', spacing: 'normal' };
      save(); apply();
    });
  }

  var mb = document.getElementById('menuBtn'), mn = document.getElementById('mnav');
  if (mb && mn) {
    mb.addEventListener('click', function () {
      var open = mn.classList.toggle('open');
      mb.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
})();
