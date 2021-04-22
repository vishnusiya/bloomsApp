(function (window) {
  SHP = {}
  SHP.username = ko.observable('');
  SHP.password = ko.observable('');


  SHP.getCookie = function(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    };


  SHP.userLogin = function () {
    var csrftoken = SHP.getCookie('csrftoken');
    var formdata = new FormData();
    formdata.append('username', SHP.username());
    formdata.append('password', SHP.password());
    $.ajax({
      method: 'POST',
      url: '/appshop/user/login/',
      data: formdata,
      contentType: false,
      processData: false,
      beforeSend: function (xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    })
      .done(function (d, textStatus, jqXHR) {
        location.href = '/home/'
      })
      .fail(function (jqXHR, textStatus, errorThrown) {
        jsonValue = jQuery.parseJSON( jqXHR.responseText );
        alert(jsonValue)
      })
    }


})(this);

function init() {
if (document.readyState == "interactive") {
    ko.applyBindings(SHP);
}
}
document.onreadystatechange = init;