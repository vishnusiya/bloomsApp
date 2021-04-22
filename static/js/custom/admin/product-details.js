(function (window) {
  SHP = {}
  SHP.product_id = ko.observable('');
  SHP.product_name = ko.observable('');
  SHP.category_name = ko.observable('');
  SHP.s_price = ko.observable('');
  SHP.stock_status = ko.observable('');
  SHP.stock = ko.observable('');
  SHP.quantity = ko.observable('');


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

  

  SHP.getProductDetails = function () {
    var csrftoken = SHP.getCookie('csrftoken');
    $.ajax({
      method: 'GET',
      url: '/appshop/product/details/get',
      data: {'product_id':SHP.product_id()},
      dataType: 'json',
      beforeSend: function (xhr, settings) {
        SHP.showLoading();
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      })
      .done(function (d, textStatus, jqXHR) {
        SHP.product_name(d.product_name)
        // SHP.p_price(d.p_price)
        SHP.s_price(d.s_price)
        SHP.category_name(d.category_name)
        SHP.quantity(d.quantity)
        // SHP.minimum_status(d.minimum_status)
        $("#StockStatus").val(d.stock_status).trigger("change")
      })
      .fail(function (jqXHR, textStatus, errorThrown) {
        jsonValue = jQuery.parseJSON( jqXHR.responseText );
      })
      .always(function () {
        SHP.hideLoading();
      })
    }


    $(".edit-btn").on("click", function () {
      $(".save-btn").removeClass("d-none")
      $(".edit-btn").addClass("d-none")
      $("#product_name").prop("disabled", false)
      $("#p_price").prop("disabled", false)
      $("#s_price").prop("disabled", false)
      $("#StockStatus").prop("disabled", false)
      $("#quantity").prop("disabled", false)
      $("#minimum_status").prop("disabled", false)
    })


  SHP.productUpdate = function () {
   var csrftoken = SHP.getCookie('csrftoken');
    var formdata = new FormData();
    formdata.append('product_id',SHP.product_id());
    formdata.append('product_name',SHP.product_name());
    formdata.append('s_price',SHP.s_price());
    formdata.append('stock_status',SHP.stock_status());
    formdata.append('quantity',SHP.quantity());
    $.ajax({
      method: 'POST',
      url: '/appshop/product/update/',
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
      location.reload();
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
    var docUrlArr = document.URL.split('/');
    var product_id = docUrlArr[docUrlArr.length - 1];
    SHP.product_id(product_id)
    SHP.getProductDetails();
    ko.applyBindings(SHP);
}
}
document.onreadystatechange = init;