// Closes any open <details class="nav-menu"> (and its nested submenu) when
// you click outside it. The open/close itself is native <details> behavior --
// this just adds the "click elsewhere to close" polish on top.
document.addEventListener('click', function (e) {
  document.querySelectorAll('.nav-menu[open]').forEach(function (menu) {
    if (!menu.contains(e.target)) {
      menu.removeAttribute('open');
      menu.querySelectorAll('.nav-submenu[open]').forEach(function (sub) {
        sub.removeAttribute('open');
      });
    }
  });
});
