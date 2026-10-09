/* Southern Lumber & Supply draft: mobile menu only. No tracking. */
(function () {
  var b = document.getElementById('menuBtn'), n = document.getElementById('mnav');
  if (b && n) b.addEventListener('click', function () {
    var o = n.classList.toggle('open');
    b.setAttribute('aria-expanded', o ? 'true' : 'false');
  });
})();
