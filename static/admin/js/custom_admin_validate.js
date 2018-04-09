$(document).ready(function() {



    $("#id_cliente").change(function() {

        $.ajax({

            method: "GET",

            url: "/obtener_cliente",

            data: { id_cliente: $("#id_cliente").val() },

            dataType: "json"

        }).done(function(retorno) {

            $("#id_direccion_envio").val(retorno.direccion)

            $("#id_mail").val(retorno.mail)

            $("#id_telefono").val(retorno.telefono)

        });

    });



    $(".add-row").click(function(){

        total_total = parseInt($('#id_total').val());

        $('select[id^="id_productopedido_set-"]').each(function( index ) {

            var idSelect = $( this ).prop('id')

            if ( idSelect.indexOf("prefix") < 0){

                alert(idSelect);
/////////////////////////////////////////////////////////////////
                $('#'+idSelect).replaceWith('<input type="text" name="'+idSelect+'" id="'+idSelect+'" class="typeahead" data-provide="typeahead">');
    
                var productos = []
                $.getJSON( "/shop/obtenerProductosJson/", function( data ) {
                  $.each( data, function( key, val ) {
                    productos.push({ id: val["pk"] , name: val["fields"]["nombre"]})
                  });

                  var $input = $('#'+idSelect);
                        $input.typeahead({
                        source: productos,
                        autoSelect: true
                    });
                
                    $input.change(function() {
                        var current = $input.typeahead("getActive");
                        if (current) {
                            // Some item from your model is active!
                            if (current.name == $input.val()) {
                                alert(current.name);
                                //$('<form method="GET" action="/shop/producto"><input type="text" value="'+current.id+'" name="id" /></form>').appendTo('body').submit();
                            } else {
                            // This means it is only a partial match, you can either add a new item
                            // or take the active if you don't want new items
                            }
                        } else {
                            // Nothing is active so it is a new value (or maybe empty value)
                        }
                    });
                });                   
/////////////////////////////////////////////////////////////////

                $('#' + idSelect ).change(function() {

                    $.ajax({

                        method: "GET",

                        url: "/obtener_producto",

                        data: { id_producto: $(this).val() },

                        dataType: "json"

                    }).done(function(retorno) {

                        $("#id_productopedido_set-"+ index +"-precio_venta_distribuidor").val(retorno.precio_venta_publico);

                        $("#id_productopedido_set-"+ index +"-cantidad_productos").val(1);

                        var precioDistri = $('#id_productopedido_set-'+ index +'-precio_venta_distribuidor').val();

                        var cantidad = $('#id_productopedido_set-'+ index +'-cantidad_productos').val();

                        var total = precioDistri * cantidad;

                        total = total - ( (total * $('#id_productopedido_set-'+ index +'-descuento').val() ) / 100 );

                        $('#id_productopedido_set-'+ index +'-total').val(total);

                        

                        if ( $('#id_productopedido_set-'+ index +'-total').val() != undefined){

                            total_total = parseInt(total_total) + parseInt($('#id_productopedido_set-'+ index +'-total').val());

                        }

                        

                        $('#id_total').val(parseInt(total_total));

                        

                    });

                });

            }

        });



        $('input[id$="cantidad_productos"]').each(function( index ) {

            var idSelect = $( this ).prop('id')

            calcularTotal(index, idSelect)

        });



        $('input[id$="precio_venta_distribuidor"]').each(function( index ) {

            var idSelect = $( this ).prop('id')

            calcularTotal(index, idSelect)

        });



        $('input[id$="descuento"]').each(function( index ) {

            var idSelect = $( this ).prop('id')

            calcularTotal(index, idSelect)

        });



    });



    

    if ($("#id_estado").val() == ''){

        $("#id_estado option[value='5']").remove();

        $("#id_estado option[value='11']").remove();

    }

    



    if ($("#id_estado").val() == '5'){

        $("#id_estado option[value='1']").remove();

        $("#id_estado option[value='4']").remove();

        $("#id_estado option[value='6']").remove();

        $("p.deletelink-box").css("display","none");

        $('#productopedido_set-group').find('a').each(function() {

            $(this).hide();

        });



        var nodes = document.getElementById("productopedido_set-group").getElementsByTagName('*');

        for(var i = 0; i < nodes.length; i++){

            nodes[i].readOnly = true;

        }



        $("select[id^='id_productopedido_set-']").each(function() {

            $(this).css( "pointer-events", "none" );

            $(this).css( "cursor", "default" );

        });



    }



    



    if ($("#id_estado").val() == '11'){

        $("#id_estado option[value='1']").remove();

        $("#id_estado option[value='4']").remove();

        $("#id_estado option[value='5']").remove();

        $("#id_estado option[value='6']").remove();

        $("p.deletelink-box").css("display","none");

        $('#productopedido_set-group').find('a').each(function() {

            $(this).hide();

        });



        var nodes = document.getElementById("productopedido_set-group").getElementsByTagName('*');

        for(var i = 0; i < nodes.length; i++){

            nodes[i].readOnly = true;

        }



        $("select[id^='id_productopedido_set-']").each(function() {

            $(this).css( "pointer-events", "none" );

            $(this).css( "cursor", "default" );

        });

    }



    document.getElementById("id_total").readOnly = true;



});







	



function calcularTotal(index, idSelect){



    if ( idSelect.indexOf("prefix") < 0){



        $('#' + idSelect ).change(function() {

            var precioDistri = $('#id_productopedido_set-'+ index +'-precio_venta_distribuidor').val();

            var cantidad = $('#id_productopedido_set-'+ index +'-cantidad_productos').val();

            var total = precioDistri * cantidad;

            total = total - ( (total * $('#id_productopedido_set-'+ index +'-descuento').val() ) / 100 );

            $('#id_productopedido_set-'+ index +'-total').val(total);

            

            total = 0;

            $('select[id^="id_productopedido_set-"]').each(function( index ) {

                if ( $('#id_productopedido_set-'+ index +'-total').val() != undefined){

                    total = parseInt(total) + parseInt($('#id_productopedido_set-'+ index +'-total').val());

                }

            });

            

            $('#id_total').val(parseInt(total));

            

        });



    }



}    