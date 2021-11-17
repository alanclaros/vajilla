
//modal function
modalFunction = document.getElementById('modalFunctionSuccess');
modalF = $('#modalForm');
div_modulo = $("#div_block_content");

modalPrintFunctionB1 = document.getElementById('modalPrintFunctionB1');
modalPrintFunctionB2 = document.getElementById('modalPrintFunctionB2');
modalFPrint = $('#modalPrint');

function ventaWarning() {
    modalF = $('#modalForm');
    modalF.modal('toggle');
}

function sendFormVenta(operation, message) {
    switch (operation) {
        case ('add'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'ventaSaveForm();';
                modalSetParameters('success', 'center', 'Ventas!', 'Esta seguro de querer adicionar esta Preventa?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                modalSetParameters('warning', 'center', 'Ventas!', resValidation, 'Cancelar', 'Volver');
                modalFunction.value = 'ventaWarning();';
                modalF.modal();
            }
            break;

        case ('modify'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'ventaSaveForm();';
                modalSetParameters('success', 'center', 'Ventas!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                modalSetParameters('warning', 'center', 'Ventas!', resValidation, 'Cancelar', 'Volver');
                modalFunction.value = 'ventaWarning();';
                modalF.modal();
            }
            break;

        case ('anular'):
            modalFunction.value = 'ventaSaveForm();';
            //set data modal
            modalSetParameters('danger', 'center', 'Ventas!', 'Esta seguro de querer anular ' + message + '?', 'Cancelar', 'Anular');
            modalF.modal();

            break;

        case ('pasar_venta'):
            modalFunction.value = 'ventaSaveForm();';
            //set data modal
            modalSetParameters('success', 'center', 'Ventas!', 'Esta seguro de querer confirmar esta venta?', 'Cancelar', 'Confirmar');
            modalF.modal();

            break;

        case ('pasar_venta_anular'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'ventaSaveForm();';
                modalSetParameters('danger', 'center', 'Ventas!', 'Esta seguro de querer anular esta Venta?', 'Cancelar', 'Anular');
                modalF.modal();
            }
            else {
                modalSetParameters('warning', 'center', 'Ventas!', resValidation, 'Cancelar', 'Volver');
                modalFunction.value = 'ventaWarning();';
                modalF.modal();
            }
            break;

        case ('aumento_pedido'):
            resValidation = validarAumentoVenta();
            if (resValidation === true) {
                modalFunction.value = 'ventaSaveForm();';
                modalSetParameters('success', 'center', 'Ventas!', 'Esta seguro de adicionar este aumento?', 'Cancelar', 'Adicionar');
                modalF.modal();
            }
            else {
                modalSetParameters('warning', 'center', 'Ventas!', resValidation, 'Cancelar', 'Volver');
                modalFunction.value = 'ventaWarning();';
                modalF.modal();
            }
            break;

        case ('pasar_salida'):
            modalFunction.value = 'ventaSaveForm();';
            //set data modal
            modalSetParameters('success', 'center', 'Ventas!', 'Esta seguro de querer confirmar esta salida de almacen?', 'Cancelar', 'Confirmar');
            modalF.modal();

            break;

        case ('pasar_salida_anular'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'ventaSaveForm();';
                modalSetParameters('danger', 'center', 'Ventas!', 'Esta seguro de querer anular esta salida de almacen?', 'Cancelar', 'Anular');
                modalF.modal();
            }
            else {
                modalSetParameters('warning', 'center', 'Ventas!', resValidation, 'Cancelar', 'Volver');
                modalFunction.value = 'ventaWarning();';
                modalF.modal();
            }
            break;

        case ('pasar_vuelta'):
            resValidation = verifyPasarVueltaVenta();
            if (resValidation === true) {
                modalFunction.value = 'ventaSaveForm();';
                modalSetParameters('success', 'center', 'Ventas!', 'Esta seguro de querer devolver los productos a Almacen?', 'Cancelar', 'Confirmar');
                modalF.modal();
            }
            else {
                modalSetParameters('warning', 'center', 'Ventas!', resValidation, 'Cancelar', 'Volver');
                modalFunction.value = 'ventaWarning();';
                modalF.modal();
            }
            break;

        case ('pasar_vuelta_anular'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'ventaSaveForm();';
                modalSetParameters('danger', 'center', 'Ventas!', 'Esta seguro de querer anular esta vuelta a almacen?', 'Cancelar', 'Anular');
                modalF.modal();
            }
            else {
                modalSetParameters('warning', 'center', 'Ventas!', resValidation, 'Cancelar', 'Volver');
                modalFunction.value = 'ventaWarning();';
                modalF.modal();
            }
            break;

        case ('gastos'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'ventaSaveForm();';
                modalSetParameters('success', 'center', 'Ventas!', 'Esta seguro de querer adicionar este gasto?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                modalSetParameters('warning', 'center', 'Ventas!', resValidation, 'Cancelar', 'Volver');
                modalFunction.value = 'ventaWarning();';
                modalF.modal();
            }
            break;

        case ('cobros'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'ventaSaveForm();';
                modalSetParameters('success', 'center', 'Ventas!', 'Esta seguro de querer adicionar este cobro?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                modalSetParameters('warning', 'center', 'Ventas!', resValidation, 'Cancelar', 'Volver');
                modalFunction.value = 'ventaWarning();';
                modalF.modal();
            }
            break;

        case ('pasar_finalizado'):
            modalFunction.value = 'ventaSaveForm();';
            modalSetParameters('success', 'center', 'Ventas!', 'Esta seguro de querer finalizar esta venta?', 'Cancelar', 'Finalizar');
            modalF.modal();

            break;

        case ('pasar_finalizado_anular'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'ventaSaveForm();';
                modalSetParameters('danger', 'center', 'Ventas!', 'Esta seguro de querer anular esta finalizacion?', 'Cancelar', 'Anular');
                modalF.modal();
            }
            else {
                modalSetParameters('warning', 'center', 'Ventas!', resValidation, 'Cancelar', 'Volver');
                modalFunction.value = 'ventaWarning();';
                modalF.modal();
            }
            break;

        default:
            break;
    }
}

function validarAumentoVenta() {
    const t_final = Trim(document.getElementById('total_final').value);
    if (t_final == '') {
        return 'Debe registrar al menos 1 producto';
    }
    else {
        const t_valor = parseFloat(t_final);
        if (t_valor <= 0) {
            return 'Debe llenar la cantidad y costo de los productos';
        }
        else {
            return true;
        }
    }
}

function ventaSaveForm() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function sendSearchVenta() {
    div_modulo = $("#div_block_content");
    sendFormObject('search', div_modulo);
}

//confirmar anular venta
function anularPreventa() {
    modalSetParameters('danger', 'center', 'Ventas!', 'Esta seguro de querer anular esta preventa?', 'Cancelar', 'Anular');
    modalFunction.value = 'anularPreventaSend();';
    modalF.modal();
}

function anularPreventaSend() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function anularVenta() {
    motivo_an = Trim(document.getElementById('motivo_anula').value);
    if (motivo_an == '') {
        modalSetParameters('warning', 'center', 'Ventas!', 'Debe llenar el motivo', 'Cancelar', 'Volver');
        modalFunction.value = 'ventaWarning();';
        modalF.modal();
        return false;
    }

    modalSetParameters('danger', 'center', 'Ventas!', 'Esta seguro de querer anular esta venta?', 'Cancelar', 'Anular');
    modalFunction.value = 'anularVentaSend();';
    modalF.modal();
}

function anularVentaSend() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

//acc, buscar cliente
function buscarClienteVenta() {
    obj_ci_nit = Trim(document.getElementById('buscar_ci_nit').value);
    obj_apellidos = Trim(document.getElementById('buscar_apellidos').value);
    obj_nombres = Trim(document.getElementById('buscar_nombres').value);

    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

    url_main = document.getElementById('url_main').value;
    ruta_imagen = url_empresa + '/static/img/pass/loading.gif';
    imagen = '<td colspan="4" class="left w100"><img src="' + ruta_imagen + '"></td>';

    datos = {
        'module_x': document.forms['form_operation'].elements['module_x'].value,
        'operation_x': 'buscar_cliente',
        'ci_nit': obj_ci_nit,
        'apellidos': obj_apellidos,
        'nombres': obj_nombres,
        'csrfmiddlewaretoken': token,
    }

    $("#div_clientes").fadeIn('slow');
    $("#div_clientes").html(imagen);
    $("#div_clientes").load(url_main, datos, function () {
        //termina de cargar la ventana
    });
}

//acc, selecccionar cliente
function seleccionarClienteVenta(cliente_id) {
    obj_ci_nit = document.getElementById('ci_nit_' + cliente_id).value;
    obj_apellidos = document.getElementById('apellidos_' + cliente_id).value;
    obj_nombres = document.getElementById('nombres_' + cliente_id).value;
    obj_telefonos = document.getElementById('telefonos_' + cliente_id).value;
    obj_direccion = document.getElementById('direccion_' + cliente_id).value;

    p_ci_nit = document.getElementById('ci_nit');
    p_apellidos = document.getElementById('apellidos');
    p_nombres = document.getElementById('nombres');
    p_telefonos = document.getElementById('telefonos');
    p_direccion = document.getElementById('direccion_evento');
    p_cliente_id = document.getElementById('cliente_id');

    p_ci_nit.value = obj_ci_nit;
    p_apellidos.value = obj_apellidos;
    p_nombres.value = obj_nombres;
    p_telefonos.value = obj_telefonos;
    p_direccion.value = obj_direccion;
    p_cliente_id.value = cliente_id;

    $("#div_clientes").fadeOut('slow');
}

//mostramos la lista de productos
function mostrarProductosVenta() {
    //verificamos las fechas
    const fecha_entrega = document.getElementById('fecha_entrega').value;
    const hora_entrega = document.getElementById('hora_entrega').value;
    const minuto_entrega = document.getElementById('minuto_entrega').value;
    const fecha_ini = parseInt(getFechaFormatoDB(fecha_entrega) + hora_entrega + minuto_entrega);

    const fecha_devolucion = document.getElementById('fecha_devolucion').value;
    const hora_devolucion = document.getElementById('hora_devolucion').value;
    const minuto_devolucion = document.getElementById('minuto_devolucion').value;
    const fecha_fin = parseInt(getFechaFormatoDB(fecha_devolucion) + hora_devolucion + minuto_devolucion);

    if (fecha_ini >= fecha_fin) {
        modalSetParameters('warning', 'center', 'Ventas!', 'La fecha de entrega no debe ser mayor a la fecha de devolucion', 'Cancelar', 'Volver');
        modalFunction.value = 'ventaWarning();';
        modalF.modal();
        return false;
    }
    else {
        $("#div_listap").fadeIn('slow');
        url_main = document.getElementById('url_main').value;
        token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
        ruta_imagen = url_empresa + '/static/img/pass/loading.gif';

        datos = {
            'module_x': document.forms['form_operation'].elements['module_x'].value,
            'operation_x': 'stock_productos',
            'fecha_entrega': fecha_entrega,
            'hora_entrega': hora_entrega,
            'minuto_entrega': minuto_entrega,
            'fecha_devolucion': fecha_devolucion,
            'hora_devolucion': hora_devolucion,
            'minuto_devolucion': minuto_devolucion,
            'csrfmiddlewaretoken': token,
        }

        const btn_s = document.getElementById('btn_stock');
        btn_s.disabled = true;

        imagen = '<img src="' + ruta_imagen + '">';
        listado = $("#div_cargar_stock");
        listado.fadeIn('slow');
        listado.html(imagen);
        listado.load(url_main, datos, function () {
            //termina de cargar la ventana
            terminaStockVenta();
        });
    }
}

function terminaStockVenta() {
    const btn_s = document.getElementById('btn_stock');
    btn_s.disabled = false;
    $("#div_cargar_stock").fadeOut('slow');
    $("#div_listap").fadeIn('slow');
    reiniciarProductosVenta();
}

function ocultarProductosVenta() {
    reiniciarProductosVenta();
    $("#div_listap").fadeOut('slow');
}

function reiniciarProductosVenta() {
    //reiniciamos la seleccion
    for (i = 1; i <= 50; i++) {
        producto = document.getElementById('producto_' + i);
        tb2 = document.getElementById('tb2_' + i);

        try {
            cantidad = document.getElementById('cantidad_' + i);
            cantidad.value = '';

            //costo
            costo = document.getElementById('costo_' + i);
            costo.value = '';

            //total
            total = document.getElementById('total_' + i);
            total.value = '';
        }
        catch (e) { }


        producto.value = "0";
        tb2.value = "";

        //ocultamos las filas
        if (i > 1) {
            fila = document.getElementById('fila_' + i);
            fila.style.display = 'none';
        }
    }//end for
    obj_total = document.getElementById('total_pedido');
    obj_total.value = '';

    obj_desc = document.getElementById('porcentaje_descuento');
    obj_porcentaje_desc = document.getElementById('descuento');
    obj_t_venta = document.getElementById('total_venta');
    obj_desc.value = '';
    obj_porcentaje_desc.value = '';
    obj_t_venta.value = '';
}

//acc, seleccion del producto
function seleccionPPreVenta(numero_registro, producto, id) {
    //verificamos que no repita productos
    for (i = 1; i <= 50; i++) {
        aux_p = document.getElementById('producto_' + i);
        if (parseInt(numero_registro) != i && aux_p.value == id) {
            //alert('ya selecciono este producto');
            tb2 = document.getElementById('tb2_' + numero_registro);
            //tb2.focus();
            tb2.value = '';
            modalSetParameters('warning', 'center', 'Ventas!', 'Ya selecciono este producto', 'Cancelar', 'Volver');
            modalFunction.value = 'ventaWarning();';
            modalF.modal();
            return false;
        }
    }

    //asignamos el id del producto
    obj_aux = document.getElementById("producto_" + numero_registro);
    obj_aux.value = id;

    //recuperamos el precio y el stock del producto
    const precio_producto = lista_productos_precios[id];
    const costo_pro = document.getElementById('costo_' + numero_registro);
    costo_pro.value = precio_producto;

    //stock
    const stock_pro = document.getElementById('pro_stock_' + id);
    const span_stock = document.getElementById('span_stock_producto_' + numero_registro);
    span_stock.innerHTML = stock_pro.value;
    if (parseInt(stock_pro.value) <= 0) {
        span_stock.className = "input_stock_red";
    }
    else {
        span_stock.className = "input_stock";
    }


    numero = parseInt(numero_registro);
    numero_int = numero + 1;
    if (numero_int <= 50) {
        numero_str = numero_int.toString();
        nombre_actual = "fila_" + numero_str;
        objeto_actual = document.getElementById(nombre_actual);
        objeto_actual.style.display = "block";
        objeto_actual.style.display = "";
    }
}

//acc
function validarFilaPreVenta(fila) {
    tb2 = document.getElementById("tb2_" + fila.toString());
    producto = document.getElementById("producto_" + fila.toString());

    tb2_val = Trim(tb2.value);
    pro_val = Trim(producto.value);

    //no selecciono ningun producto
    if (tb2_val == '') {
        producto.value = '0';
    }
    else {
        //escribio un producto, verificamos si selecciono
        if (pro_val == '0') {
            /*alert('Debe Seleccionar un Producto');
            tb2.value = '';
            tb2.focus();*/
        }
    }
}

//acc, total por producto
function totalPedidoPreVenta(origen) {
    total_pedido = 0;
    for (i = 1; i <= 50; i++) {
        try {
            p_id = document.getElementById('producto_' + i).value;
            if (p_id != '0') {
                cantidad = Trim(document.getElementById('cantidad_' + i).value);
                costo = Trim(document.getElementById('costo_' + i).value);
                if (cantidad != '' && costo != '') {
                    cantidad_valor = parseFloat(cantidad);
                    costo_valor = parseFloat(costo);
                    total = cantidad_valor * costo_valor;
                    total_pedido += total;
                    obj_total = document.getElementById('total_' + i);
                    obj_total.value = redondeo(total, 2);
                }
            }
        }
        catch (e) {
            console.log('sin filas');
        }
    }
    //console.log('antes error');
    obj_total_pedido = document.getElementById('total_pedido');
    //console.log('error');
    obj_total_pedido.value = redondeo(total_pedido, 2);

    if (origen !== 'descuento') {
        calcularPorcentajeDescuentoVenta();
    }

    //descuento
    t_final = total_pedido;
    descuento = Trim(document.getElementById('descuento').value);
    total_venta = document.getElementById('total_venta');
    if (descuento != '') {
        val_descuento = parseFloat(descuento);
        t_final = t_final - val_descuento;
        total_venta.value = redondeo((total_pedido - val_descuento), 2);
    }
    else {
        total_venta.value = redondeo(total_pedido, 2);
    }

    //costo transporte
    costo_transporte = Trim(document.getElementById('costo_transporte').value);
    if (costo_transporte == '') {
        costo_transporte = '0';
    }
    total_final = document.getElementById('total_final');
    total_final.value = redondeo((t_final + parseFloat(costo_transporte)), 2);
}

//acc, descuento en venta
function calcularPorcentajeDescuentoVenta() {
    porcentaje_descuento = Trim(document.getElementById('porcentaje_descuento').value);
    total_pedido2 = Trim(document.getElementById('total_pedido').value);

    descuento_obj = document.getElementById('descuento');

    if (total_pedido2 != '' && porcentaje_descuento != '') {
        resta_descuento = (parseFloat(porcentaje_descuento) / 100) * parseFloat(total_pedido2);
        descuento_obj.value = redondeo(resta_descuento, 2);
    }
    else {
        descuento_obj.value = '';
    }
}

function anularAumentoVenta(vaid) {
    const div_a = $('#div_motivo_anula_' + vaid);
    div_a.fadeIn('slow');
}

function anularAumentoVentaCancelar(vaid) {
    const div_a = $('#div_motivo_anula_' + vaid);
    div_a.fadeOut('slow');
}

function anularAumentoVentaConfirmar(vaid) {
    const motivo_anula = Trim(document.getElementById('motivo_anula_' + vaid).value);
    if (motivo_anula == '') {
        modalSetParameters('warning', 'center', 'Ventas!', 'debe llenar el motivo', 'Cancelar', 'Volver');
        modalFunction.value = 'ventaWarning();';
        modalF.modal();
    }
    else {


        document.forms['form_operation'].elements['motivo_anula'].value = motivo_anula;
        document.forms['form_operation'].elements['vaid'].value = vaid;
        document.forms['form_operation'].elements['operation_x2'].value = 'aumento_pedido_anular_x';
        modalSetParameters('danger', 'center', 'Ventas Aumentos!', 'esta seguro de anular este aumento?', 'Cancelar', 'Anular');
        modalFunction.value = 'anularAumentoVentaSend();';
        modalF.modal();
    }
}

function anularAumentoVentaSend() {
    modalF.modal('toggle');

    sendFormObject('form_operation', div_modulo);
}

function totalPedidoVueltaVenta() {
    const cantProductos = document.getElementById('cant_productos').value;
    let totalVuelta = 0;
    const totalFinal = document.getElementById('total_final');

    for (let i = 1; i <= cantProductos; i++) {
        const inpSalida = Trim(document.getElementById('salida_' + i).value);
        const inpVuelta = Trim(document.getElementById('vuelta_' + i).value);
        const inpRotura = Trim(document.getElementById('rotura_' + i).value);
        const inpRefaccion = Trim(document.getElementById('refaccion_' + i).value);
        const inpTotal = document.getElementById('total_' + i);
        //console.log('salida: ', inpSalida, ', vuelta: ', inpVuelta, ', rotura: ', inpRotura);
        if (inpVuelta != '' && inpRotura != '') {
            const resta = parseInt(inpSalida) - parseInt(inpVuelta);
            if (resta < 0) {
                document.getElementById('vuelta_' + i).value = '';
                modalSetParameters('warning', 'center', 'Ventas!', 'la cantidad de vuelta no puede ser mayor a la cantidad de salida', 'Cancelar', 'Volver');
                modalFunction.value = 'ventaWarning();';
                modalF.modal();
                return false;
            }
            let total = resta * parseFloat(inpRotura);
            if (inpRefaccion != '') {
                total = total + parseFloat(inpRefaccion);
            }
            totalVuelta += total;
            inpTotal.value = redondeo(total, 2);
        }
    }
    totalFinal.value = redondeo(totalVuelta, 2);
}

function verifyPasarVueltaVenta() {
    const cantProductos = document.getElementById('cant_productos').value;

    for (let i = 1; i <= cantProductos; i++) {
        const inpSalida = Trim(document.getElementById('salida_' + i).value);
        const inpVuelta = Trim(document.getElementById('vuelta_' + i).value);
        const inpRotura = Trim(document.getElementById('rotura_' + i).value);
        const inpRefaccion = Trim(document.getElementById('refaccion_' + i).value);
        const inpTotal = document.getElementById('total_' + i);

        if (inpVuelta != '' && inpRotura != '') {
            const resta = parseInt(inpSalida) - parseInt(inpVuelta);
            if (resta < 0) {
                return 'la cantidad de vuelta no puede ser mayor a la cantidad de salida';
            }
        }
        else {
            return 'Debe registrar cantidad de vuelta de todos los productos';
        }
    }
    return true;
}

//gastos
function anularGastoVenta(ce_id) {
    const div_a = $('#div_motivo_anula_' + ce_id);
    div_a.fadeIn('slow');
}

function anularGastoVentaCancelar(ce_id) {
    const div_a = $('#div_motivo_anula_' + ce_id);
    div_a.fadeOut('slow');
}

function anularGastoVentaConfirmar(ce_id) {
    const motivo_anula = Trim(document.getElementById('motivo_anula_' + ce_id).value);
    if (motivo_anula == '') {
        modalSetParameters('warning', 'center', 'Ventas!', 'debe llenar el motivo', 'Cancelar', 'Volver');
        modalFunction.value = 'ventaWarning();';
        modalF.modal();
    }
    else {
        document.forms['form_operation'].elements['motivo_anula'].value = motivo_anula;
        document.forms['form_operation'].elements['ce_id'].value = ce_id;
        document.forms['form_operation'].elements['operation_x2'].value = 'gastos_anular_x';
        modalSetParameters('danger', 'center', 'Gastos!', 'esta seguro de anular este gasto?', 'Cancelar', 'Anular');
        modalFunction.value = 'anularGastoVentaSend();';
        modalF.modal();
    }
}

function anularGastoVentaSend() {
    modalF.modal('toggle');

    sendFormObject('form_operation', div_modulo);
}

//cobros
function anularCobroVenta(ci_id) {
    const div_a = $('#div_motivo_anula_' + ci_id);
    div_a.fadeIn('slow');
}

function anularCobroVentaCancelar(ci_id) {
    const div_a = $('#div_motivo_anula_' + ci_id);
    div_a.fadeOut('slow');
}

function anularCobroVentaConfirmar(ci_id) {
    const motivo_anula = Trim(document.getElementById('motivo_anula_' + ci_id).value);
    if (motivo_anula == '') {
        modalSetParameters('warning', 'center', 'Ventas!', 'debe llenar el motivo', 'Cancelar', 'Volver');
        modalFunction.value = 'ventaWarning();';
        modalF.modal();
    }
    else {
        document.forms['form_operation'].elements['motivo_anula'].value = motivo_anula;
        document.forms['form_operation'].elements['ci_id'].value = ci_id;
        document.forms['form_operation'].elements['operation_x2'].value = 'cobros_anular_x';
        modalSetParameters('danger', 'center', 'Cobros!', 'esta seguro de anular este cobro?', 'Cancelar', 'Anular');
        modalFunction.value = 'anularCobroVentaSend();';
        modalF.modal();
    }
}

function anularCobroVentaSend() {
    modalF.modal('toggle');

    sendFormObject('form_operation', div_modulo);
}

//impresion de venta
function imprimirVenta(venta_id) {
    modalPrintFunctionB1.value = "imprimirVentaConCostos('" + venta_id + "');";
    modalPrintFunctionB2.value = "imprimirVentaSinCostos('" + venta_id + "');";
    modalPrintSetParameters('success', 'center', 'Ventas!', 'Imprimir Costos?', 'SI', 'NO');
    modalFPrint.modal();
}

function imprimirVentaConCostos(venta_id) {
    modalFPrint.modal('toggle');
    document.forms['form_print'].elements['id'].value = venta_id;
    document.forms['form_print'].elements['operation_x'].value = 'imprimir_con_costos';
    document.forms['form_print'].submit();
}

function imprimirVentaSinCostos(venta_id) {
    modalFPrint.modal('toggle');
    document.forms['form_print'].elements['id'].value = venta_id;
    document.forms['form_print'].elements['operation_x'].value = 'imprimir_sin_costos';
    document.forms['form_print'].submit();
}

//impresion de venta gasto
function imprimirVentaGasto(gasto_id) {
    document.forms['form_print'].elements['id'].value = gasto_id;
    document.forms['form_print'].submit();
}

//impresion de venta cobro
function imprimirVentaCobro(cobro_id) {
    document.forms['form_print'].elements['id'].value = cobro_id;
    document.forms['form_print'].submit();
}

//impresion de venta resumen
function imprimirVentaResumen(venta_id) {
    document.forms['form_print'].elements['id'].value = venta_id;
    document.forms['form_print'].elements['operation_x'].value = 'print_resumen';
    document.forms['form_print'].submit();
}
