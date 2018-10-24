function activarAutocomplete(){
    var productos = []
    $.getJSON( "/shop/obtenerProductosJson", function( data ) {
      $.each( data, function( key, val ) {
        productos.push({ id: val["pk"] , name: val["fields"]["nombre"]})
      });
    });

    var $input = $(".typeahead");
    $input.typeahead({
      source: productos,
      autoSelect: true
    });
    $input.change(function() {
      var current = $input.typeahead("getActive");
      if (current) {
        // Some item from your model is active!
        if (current.name == $input.val()) {
          $('<form method="GET" action="/shop/producto"><input type="text" value="'+current.id+'" name="id" /></form>').appendTo('body').submit();
        } else {
          // This means it is only a partial match, you can either add a new item
          // or take the active if you don't want new items
        }
      } else {
        // Nothing is active so it is a new value (or maybe empty value)
      }
    });
}
function addProductCart(id){
    $.post( "/shop/addProductCart/", { id_prod_add: id } , function( data ) {
        $("#changuito").html( data );
        $("#changuito").effect( "slide", "slow" );
    });
}
function lessProductCart(id){
    $.post( "/shop/lessProductCart/", { id_prod_less: id } , function( data ) {
        $("#changuito").html( data );
    }).done(function() {
        if (window.location.pathname.includes("carretilla")){
            if ($("#totalProd").val() == "0"){
                window.location = "/shop/shop";
            }else{
                $.post( "/shop/regarcaPasoUno/", function( data ) {
                    $("#tab-pane-carretilla").html( data );
                });
            }
        }
    });
}

function emptyCart(id){
    $.post( "/shop/emptyCart/" , function( data ) {
        $("#changuito").html( data );
    });
}
function traer_prod_categoria(id_cat){
    $("#id_categoria").val(id_cat);
    $("#form_prod_categoria").submit();
}

$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
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
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});