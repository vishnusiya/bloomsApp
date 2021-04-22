(function (window) {
  SHP = {}
  SHP.purchase_date = ko.observable('');
  SHP.product_id = ko.observable('');
  SHP.product_name = ko.observable('');
  SHP.quantity = ko.observable('');
  SHP.purchase_price = ko.observable('');
  SHP.sales_price = ko.observable('');
  SHP.selected_product_id = ko.observable('');
  SHP.productList = ko.observableArray([]);


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


  SHP.purchaseCreate = function(data){
    var csrftoken = SHP.getCookie('csrftoken');
    var formdata = new FormData();
    formdata.append('purchase_date',SHP.purchase_date());
    formdata.append('product_id',SHP.product_id());
    formdata.append('quantity',SHP.quantity());
    formdata.append('purchase_price',SHP.purchase_price());
    formdata.append('sales_price',SHP.sales_price());
    $.ajax({
      method: 'POST',
      url: '/appshop/purchase/create/',
      data: formdata,
      contentType: false,
      processData: false,
      beforeSend: function(xhr, settings) {
        SHP.showLoading();
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    })
    .done( function (d, textStatus, jqXHR) {
      // SHP.showErrorModal(jQuery.parseJSON(jqXHR.responseText));
      // $('#errorModal').on('hidden.bs.modal', function (e) {
        alert(jQuery.parseJSON(jqXHR.responseText));
        location.href = '/purchase/list/'
      // });
    })
    .fail( function (jqXHR, textStatus, errorThrown) {
      alert(jQuery.parseJSON(jqXHR.responseText));
    })
    .always(function () {
        SHP.hideLoading();
      })
  }


  SHP.getProductList = function () {
    var csrftoken = SHP.getCookie('csrftoken');
    $.ajax({
      method: 'GET',
      url: '/appshop/get/all/products/list',
      dataType: 'json',
      beforeSend: function (xhr, settings) {
        SHP.showLoading();
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      })
      .done(function (d, textStatus, jqXHR) {
        SHP.productList([]);
        for (var i = 0; i < d.length; i++) {
          SHP.productList.push(d[i]);
        } 
        console.log(SHP.productList()) 
      })
      .fail(function (jqXHR, textStatus, errorThrown) {
        jsonValue = jQuery.parseJSON( jqXHR.responseText );
      })
      .always(function () {
        SHP.hideLoading();
      })
    }


})(this);

function init() {
if (document.readyState == "interactive") {
    SHP.hideLoading();
    SHP.getProductList();
    ko.applyBindings(SHP);
}
}
document.onreadystatechange = init;