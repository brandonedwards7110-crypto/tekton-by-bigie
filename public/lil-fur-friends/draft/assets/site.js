(function () {
  var btn = document.getElementById('menuBtn'), mnav = document.getElementById('mnav');
  if (btn && mnav) {
    btn.addEventListener('click', function () {
      var open = mnav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    });
    mnav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { mnav.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; }
    });
  }
})();

(function () {
  var stage = document.getElementById('cf');
  if (!stage) return;
  var items = Array.prototype.slice.call(stage.querySelectorAll('.cf-item'));
  var dotsWrap = document.getElementById('cfDots');
  var n = items.length, active = 0, timer = null, interacted = false, visible = false;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var dots = items.map(function (el, i) {
    var b = document.createElement('button');
    b.type = 'button';
    b.setAttribute('aria-label', 'Show review ' + (i + 1));
    b.addEventListener('click', function () { go(i, true); });
    dotsWrap.appendChild(b);
    return b;
  });

  function cardW() {
    var w = stage.clientWidth;
    return Math.max(250, Math.min(400, w * (w < 500 ? 0.86 : 0.74)));
  }

  function layout() {
    var w = cardW();
    stage.style.setProperty('--cw', w + 'px');
    items.forEach(function (el, i) {
      var off = i - active;
      if (off > n / 2) off -= n;
      if (off < -n / 2) off += n;
      var a = Math.abs(off), s = off === 0 ? 0 : (off > 0 ? 1 : -1);
      var tx = 0, ry = 0, sc = 1, op = 1, z = 10;
      if (a === 0) { sc = 1.06; }
      else if (a === 1) { tx = s * w * 0.8; ry = -s * 42; sc = 0.86; op = 0.92; z = 9; }
      else if (a === 2) { tx = s * w * 1.3; ry = -s * 58; sc = 0.7; op = 0.55; z = 8; }
      else { tx = s * w * 1.6; ry = -s * 65; sc = 0.6; op = 0; z = 1; }
      el.style.transform = 'translate(-50%,-50%) translateX(' + tx + 'px) rotateY(' + ry + 'deg) scale(' + sc + ')';
      el.style.opacity = op;
      el.style.zIndex = z;
      el.style.pointerEvents = a > 2 ? 'none' : 'auto';
      el.classList.toggle('is-active', a === 0);
      el.setAttribute('aria-hidden', a === 0 ? 'false' : 'true');
    });
    dots.forEach(function (d, i) { d.classList.toggle('on', i === active); });
  }

  function go(i, user) {
    active = (i + n) % n;
    if (user) { interacted = true; stop(); }
    layout();
  }

  function stop() { if (timer) { clearInterval(timer); timer = null; } }
  function start() {
    if (reduce || interacted || timer || !visible) return;
    timer = setInterval(function () { go(active + 1, false); }, 5500);
  }

  items.forEach(function (el, i) {
    el.addEventListener('click', function () { if (i !== active) go(i, true); });
  });
  document.getElementById('cfPrev').addEventListener('click', function () { go(active - 1, true); });
  document.getElementById('cfNext').addEventListener('click', function () { go(active + 1, true); });
  stage.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') { e.preventDefault(); go(active - 1, true); }
    if (e.key === 'ArrowRight') { e.preventDefault(); go(active + 1, true); }
  });

  var startX = null;
  stage.addEventListener('pointerdown', function (e) { startX = e.clientX; });
  stage.addEventListener('pointerup', function (e) {
    if (startX === null) return;
    var dx = e.clientX - startX; startX = null;
    if (Math.abs(dx) > 40) go(active + (dx < 0 ? 1 : -1), true);
  });
  stage.addEventListener('pointercancel', function () { startX = null; });
  stage.addEventListener('mouseenter', stop);
  stage.addEventListener('mouseleave', function () { if (!interacted) start(); });

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      visible = entries[0].isIntersecting;
      visible ? start() : stop();
    }, { threshold: 0.35 }).observe(stage);
  } else { visible = true; start(); }

  window.addEventListener('resize', layout);
  layout();
})();
