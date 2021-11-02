/*
* home page java script
*/

//cliente
var tiempo_ini = 0;
var tiempo_fin = 0;
var primera_vez = 0;
var timeDiff = 0;
var seBusco = 0;

setInterval('buscarCI()', 1000);

//cliente CI
function empiezaEscribir() {
    if (primera_vez == 0) {
        primera_vez = 1;
        tiempo_ini = new Date();
        tiempo_fin = new Date();
    }
    else {
        //variable que indicar si mandar el ajax para buscar
        seBusco = 0;

        tiempo = new Date();
        // time difference in ms
        timeDiff = tiempo - tiempo_fin;

        tiempo_fin = tiempo;

        // strip the ms
        timeDiff /= 1000;
    }
}

//cliente
function buscarCI() {
    try {
        ci_origen = Trim(document.getElementById('ci').value);
        if (ci_origen.length > 5) {
            tiempo = new Date();
            timeDiff = tiempo - tiempo_fin;
            tiempo_fin = tiempo;
            timeDiff /= 1000;

            imagen = '<img src="/static/img/pass/loading2.gif">';
            url_main = document.forms['formulario'].elements['url_main'].value;
            token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
            datos = {
                'ci': ci_origen,
                'operation_x': 'buscar_ci',
                'csrfmiddlewaretoken': token,
            }
            //alert(timeDiff>1.5);
            if (timeDiff > 0.7 && seBusco == 0) {
                seBusco = 1;
                //alert('termino escribir');

                //$('#tabla_cliente').fadeIn('slow');

                $("#img_load").html(imagen);
                $("#img_load").load(url_main, datos, function () {
                    //termina de cargar la ventana
                    resultadoBusqedaCI();
                });
            }
        }
    }
    catch (e) {

    }
}

//remitente
function resultadoBusqedaCI() {
    try {
        r_apellidos = document.getElementById('r_apellidos').value;
        r_nombres = document.getElementById('r_nombres').value;
        r_telefonos = document.getElementById('r_telefonos').value;
        r_direccion = document.getElementById('r_direccion').value;
        r_email = document.getElementById('r_email').value;

        apellidos = document.getElementById('apellidos');
        nombres = document.getElementById('nombres');
        telefonos = document.getElementById('telefonos');
        direccion = document.getElementById('direccion');
        email = document.getElementById('email');

        apellidos.value = r_apellidos;
        nombres.value = r_nombres;
        telefonos.value = r_telefonos;
        direccion.value = r_direccion;
        email.value = r_email;
        //alert('busqueda terminada');
    }
    catch (e) {
        alert('no existe datos para este CI');
    }
}

url_empresa = document.getElementById('url_empresa').value;

function cambiarLinea() {
    linea_select = document.getElementById('linea_select').value;
    document.form_linea.linea.value = linea_select;
    document.form_linea.submit();
}

function escogerLinea(linea) {
    document.form_linea.linea.value = linea;
    document.form_linea.submit();
}

function buscarProducto() {
    producto_dato = document.getElementById('producto_search');
    producto_val = Trim(producto_dato.value);
    if (producto_val == '') {
        alert('Debe escribir un criterio de busqueda');
        producto_dato.focus();
        return false;
    }

    //mandamos
    document.form_producto.producto.value = producto_val;
    document.form_producto.submit();
}

/*$('a[data-toggle]').on('click', function () {
    alert('asdf');
    $('#myGallery').carousel($(this).data('slide-to'));
});*/

function mostrarD(nombre_div, p_id) {
    //token
    token = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;
    url_main = document.forms['form_operation'].elements['url_main'].value;

    document.form_operation.operation_x.value = 'img_producto';
    document.form_operation.id.value = p_id;

    datos_img = {
        'operation_x': 'img_producto',
        'id': p_id,
        'csrfmiddlewaretoken': token,
    }

    //loading
    div_load = document.getElementById(nombre_div);
    div_load.className = 'overlay';
    div_load.innerHTML = '<i class="fas fa-2x fa-sync-alt fa-spin"></i>';

    imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
    $("#div_img_carousel").html(imagen);
    $("#div_img_carousel").load(url_main, datos_img, function () {
        //termina de cargar ajax
        mostrarModal(nombre_div);
    });
}

//mostrando imagenes del producto en modal
function mostrarModal(nombre_div) {
    div_load2 = document.getElementById(nombre_div);
    div_load2.className = '';
    div_load2.innerHTML = '';
    $("#myModal").modal();
}

//formulario de contacdto
function formularioContacto() {
    apellidos = document.getElementById('apellidos');
    apellidos_value = Trim(apellidos.value);

    nombres = document.getElementById('nombres');
    nombres_value = Trim(nombres.value);

    telefonos = document.getElementById('telefonos');
    telefonos_value = Trim(telefonos.value);

    mensaje = document.getElementById('mensaje');
    mensaje_value = Trim(mensaje.value);

    email = document.getElementById('email');
    email_value = Trim(email.value);

    if (apellidos_value == '') {
        alert('Debe llenar sus apellidos');
        apellidos.focus();
        return false;
    }

    if (nombres_value == '') {
        alert('Debe llenar sus nombres');
        nombres.focus();
        return false;
    }

    if (telefonos_value == '') {
        alert('Debe llenar sus telefonos');
        telefonos.focus();
        return false;
    }

    if (mensaje_value == '') {
        alert('Debe llenar su mensaje');
        mensaje.focus();
        return false;
    }

    //token
    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
    url_main = document.forms['formulario'].elements['url_main'].value;

    datos_contacto = {
        'operation_x': 'contacto',
        'nombres': nombres_value,
        'apellidos': apellidos_value,
        'telefonos': telefonos_value,
        'email': email_value,
        'mensaje': mensaje_value,
        'csrfmiddlewaretoken': token,
    }

    //div fila
    div_fila = $("#fila_resultado");
    div_fila.fadeIn('slow');

    imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
    $("#div_resultado").html(imagen);
    $("#div_resultado").load(url_main, datos_contacto, function () {
        //termina de cargar ajax
        limpiar_form_contacto();
    });
}

//limipamos
function limpiar_form_contacto() {
    apellidos = document.getElementById('apellidos');
    apellidos.value = "";

    nombres = document.getElementById('nombres');
    nombres.value = "";

    telefonos = document.getElementById('telefonos');
    telefonos.value = "";

    mensaje = document.getElementById('mensaje');
    mensaje.value = "";

    email = document.getElementById('email');
    email.value = "";
}

//mostrando confirmacion de compra
function mostrarModalCompra(producto_id, precio) {
    cantidad = document.getElementById('cantidad_' + producto_id);
    cantidad_valor = Trim(cantidad.value);
    if (cantidad_valor == '') {
        alert('Debe llenar una cantidad');
        cantidad.focus();
        return false;
    }

    //producto id
    pedido_prod_id = document.getElementById('pedido_producto_id');
    pedido_prod_id.value = producto_id;

    //producto
    pedido_pr = document.getElementById('pedido_producto');
    nombre_pr = document.getElementById('producto_nombre_' + producto_id).value;
    pedido_pr.innerHTML = nombre_pr;

    //cantidad
    pedido_cant = document.getElementById('pedido_cantidad');
    pedido_cant.value = cantidad_valor;

    //precio
    costo_pr = document.getElementById('costo_' + producto_id).value;
    pedido_prec = document.getElementById('pedido_precio');
    //pedido_prec.value = precio;
    pedido_prec.value = costo_pr;

    //total
    total = redondeo(parseFloat(costo_pr) * parseFloat(cantidad_valor), 2) + ' Bs.';
    pedido_total = document.getElementById('pedido_total');
    pedido_total.innerHTML = total;

    //talla
    // talla_ori = document.getElementById('talla');
    // talla_dest = document.getElementById('pedido_talla');
    // talla_dest.value = talla_ori.value;

    //modal
    $("#modalCompra").modal();
}

//total del pedido
function totalPedido() {
    //cantidad
    pedido_cant = document.getElementById('pedido_cantidad');
    pedido_cant_valor = Trim(pedido_cant.value);

    //total
    pedido_total = document.getElementById('pedido_total');

    if (pedido_cant_valor == '') {
        //alert('Debe llenar una cantidad');
        pedido_total.innerHTML = '0';
        pedido_cant.focus();
        return false;
    }

    //precio
    precio = document.getElementById('pedido_precio').value;

    //total
    total = redondeo(parseFloat(precio) * parseFloat(pedido_cant_valor), 2) + ' Bs.';
    pedido_total.innerHTML = total;
}

//comprar y seguir
async function agregarSeguir() {
    //verificamos cantidad
    cantidad = document.getElementById('pedido_cantidad');
    cantidad_valor = Trim(cantidad.value);
    if (cantidad == '') {
        alert('Debe llenar la cantidad');
        cantidad.focus();
        return false;
    }

    //mandamos los datos
    //token
    // token = document.forms['form_cart'].elements['csrfmiddlewaretoken'].value;
    url_main = document.forms['form_cart'].elements['url_main'].value;
    // producto_id = document.getElementById('pedido_producto_id').value;
    // costo_pr = document.getElementById('pedido_precio').value;

    // datos_cart = {
    //     'operation_x': 'add_cart',
    //     'producto': producto_id,
    //     'cantidad': cantidad_valor,
    //     'precio': costo_pr,
    //     'csrfmiddlewaretoken': token,
    // }

    //div notificaciones
    imagen = '<img src="' + url_empresa + '/static/img/pass/loading2.gif">';

    $("#div_notifications").html(imagen);
    // $("#div_notifications").load(url_main, datos_cart, function () {
    //     //termina de cargar ajax
    //     $("#modalCompra").modal('hide');
    // });

    var fd = new FormData(document.forms['formulario']);

    // for (var pair of fd.entries()) {
    //     console.log(pair[0] + ', ' + pair[1]);
    // }

    let result22;

    try {
        result22 = await $.ajax({
            url: url_main,
            method: 'POST',
            type: 'POST',
            cache: false,
            data: fd,
            contentType: false,
            processData: false,
            success: function (response) {
                if (response != 0) {
                    $("#div_notifications").html(response);
                    $("#modalCompra").modal('hide');
                } else {
                    alert('error al realizar la operacion, intentelo de nuevo');
                }
            },
            error: function (qXHR, textStatus, errorThrown) {
                console.log(errorThrown); console.log(qXHR); console.log(textStatus);
            },
        });
        //alert(result);
    }
    catch (e) {
        console.error(e);
    }

    return true;
}

//comprar ahora
function comprarAhora() {
    if (agregarSeguir()) {
        sleep(2000);
        window.open(url_empresa + '/carrito/', '_self');
    }
}

function sleep(milliseconds) {
    var start = new Date().getTime();
    for (var i = 0; i < 1e7; i++) {
        if ((new Date().getTime() - start) > milliseconds) {
            break;
        }
    }
}

//total del carrito
function totalCarrito(p_id) {
    //cantidad
    pedido_cant = document.getElementById('pedido_' + p_id);
    pedido_cant_valor = Trim(pedido_cant.value);

    //total
    pedido_total = document.getElementById('pedido_total_' + p_id);

    if (pedido_cant_valor == '') {
        //alert('Debe llenar una cantidad');
        pedido_total.innerHTML = '0';
        totalCompra();
        return false;
    }

    //precio
    precio = document.getElementById('precio_' + p_id).value;

    //total
    total = redondeo(parseFloat(precio) * parseFloat(pedido_cant_valor), 2) + ' Bs.';
    pedido_total.innerHTML = total;

    totalCompra();
}

function totalCompra() {
    lista_ids = document.getElementById('lista_ids').value;
    total_c = 0;

    if (lista_ids != '') {
        division = lista_ids.split(';');
        for (i = 0; i < division.length; i++) {
            cantidad = Trim(document.getElementById('pedido_' + division[i]).value);
            precio = Trim(document.getElementById('precio_' + division[i]).value);

            if (cantidad != '' && precio != '') {
                total_c = total_c + (parseFloat(cantidad) * parseFloat(precio));
            }
        }
        total_car = document.getElementById('total_carrito');
        total_car.innerHTML = redondeo(total_c, 2) + ' Bs.';
    }
}

//mostrando dialogo
function realizarPedido() {
    ci = document.getElementById('ci');
    ci_value = Trim(ci.value);

    apellidos = document.getElementById('apellidos');
    apellidos_value = Trim(apellidos.value);

    nombres = document.getElementById('nombres');
    nombres_value = Trim(nombres.value);

    telefonos = document.getElementById('telefonos');
    telefonos_value = Trim(telefonos.value);

    direccion = document.getElementById('direccion');
    direccion_value = Trim(direccion.value);

    email = document.getElementById('email');
    email_value = Trim(email.value);

    mensaje = document.getElementById('mensaje');
    mensaje_value = Trim(mensaje.value);

    if (ci_value == '') {
        alert('Debe llenar su CI');
        ci.focus();
        return false;
    }

    if (apellidos_value == '') {
        alert('Debe llenar sus apellidos');
        apellidos.focus();
        return false;
    }

    if (nombres_value == '') {
        alert('Debe llenar sus nombres');
        nombres.focus();
        return false;
    }

    if (telefonos_value == '') {
        alert('Debe llenar sus telefonos');
        telefonos.focus();
        return false;
    }

    if (direccion_value == '') {
        alert('Debe llenar su direccion');
        direccion.focus();
        return false;
    }

    //lista de productos para el pedido
    lista_ids = document.getElementById('lista_ids').value;
    if (lista_ids == '') {
        alert('debe tener al menos un producto');
        return false;
    }

    division = lista_ids.split(';');
    lista_productos_ids = '';
    lista_cantidad = '';

    for (i = 0; i < division.length; i++) {
        cantidad = Trim(document.getElementById('pedido_' + division[i]).value);

        if (cantidad != '') {
            lista_productos_ids += division[i] + '|';
            lista_cantidad += cantidad + '|';
        }
    }

    if (lista_productos_ids == '') {
        alert('Debe Comprar al menos un producto');
        return false;
    }

    //modal
    $("#modalCarrito").modal();
}

//formulario de contacdto
function confirmarPedido() {

    //lista de productos para el pedido
    lista_ids = document.getElementById('lista_ids').value;

    division = lista_ids.split(';');
    lista_productos_ids = '';
    lista_cantidad = '';

    for (i = 0; i < division.length; i++) {
        cantidad = Trim(document.getElementById('pedido_' + division[i]).value);

        if (cantidad != '' && cantidad != '0') {
            lista_productos_ids += division[i] + '|';
            lista_cantidad += cantidad + '|';
        }
    }

    if (lista_productos_ids == '') {
        alert('Debe Comprar al menos un producto');
        return false;
    }

    lista_productos_ids = lista_productos_ids.substring(0, lista_productos_ids.length - 1);
    lista_cantidad = lista_cantidad.substring(0, lista_cantidad.length - 1);

    //token
    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
    url_main = document.forms['formulario'].elements['url_main'].value;

    tipo_pedido = document.getElementById('tipo_pedido').value;

    datos_pedido = {
        'operation_x': 'realizar_pedido',
        'ci': ci_value,
        'nombres': nombres_value,
        'apellidos': apellidos_value,
        'telefonos': telefonos_value,
        'direccion': direccion_value,
        'email': email_value,
        'mensaje': mensaje_value,
        'tipo_pedido': tipo_pedido,
        'lista_productos_ids': lista_productos_ids,
        'lista_cantidad': lista_cantidad,
        'csrfmiddlewaretoken': token,
    }

    //div fila
    div_fila = $("#fila_resultado");
    div_fila.fadeIn('slow');

    imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
    $("#div_resultado").html(imagen);
    $("#div_resultado").load(url_main, datos_pedido, function () {
        //termina de cargar ajax
        finalizarCarrito();

        error_de_carrito = document.getElementById('error_carrito').value;
        if (error_de_carrito != '1') {
            const total_compra = document.getElementById('total_carrito').innerHTML;
            const head = 'pedido de venta';
            const body = 'Cliente: ' + apellidos_value + ' ' + nombres_value + '\nFonos: ' + telefonos_value + '\nTotal: ' + total_compra + "\nMensaje: " + mensaje_value;
            const id = document.getElementById('lista_notificacion').value;

            //btn_push= document.getElementById('btn_webpush');
            url_push = document.forms['formulario'].elements['url_webpush'].value;

            datos_push = {
                'head': head,
                'body': body,
                'id': id,
                'csrfmiddlewaretoken': token,
            }

            $("#div_push_result").html(imagen);
            $("#div_push_result").load(url_push, datos_push, function () {
                //termina de cargar ajax
                //finalizarCarrito();
                //alert('push enviado');
            });
        }

    });

}

//cancelamos
function cancelarPedido() {
    $("#modalCarrito").modal('hide');
}

//finalizar carrito
function finalizarCarrito() {
    $("#modalCarrito").modal('hide');
    $("#tabla_cliente").fadeOut('slow');
    $("#tabla_detalle").fadeOut('slow');
    $("#tabla_boton").fadeOut('slow');

    //notificaciones
    div_noti = $("#div_notifications");
    div_noti.html('<i class="fas fa-cart-arrow-down notification_icon"></i>');

    //webpush
}

//para ir al carrito desde el icono
function irCarrito(direccion) {
    window.open(direccion, '_self');
}

//eliminar producto
function eliminarProducto(p_id) {
    if (confirm('Esta seguro de eliminar este producto?')) {
        document.form_delete.operation_x.value = 'delete';
        document.form_delete.producto.value = p_id;
        document.form_delete.submit();
    }
}

//forma de pago
function formaDePago(tipo) {
    tabla_qr = $("#tabla_qr");
    tabla_transferencia = $("#tabla_transferencia");

    if (tipo == "qr") {
        document.formulario.tipo_pedido.value = 'qr';
        tabla_qr.fadeIn('slow');
        tabla_transferencia.fadeOut('slow');
    }
    else {
        document.formulario.tipo_pedido.value = 'transferencia';
        tabla_qr.fadeOut('slow');
        tabla_transferencia.fadeIn('slow');
    }
}

//ropa, detalle del producto
function detalleProducto(producto_id, producto) {
    document.form_detalle.id.value = producto_id;
    document.form_detalle.producto.value = producto;
    document.form_detalle.submit();
}

function paginaInicio() {
    document.form_inicio.submit();
}

//seleccion de ingresdientes y extras
//acc, modal componentes
function componentesProducto(numero_registro) {
    $('#modal-componentes-' + numero_registro).modal('show');
    loadComponentes(numero_registro);

    //extras
    loadExtras(numero_registro);
    //refrescos
    loadRefrescos(numero_registro);
    //papas
    loadPapas(numero_registro);

    ajustarPrecioExtras(numero_registro);

    totalPedidoVenta(numero_registro);
}

//acc, modal extras
function extrasProducto(numero_registro) {
    $('#modal-extras-' + numero_registro).modal('show');
    loadExtras(numero_registro);
    ajustarPrecioExtras(numero_registro);
    totalPedidoVenta(numero_registro);
}

//acc, carga de componentes
function loadComponentes(numero_registro) {
    componentes_ids = document.getElementById('componentes_ids_' + numero_registro).value;

    if (Trim(componentes_ids) != '') {
        div_co = Trim(componentes_ids).split('|');
        for (ic = 0; ic < div_co.length; ic++) {
            aux_c = document.forms['formulario'].elements['componente_' + numero_registro + '_' + div_co[ic]].value;
            aux_c2 = document.getElementById('aux_componente_' + numero_registro + '_' + div_co[ic]);

            if (aux_c == '1') {
                aux_c2.checked = true;
            }
            else {
                aux_c2.checked = false;
            }
        }
    }
}

//acc, carga de extras
function loadExtras(numero_registro) {
    extras_ids = document.getElementById('extras_ids_' + numero_registro).value;
    if (Trim(extras_ids) != '') {
        div_ex = Trim(extras_ids).split('|');
        for (ie = 0; ie < div_ex.length; ie++) {
            aux_c = document.forms['formulario'].elements['extra_' + numero_registro + '_' + div_ex[ie]].value;
            aux_c2 = document.getElementById('aux_extra_' + numero_registro + '_' + div_ex[ie]);
            if (aux_c == '1') {
                aux_c2.checked = true;
            }
            else {
                aux_c2.checked = false;
            }
        }
    }
}

//acc, carga de refrescos
function loadRefrescos(numero_registro) {
    refrescos_ids = document.getElementById('refrescos_ids_' + numero_registro).value;
    if (Trim(refrescos_ids) != '') {
        div_re = Trim(refrescos_ids).split('|');
        for (ie = 0; ie < div_re.length; ie++) {
            aux_c = document.forms['formulario'].elements['refresco_' + numero_registro + '_' + div_re[ie]].value;
            aux_c2 = document.getElementById('aux_refresco_' + numero_registro + '_' + div_re[ie]);
            if (aux_c == '1') {
                aux_c2.checked = true;
            }
            else {
                aux_c2.checked = false;
            }
        }
    }
}

//acc, carga de papas
function loadPapas(numero_registro) {
    papas_ids = document.getElementById('papas_ids_' + numero_registro).value;
    if (Trim(papas_ids) != '') {
        div_re = Trim(papas_ids).split('|');
        for (ie = 0; ie < div_re.length; ie++) {
            aux_c = document.forms['formulario'].elements['papa_' + numero_registro + '_' + div_re[ie]].value;
            aux_c2 = document.getElementById('aux_papa_' + numero_registro + '_' + div_re[ie]);
            if (aux_c == '1') {
                aux_c2.checked = true;
            }
            else {
                aux_c2.checked = false;
            }
        }
    }
}

//acc, ajustar precio extras
function ajustarPrecioExtras(numero_registro) {
    extras_ids = document.getElementById('extras_ids_' + numero_registro).value;
    precio_extra = 0;
    if (Trim(extras_ids) != '') {
        div_ex = Trim(extras_ids).split('|');
        for (ie = 0; ie < div_ex.length; ie++) {
            aux_c = document.forms['formulario'].elements['extra_' + numero_registro + '_' + div_ex[ie]].value;

            if (aux_c == '1') {
                precio_add = parseFloat(document.forms['formulario'].elements['extra_precio_' + numero_registro + '_' + div_ex[ie]].value);
                precio_extra += precio_add;
            }
        }
    }

    //refrescos
    refrescos_ids = document.getElementById('refrescos_ids_' + numero_registro).value;
    if (Trim(refrescos_ids) != '') {
        div_re = Trim(refrescos_ids).split('|');
        for (ie = 0; ie < div_re.length; ie++) {
            aux_c = document.forms['formulario'].elements['refresco_' + numero_registro + '_' + div_re[ie]].value;

            if (aux_c == '1') {
                precio_add = parseFloat(document.forms['formulario'].elements['refresco_precio_' + numero_registro + '_' + div_re[ie]].value);
                precio_extra += precio_add;
            }
        }
    }

    //papas
    papas_ids = document.getElementById('papas_ids_' + numero_registro).value;
    if (Trim(papas_ids) != '') {
        div_re = Trim(papas_ids).split('|');
        for (ie = 0; ie < div_re.length; ie++) {
            aux_c = document.forms['formulario'].elements['papa_' + numero_registro + '_' + div_re[ie]].value;

            if (aux_c == '1') {
                precio_add = parseFloat(document.forms['formulario'].elements['papa_precio_' + numero_registro + '_' + div_re[ie]].value);
                precio_extra += precio_add;
            }
        }
    }

    costo_obj = document.getElementById('costo_' + numero_registro);
    costo_aux = parseFloat(document.getElementById('costo_aux_' + numero_registro).value);

    costo_obj.value = redondeo(costo_aux + precio_extra, 2);

    //txt precio
    txt_precio = document.getElementById('txt_precio');
    txt_precio.innerHTML = costo_obj.value + ' Bs.';
}

//acc, marcar componente
function marcarComponente(check_c, componente) {
    componente_form = document.forms['formulario'].elements[componente];
    if (check_c.checked) {
        componente_form.value = '1';
    }
    else {
        componente_form.value = '0';
    }
}

//acc, marcar extra
function marcarExtra(check_c, extra, numero_registro) {
    extra_form = document.forms['formulario'].elements[extra];
    if (check_c.checked) {
        extra_form.value = '1';
    }
    else {
        extra_form.value = '0';
    }
    ajustarPrecioExtras(numero_registro);
    totalPedidoVenta(numero_registro);
}

//acc, marcar refresco
function marcarRefresco(check_c, extra, numero_registro) {

    //desmarcamos todo
    a_refrescos_ids = Trim(document.getElementById('refrescos_ids_' + numero_registro).value);
    if (a_refrescos_ids != '') {
        a_div = a_refrescos_ids.split('|');
        for (ai = 0; ai < a_div.length; ai++) {
            a_re = document.forms['formulario'].elements['refresco_' + numero_registro + '_' + a_div[ai]];
            a_aux = document.getElementById('aux_refresco_' + numero_registro + '_' + a_div[ai]);

            a_re.value = '0';
            a_aux.checked = false;
        }
    }

    //siempre marcado el seleccionado
    check_c.checked = true;
    extra_form = document.forms['formulario'].elements[extra];
    extra_form.value = '1';

    ajustarPrecioExtras(numero_registro);
    totalPedidoVenta(numero_registro);
}

//acc, marcar papa
function marcarPapa(check_c, extra, numero_registro) {

    //desmarcamos todo
    a_papas_ids = Trim(document.getElementById('papas_ids_' + numero_registro).value);
    if (a_papas_ids != '') {
        a_div = a_papas_ids.split('|');
        for (ai = 0; ai < a_div.length; ai++) {
            a_re = document.forms['formulario'].elements['papa_' + numero_registro + '_' + a_div[ai]];
            a_aux = document.getElementById('aux_papa_' + numero_registro + '_' + a_div[ai]);

            a_re.value = '0';
            a_aux.checked = false;
        }
    }

    check_c.checked = true;
    extra_form = document.forms['formulario'].elements[extra];
    extra_form.value = '1';

    ajustarPrecioExtras(numero_registro);
    totalPedidoVenta(numero_registro);
}

//acc, total por producto
function totalPedidoVenta(numero_registro) {
    total_pedido = 0;

    cantidad = Trim(document.getElementById('cantidad_' + numero_registro).value);
    costo = Trim(document.getElementById('costo_' + numero_registro).value);
    if (cantidad != '' && costo != '') {
        cantidad_valor = parseFloat(cantidad);
        costo_valor = parseFloat(costo);
        total = cantidad_valor * costo_valor;
        total_pedido += total;
        obj_total = document.getElementById('total_' + numero_registro);
        obj_total.value = redondeo(total, 2);
    }
}

function nextPedido() {
    tab_forma_pago = $('#custom-tabs-one-profile-tab');
    tab_forma_pago.click();
}

function anteriorPedido() {
    tab_datos = $('#custom-tabs-one-home-tab');
    tab_datos.click();
}