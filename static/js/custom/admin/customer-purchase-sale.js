(function (window) {
  SHP = {}
  SHP.search_term = ko.observable('');
  SHP.customer_name = ko.observable('');
  SHP.customer_id = ko.observable('');
  SHP.received_amount = ko.observable(0);
  SHP.product_quantity = ko.observable('');
  SHP.product_id = ko.observable('');
  SHP.product_price = ko.observable('');
  SHP.selected_customer_name = ko.observable('');
  SHP.selected_customer_no = ko.observable('');
  SHP.active_add_btn = ko.observable('');
  SHP.sales_date = ko.observable('');
  SHP.grand_total = ko.observable(0);
  SHP.active_order_btn = ko.observable('');
  SHP.productList = ko.observableArray([]);
  SHP.actual_product_list = ko.observableArray([]);
  SHP.customerList = ko.observableArray([]);
  SHP.mainSelectedList = ko.observableArray([]);


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



   SHP.item = function () {
    this.index = ko.observable('');
    this.available_product_list = ko.observableArray([]);
    this.selected_product_id = ko.observable('');
    this.selected_product_unit_price = ko.observable('');
    this.selected_quantity = ko.observable('');
    this.total_price = ko.observable('');
    this.fill = function (d) {
    this.index('' || d.index);
    this.available_product_list('' || d.available_product_list);
    this.selected_product_id('' || d.selected_product_id);
    this.selected_product_unit_price('' || d.selected_product_unit_price);
    this.selected_quantity('' || d.selected_quantity);
    this.total_price('' || d.total_price);    
      }
  }


  SHP.additem = function () {
    $('#productHead').removeClass('d-none')
    var info =new  SHP.item();
    d = {
        index: SHP.actual_product_list().length,
        available_product_list:SHP.productList(),
        selected_product_id: '',
        selected_product_unit_price: '',
        selected_quantity: '',
        total_price: '',
        }
    info.fill(d);
    SHP.actual_product_list.push(info);
    console.log(SHP.actual_product_list())
  }


  SHP.priceChange = function(data){
    console.log(data)
    var item_index=data.index()
    var price = data.selected_product_unit_price()
    var quantity = data.selected_quantity()
    price = parseFloat(price)
    quantity = parseFloat(quantity)
    var total = price * quantity

    SHP.actual_product_list()[item_index].total_price(total)
    SHP.findGrandTotal();
  }

  SHP.quantityChange = function(data){
    var item_index=data.index()
    var price = data.selected_product_unit_price()
    var quantity = data.selected_quantity()
    price = parseFloat(price)
    quantity = parseFloat(quantity)
    var total = price * quantity

    SHP.actual_product_list()[item_index].total_price(total)
    SHP.findGrandTotal();
  }

  SHP.findGrandTotal = function(){
    var grand_total = 0
    for(var i=0;i<SHP.actual_product_list().length;i++){
      grand_total = grand_total+SHP.actual_product_list()[i].total_price()
    }
    SHP.grand_total(grand_total)
  }


  SHP.productChange = function(data){
    var item_index=data.index()
    const result = SHP.productList().find( ({ product_id }) => product_id ===  data.selected_product_id());
    SHP.actual_product_list()[item_index].selected_product_unit_price(result.s_price)
  }


  SHP.deleteProduct = function(data) {
    SHP.actual_product_list.remove(data)
    SHP.findGrandTotal();
  }


  SHP.customerPurchaseCreate = function(){ 
    SHP.mainSelectedList([])
    for(var i=0;i<SHP.actual_product_list().length;i++){
      d = {}
      d['selected_product_id'] = SHP.actual_product_list()[i].selected_product_id()
      d['selected_product_unit_price'] = SHP.actual_product_list()[i].selected_product_unit_price()
      d['selected_quantity'] = SHP.actual_product_list()[i].selected_quantity()
      d['total_price'] = SHP.actual_product_list()[i].total_price()
      SHP.mainSelectedList().push(d)
    }
    var csrftoken = SHP.getCookie('csrftoken');
    var formdata = new FormData();
    formdata.append('sales_date',SHP.sales_date());
    formdata.append('received_amount', SHP.received_amount());
    formdata.append('grand_total', SHP.grand_total());
    formdata.append('selected_customer_name', SHP.selected_customer_name());
    formdata.append('selected_customer_no', SHP.selected_customer_no());
    formdata.append('main_products_list', ko.toJSON(SHP.mainSelectedList()));
    $.ajax({
      method: 'POST',
      url: '/appshop/customer/purchase/sales',
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
      // $('#errorModal').on('hidden.bs.modal', function (e) {
      location.href = '/customer/sales/list/'
      // });
    })
    .fail( function (jqXHR, textStatus, errorThrown) {
      alert(jqXHR.responseText)
    })
    .always(function(){
      SHP.hideLoading();
    })
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

  
  SHP.getCustomerList = function () {
    var csrftoken = SHP.getCookie('csrftoken');
    $.ajax({
      method: 'GET',
      url: '/appshop/get/all/customers/list',
      dataType: 'json',
      beforeSend: function (xhr, settings) {
        SHP.showLoading();
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      })
      .done(function (d, textStatus, jqXHR) {
        SHP.customerList([]);
        for (var i = 0; i < d.length; i++) {
          SHP.customerList.push(d[i]);
        }  

        SHP.getProductList();
      })
      .fail(function (jqXHR, textStatus, errorThrown) {
        jsonValue = jQuery.parseJSON( jqXHR.responseText );
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
        console.log(111,d)
        SHP.productList([]);
        for (var i = 0; i < d.length; i++) {
          SHP.productList.push(d[i]);
        }  
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