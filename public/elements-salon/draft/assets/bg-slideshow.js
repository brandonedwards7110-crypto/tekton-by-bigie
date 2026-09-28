// Reusable full-page background slideshow. Call once per page:
//   initBgSlideshow('bgSlideshow', [
//     'assets/landscape-photo.jpg',                          // shows solo, full width
//     ['assets/portrait-a.jpg', 'assets/portrait-b.jpg'],     // shows as a pair, side by side
//     ...
//   ], 4);
// Third argument is seconds each slide shows before crossfading to the next.
//
// Most of these source photos are vertical phone photos. Stretching one to
// cover a wide screen crops out most of the photo, so portrait photos get
// paired two-up instead -- two portraits side by side match a wide screen's
// shape far better than one ever could. A genuinely landscape photo (the
// storefront shot, the team photo) already matches a wide screen and looks
// worse cut in half, so those stay solo -- pass them as a plain string, not
// an array, to keep them full width. Check real pixel dimensions before
// deciding which a new photo needs; don't guess from how it looks small.
function initBgSlideshow(containerId, slides, slideSeconds) {
  slideSeconds = slideSeconds || 4;
  var container = document.getElementById(containerId);
  if (!container || !slides || !slides.length) return;

  var reduceMotion = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var total = slides.length * slideSeconds;
  var fadeSeconds = Math.min(1, slideSeconds * 0.25);
  var fadePct = (fadeSeconds / total * 100).toFixed(2);
  var holdEndPct = (slideSeconds / total * 100 - fadePct).toFixed(2);
  var slidePct = (slideSeconds / total * 100).toFixed(2);

  var styleEl = document.createElement('style');
  styleEl.textContent =
    '#' + containerId + ' .bg-slide { animation: bgFade-' + containerId + ' ' + total + 's infinite; }' +
    '@keyframes bgFade-' + containerId + ' {' +
    '0% { opacity: 0; }' +
    fadePct + '% { opacity: 1; }' +
    holdEndPct + '% { opacity: 1; }' +
    slidePct + '% { opacity: 0; }' +
    '100% { opacity: 0; }' +
    '}';
  document.head.appendChild(styleEl);

  slides.forEach(function (entry, i) {
    var photos = Array.isArray(entry) ? entry : [entry];
    var slide = document.createElement('div');
    slide.className = 'bg-slide';
    photos.forEach(function (src) {
      var half = document.createElement('div');
      half.className = 'bg-slide-half';
      half.style.backgroundImage = "url('" + src + "')";
      slide.appendChild(half);
    });
    if (reduceMotion) {
      slide.style.animation = 'none';
      slide.style.opacity = i === 0 ? '1' : '0';
    } else {
      slide.style.animationDelay = (i * slideSeconds) + 's';
    }
    container.appendChild(slide);
  });
}
