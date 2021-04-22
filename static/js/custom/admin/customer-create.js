(function (window) {
  SHP = {}
  SHP.customer_name = ko.observable('');
  SHP.recieved_amount = ko.observable('');
  SHP.pending_amount = ko.observable('');
  SHP.phone_no = ko.observable('');


  SHP.getCookie = function (name) {
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


  SHP.showLoading = function(){
      $(".loader-bg").removeClass('d-none');
      $(".no-data").removeClass('active');
  }

  SHP.hideLoading = function(){
    $(".loader-bg").addClass('d-none');
    $(".no-data").addClass('active');
  }

  SHP.showErrorModal = function(msg){
      $("#errorModal").modal('show');
      $("#errorMessage").text(msg);
    }


  SHP.customerCreate = function(data){
    var csrftoken = SHP.getCookie('csrftoken');
    var formdata = new FormData();
    formdata.append('customer_name',SHP.customer_name());
    // formdata.append('recieved_amount',SHP.recieved_amount());
    // formdata.append('pending_amount',SHP.pending_amount());
    formdata.append('phone_no',SHP.phone_no());
    $.ajax({
      method: 'POST',
      url: '/appshop/customer/create/',
      data: formdata,
      contentType: false,
      processData: false,
      beforeSend: function(xhr, settings) {
        SHP.showLoading();
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    })
    .done( function (d, textStatus, jqXHR) {
      alert(jQuery.parseJSON(jqXHR.responseText));
      // SHP.showErrorModal(jQuery.parseJSON(jqXHR.responseText));
      // $('#errorModal').on('hidden.bs.modal', function (e) {
        location.href = '/customer/list/'
      // });
    })
    .fail( function (jqXHR, textStatus, errorThrown) {
      alert(jQuery.parseJSON(jqXHR.responseText));
    })
    .always(function () {
        SHP.hideLoading();
      })
  }


})(this);

function init() {
if (document.readyState == "interactive") {
    SHP.hideLoading();
    ko.applyBindings(SHP);
}
}
document.onreadystatechange = init;