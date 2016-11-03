'use strict';

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

function addPlaceInstance() {
  const name = $('label.name').children().val()
  const capacity = $('label.capacity').children().val()


  $.ajax({
    method: 'POST',
    url: '/place_instances/',
    data: JSON.stringify({
      name: name,
      capacity: capacity
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
  } else if (entity === 'place_instance') {
    $.ajax({
      method: 'DELETE',
      url: '/place_instances/' + identifier
    })
    .success(function (data, textStatus, xhr) {
      alert('Operation completed.')
      window.location.replace('/place_instances')
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
        window.location.replace('/post_comments/' + identifier)
    })
  }else if (entity === 'place_instance') {
      const name = $('label.name').children().val()
      const capacity = $('label.capacity').children().val()

      $.ajax({
        method: 'PUT',
        url: '/place_instances/' + identifier,
        data: JSON.stringify({
          name: name,
          capacity: capacity
        }),
        contentType: 'application/json'
      })
      .success(function (data, textStatus, xhr) {
        window.location.replace('/place_instances/' + identifier)
      })
  }
}

humanizeTimestamps(); setInterval(humanizeTimestamps, 10000);
