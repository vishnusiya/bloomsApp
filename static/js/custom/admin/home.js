(function (window) {
  SHP = {}
  SHP.search_term = ko.observable('');
  SHP.categoryList = ko.observableArray([]);
  SHP.pages_list = ko.observableArray([]);
  SHP.date_sort_order = ko.observable('ascending');
  SHP.no_of_date_sort = ko.observable('false');
  SHP.current_page = ko.observable(1);
  SHP.page_count = ko.observable();


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


  SHP.categoryDetails = function(data){
    location.href="/product/list/" +data.category_id
  }

  
  SHP.searchKey = function(){
    SHP.search_term($('#search-input').val());
    SHP.getCategoryList();
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

  // SHP.clickSaleDateSort = function(){
  //   SHP.current_page(1);
  //   SHP.no_of_date_sort('true');
  //   if(SHP.date_sort_order() == 'descending'){
  //     SHP.date_sort_order('ascending');
  //   }else{
  //     SHP.date_sort_order('descending');
  //   }
  //   SHP.getProductList();
  // };

  SHP.exportProducts = function () {
    location.href = '/appshop/export/products/csv/'
  };

  SHP.getCategoryList = function () {
    var csrftoken = SHP.getCookie('csrftoken');
    $.ajax({
      method: 'GET',
      url: '/appshop/product/category/list/get',
      data: {'search_term':SHP.search_term(),'page_number': SHP.current_page()},
      dataType: 'json',
      beforeSend: function (xhr, settings) {
        SHP.showLoading();
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      })
      .done(function (d, textStatus, jqXHR) {
        SHP.categoryList([]);
        for (var i = 0; i < d.length; i++) {
          SHP.categoryList.push(d[i]);
        }  
        // SHP.page_count(d.page_count);
        // SHP.refreshPagination();
        if (SHP.categoryList().length > 0){
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
    SHP.getCategoryList();
    ko.applyBindings(SHP);
}
}
document.onreadystatechange = init;