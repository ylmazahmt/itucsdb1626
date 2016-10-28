'use strict';

const timestamps = _.map($('.timestamp'), function (element) {
  return element.innerHTML;
});

function humanizeTimestamps() {
  for (var i = 0; i < $('.timestamp').length; i++) {
    $('.timestamp')[i].innerHTML = moment(timestamps[i]).fromNow();
  }
}

humanizeTimestamps(); setInterval(humanizeTimestamps, 10000);
