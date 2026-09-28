// Fake/mockup Google-Calendar-style week view. NOT live data -- shows what
// the real embed will look like once each stylist's real Google Calendar is
// connected. Call renderCalMockup(containerId, [initials...], events) --
// pass all 10 initials for the combined "master" view, or just one for a
// single stylist's own page.
var CAL_STYLIST_COLORS = {
  'RT': '#c23a63', 'AT': '#cdaa6d', 'BM': '#4f9d95', 'BH': '#6b7fd7',
  'KC': '#9b6bd7', 'KG': '#e0873f', 'KM': '#d65fa0', 'LP': '#6fae5a',
  'MD': '#d3573f', 'TW': '#4fa8c9'
};
var CAL_STYLIST_NAMES = {
  'RT': 'Robert', 'AT': 'Ayden', 'BM': 'Bailey', 'BH': 'Bree',
  'KC': 'Kayla C.', 'KG': 'Kayla G.', 'KM': 'Kyndall', 'LP': 'Lily',
  'MD': 'Merri', 'TW': 'Talynn'
};
var CAL_DAYS = ['Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
var CAL_START_HOUR = 10;
var CAL_END_HOUR = 18; // salon hours: 10am-6pm

function renderCalMockup(containerId, initials, events) {
  var container = document.getElementById(containerId);
  if (!container) return;
  var totalHours = CAL_END_HOUR - CAL_START_HOUR;

  var head = '<div class="cal-mock-head"><div></div>';
  CAL_DAYS.forEach(function (d) { head += '<div>' + d + '</div>'; });
  head += '</div>';

  var times = '<div class="cal-mock-times">';
  for (var h = CAL_START_HOUR; h < CAL_END_HOUR; h++) {
    var label = h > 12 ? (h - 12) + ' PM' : (h === 12 ? '12 PM' : h + ' AM');
    times += '<div>' + label + '</div>';
  }
  times += '</div>';

  var grid = '<div class="cal-mock-grid">';
  CAL_DAYS.forEach(function (day, dayIndex) {
    var dayEvents = events.filter(function (e) { return e.day === dayIndex; });
    grid += '<div class="cal-mock-day-col"><div class="cal-mock-lanes">';
    initials.forEach(function (initial) {
      grid += '<div class="cal-mock-lane-col">';
      dayEvents.filter(function (e) { return e.who === initial; }).forEach(function (e) {
        var top = (e.start - CAL_START_HOUR) / totalHours * 100;
        var height = (e.end - e.start) / totalHours * 100;
        grid += '<div class="cal-mock-block" style="top:' + top + '%; height:' + height +
          '%; background:' + CAL_STYLIST_COLORS[initial] + ';">' + initial + '</div>';
      });
      grid += '</div>';
    });
    grid += '</div></div>';
  });
  grid += '</div>';

  var legend = '<div class="cal-mock-legend">';
  initials.forEach(function (i) {
    legend += '<div class="cal-mock-legend-item"><span class="cal-mock-swatch" style="background:' +
      CAL_STYLIST_COLORS[i] + ';"></span>' + CAL_STYLIST_NAMES[i] + '</div>';
  });
  legend += '</div>';

  container.innerHTML = '<div class="cal-mock"><div class="cal-mock-body">' + times + grid +
    '</div></div>' + legend;

  // head goes above body but inside the same scroll container as body's grid
  container.querySelector('.cal-mock').insertAdjacentHTML('afterbegin', head);
}
