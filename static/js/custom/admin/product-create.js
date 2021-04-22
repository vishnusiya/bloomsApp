(function (window) {
  SHP = {}
  SHP.category_name = ko.observable('');
  SHP.product_name = ko.observable('');
  SHP.s_price = ko.observable('');
  SHP.stock_status = ko.observable('');
  SHP.quantity = ko.observable('');
  SHP.minimum_status = ko.observable('');


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


  SHP.productCreate = function(data){
    var csrftoken = SHP.getCookie('csrftoken');
    var formdata = new FormData();
    formdata.append('category_name',SHP.category_name());
    formdata.append('product_name',SHP.product_name());
    formdata.append('s_price',SHP.s_price());
    formdata.append('stock_status',SHP.stock_status());
    formdata.append('quantity',SHP.quantity());
    // formdata.append('p_price',SHP.p_price());
    // formdata.append('minimum_status',SHP.minimum_status());
    $.ajax({
      method: 'POST',
      url: '/appshop/product/create/',
      data: formdata,
      contentType: false,
      processData: false,
      beforeSend: function(xhr, settings) {
        SHP.showLoading();
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    })
    .done( function (d, textStatus, jqXHR) {
      alert(d);
      location.href = '/home/'
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