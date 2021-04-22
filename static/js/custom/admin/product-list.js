(function (window) {
  SHP = {}
  SHP.search_term = ko.observable('');
  SHP.productList = ko.observableArray([]);
  SHP.pages_list = ko.observableArray([]);
  SHP.date_sort_order = ko.observable('ascending');
  SHP.no_of_date_sort = ko.observable('false');
  SHP.current_page = ko.observable(1);
  SHP.page_count = ko.observable();
  SHP.category_id = ko.observable();


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


  SHP.productDetails = function(data){
    location.href="/product/details/" +data.product_id
  }

  SHP.deleteProduct = function(data){
    var csrftoken = SHP.getCookie('csrftoken');
    var formdata = new FormData();
    formdata.append('product_id',data.product_id);
    $.ajax({
      method: 'POST',
      url: '/appshop/product/delete/',
      data: formdata,
      contentType: false,
      processData: false,
      beforeSend: function(xhr, settings) {
        SHP.showLoading();
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    })
    .done( function (d, textStatus, jqXHR) {
      location.reload();
    })
    .fail( function (jqXHR, textStatus, errorThrown) {
      alert(jQuery.parseJSON(jqXHR.responseText));
    })
    .always(function () {
      SHP.hideLoading();
    })
  }


  SHP.incrementQuantity = function(data){
    var csrftoken = SHP.getCookie('csrftoken');
    var formdata = new FormData();
    formdata.append('product_id',data.product_id);
    formdata.append('quantity',data.quantity);
    formdata.append('click_type','Increment');
    $.ajax({
      method: 'POST',
      url: '/appshop/update/product/quantity/',
      data: formdata,
      contentType: false,
      processData: false,
      beforeSend: function(xhr, settings) {
        SHP.showLoading();
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    })
    .done( function (d, textStatus, jqXHR) {
      location.reload();
    })
    .fail( function (jqXHR, textStatus, errorThrown) {
      alert(jQuery.parseJSON(jqXHR.responseText));
    })
    .always(function () {
      SHP.hideLoading();
    })
  }


  SHP.decrementQuantity = function(data){
    if (data.quantity > 0){
      var csrftoken = SHP.getCookie('csrftoken');
      var formdata = new FormData();
      formdata.append('product_id',data.product_id);
      formdata.append('quantity',data.quantity);
      formdata.append('click_type','Decrement');
      $.ajax({
        method: 'POST',
        url: '/appshop/update/product/quantity/',
        data: formdata,
        contentType: false,
        processData: false,
        beforeSend: function(xhr, settings) {
          SHP.showLoading();
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      })
      .done( function (d, textStatus, jqXHR) {
        location.reload();
      })
      .fail( function (jqXHR, textStatus, errorThrown) {
        alert(jQuery.parseJSON(jqXHR.responseText));
      })
      .always(function () {
        SHP.hideLoading();
      })      
    }

  }

  


  
  SHP.searchKey = function(){
    SHP.search_term($('#search-input').val());
    SHP.getProductList();
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


  SHP.getProductList = function () {
    var csrftoken = SHP.getCookie('csrftoken');
    $.ajax({
      method: 'GET',
      url: '/appshop/product/list/get',
      data: {'search_term':SHP.search_term(),'page_number': SHP.current_page(),'category_id':SHP.category_id()},
      dataType: 'json',
      beforeSend: function (xhr, settings) {
        SHP.showLoading();
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      })
      .done(function (d, textStatus, jqXHR) {
        SHP.productList([]);
        for (var i = 0; i < d.product_lst.length; i++) {
          SHP.productList.push(d.product_lst[i]);
        }  
        SHP.page_count(d.page_count);
        SHP.refreshPagination();
        if (SHP.productList().length > 0){
          $('.no-data').addClass('d-none')
        }else{
          $('.no-data').removeClass('d-none')
        }
      })
      .fail(function (jqXHR, textStatus, errorThrown) {
        jsonValue = jQuery.parseJSON( jqXHR.responseText );
      })
      .always(function () {
        SHP.hideLoading();
      })
    }

  SHP.refreshPagination = function(){
    var max = SHP.current_page() + 2;
    if(max > SHP.page_count())
        max = SHP.page_count();
    var min = max - 4;
    if(min < 1)
        min = 1;
    SHP.pages_list([]);
    for(i=min;i<=max;i++){
      SHP.pages_list.push(i);
    }
  };

  SHP.getPrevPage = function(){
    if(SHP.current_page() != 1){
      SHP.current_page(SHP.current_page() - 1);
      SHP.getProductList();
    }
  };

  SHP.getNextPage = function(){
    if(SHP.current_page() != SHP.page_count()){
      SHP.current_page(SHP.current_page() + 1);
      SHP.getProductList();
    }
  };

  SHP.onPageClick = function(pageno){
    SHP.current_page(pageno);
    SHP.getProductList();
  };

  SHP.getFirstPage= function(){
    SHP.current_page(1);
    SHP.getProductList();
  };

  SHP.getLastPage= function(){
    SHP.current_page(SHP.page_count());
    SHP.getProductList();
  };



})(this);

function init() {
if (document.readyState == "interactive") {
    SHP.hideLoading();
    var docUrlArr = document.URL.split('/');
    var category_id = docUrlArr[docUrlArr.length - 1];
    SHP.category_id(category_id)
    SHP.getProductList();
    ko.applyBindings(SHP);
}
}
document.onreadystatechange = init;