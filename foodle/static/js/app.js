
const timestamps = _.map($('.timestamp'), function (element) {
  return element.innerHTML;
});

function humanizeTimestamps() {
  for (var i = 0; i < $('.timestamp').length; i++) {
    $('.timestamp')[i].innerHTML = moment(timestamps[i]).fromNow();
  }
}

function signup() {
  const username = $('label.username').children().val()
  const password = $('label.password').children().val()
  const passwordDuplicate = $('label.password-duplicate').children().val()

  if (password === passwordDuplicate) {
    $.ajax({
      method: 'POST',
      url: '/users/',
      data: JSON.stringify({
        username: username,
        password: password
      }),
      contentType: 'application/json'
    })
    .success(function (data, textStatus, xhr) {
      window.location.replace(xhr.getResponseHeader('location'))
    })
  } else {
    //  Set focus to the password field
    $('label.password').children().focus()
  }
}

function dispatchCreate(entity) {
  if (entity === 'post_image') {
    const link = $('label.link').children().val()

    $.ajax({
      method: 'POST',
      url: '/post_images/',
      data: JSON.stringify({
        link: link,
        post_id: 1
      }),
      contentType: 'application/json'
    })
    .success(function (data, textStatus, xhr) {
      window.location = xhr.getResponseHeader('location')
    })
  }

  return false;
}

function initializeDatabase() {
  $.ajax({
    method: 'POST',
    url: '/database_initialization/'
  })
  .success(function () {
    alert('Initialized database successfully.')
    window.location.reload()
  })
}

function addComment() {
  const body = $('label.body').children().val()

  $.ajax({
    method: 'POST',
    url: '/post_comments/',
    data: JSON.stringify({
      body: body
    }),
    contentType: 'application/json'
  })
  .success(function (data, textStatus, xhr) {
    window.location.replace(xhr.getResponseHeader('location'))
  })
}


function dispatchDelete(entity, identifier) {
  if (entity === 'user') {
    $.ajax({
      method: 'DELETE',
      url: '/users/' + identifier
    })
    .success(function (data, textStatus, xhr) {
      alert('Operation completed.')
      window.location.replace('/users')
    })
  } else if (entity === 'post_image') {
    $.ajax({
      method: 'DELETE',
      url: '/post_images/' + identifier
    })
    .success(function (data, textStatus, xhr) {
      alert('Operation completed.')
      window.location.replace('/post_images')
    })
  }
  else if (entity === 'post_comment') {
    $.ajax({
      method: 'DELETE',
      url: '/post_comments/' + identifier
    })
    .success(function (data, textStatus, xhr) {
      alert('Operation completed.')
      window.location.replace('/post_comments')
    })
  }
}

function dispatchUpdate(entity, identifier) {
  if (entity === 'user') {
    const username = $('label.username').children().val()
    const password = $('label.password').children().val()
    const passwordDuplicate = $('label.password-duplicate').children().val()

    if (password === passwordDuplicate) {
      $.ajax({
        method: 'PUT',
        url: '/users/' + identifier,
        data: JSON.stringify({
          username: username,
          password: password
        }),
        contentType: 'application/json'
      })
      .success(function (data, textStatus, xhr) {
        window.location.replace(xhr.getResponseHeader('location'))
      })
      .fail(function (data, textStatus, xhr) {
        alert('Username and password, both needs to be typed and be 7 to 20 characters long.')
      })
    } else {
      //  Set focus to the password field
      $('label.password').children().focus()
    }
  } else if (entity === 'post_image') {
    const link = $('label.link').children().val()

    $.ajax({
      method: 'PUT',
      url: '/post_images/' + identifier,
      data: JSON.stringify({
        link: link
      }),
      contentType: 'application/json'
    })
    .success(function (data, textStatus, xhr) {
      window.location = xhr.getResponseHeader('location')
    })
  } else if (entity === 'post_comment') {
    const body = $('label.body').children().val()

    $.ajax({
      method: 'PUT',
      url: '/post_comments/' + identifier,
      data: JSON.stringify({
        body: body
      }),
      contentType: 'application/json'
    })
    .success(function (data, textStatus, xhr) {
      window.location = xhr.getResponseHeader('location')
    });
  }

  return false;
}

var semaphore = 0;

$('#search').on('keydown', function (keyEvent) {
  setTimeout(function () {
    const result = $('#search').val();

    if (result !== '') {
      semaphore += 1;

      $.ajax({
        method: 'GET',
        url: '/search?parameter=' + result
      })
      .success(function (data, textStatus, xhr) {
        semaphore -= 1;

        if (!semaphore) {
          for (var i = 0; i < 5; ++i) {
            $('.cell-' + i).css('border-radius', '0');
            $('.cell-' + i).css('visibility', 'hidden');
          }

          $('#search').css('color', 'black');

          $('.top-bar-extend').css('visibility', 'visible');

          var dataCount = 0;

          $('.cell-0').css('border-radius', '10px 10px 0 0');

          for (var i = 0; i < data[0].length; ++i, ++dataCount) {
            $('.cell-' + dataCount).css('visibility', 'visible');
            $('.cell-' + dataCount + ' p.display-name')[0].innerHTML = data[0][i][2];
            $('.cell-' + dataCount + ' span.username')[0].innerHTML = '@' + data[0][i][1];
            $('.cell-' + dataCount + ' span.username').css('color', 'rgb(170, 170, 170)');
            $('.cell-' + dataCount + ' a').attr('href', '/users/' + data[0][i][0]);
            $('.cell-' + dataCount + ' .profile-image-search').css('background-image', 'url(' + data[0][i][3] + ')');
          }

          for (var i = 0; i < data[1].length; ++i, ++dataCount) {
            $('.cell-' + dataCount).css('visibility', 'visible');
            $('.cell-' + dataCount + ' p.display-name')[0].innerHTML = data[1][i][0];
            $('.cell-' + dataCount + ' span.username')[0].innerHTML = data[1][i][1];
            $('.cell-' + dataCount + ' a').attr('href', '/places/1');
            $('.cell-' + dataCount + ' .profile-image-search').css('background-image', 'url(' + data[1][i][2] + ')');
          }

          if (dataCount === 1) {
            $('.cell-0').css('border-radius', '10px');
          } else if (dataCount === 0) {
            $('#search').css('color', 'red');
          } else {
            $('.cell-' + (dataCount - 1)).css('border-radius', '0 0 10px 10px');
          }
        }
      });
    } else {
      $('.top-bar-extend').css('visibility', 'hidden');
      $('.top-bar-extend-cell').css('visibility', 'hidden');
    }
  }, 5);
});

humanizeTimestamps(); setInterval(humanizeTimestamps, 10000);
$('#search').removeAttr('disabled');
