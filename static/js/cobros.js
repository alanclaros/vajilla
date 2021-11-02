
function sendSearchCobro() {
    div_modulo = $("#div_block_content");
    sendFormObject('search', div_modulo);
}

function sendFormCobro(operation, message) {
    //modal function
    modalFunction = document.getElementById('modalFunctionSuccess');
    modalF = $('#modalForm');

    switch (operation) {
        case ('save'):
            resValidation = cobroVerifyCobro();
            if (resValidation === true) {
                modalFunction.value = 'cobroSaveForm();';
                const monto_cobro = document.getElementById('total_cobro').value;
                //set data modal
                modalSetParameters('success', 'center', 'Cobros!', 'Esta seguro de querer cobrar ' + monto_cobro + ' bs.?', 'Cancelar', 'Cobrar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Cobros!', resValidation, 'Cancelar', 'Volver');
                //function cancel
                modalFunction.value = 'cobroWarning();';
                modalF.modal();
            }
            break;

        case ('anular'):
            resValidation = cobroVerifyAnular();
            if (resValidation === true) {
                const periodo_select = Trim(document.getElementById('periodo_seleccionado').value);
                const periodo_fecha_select = Trim(document.getElementById('periodo_fecha_seleccionado').value);
                document.forms['formulario_anular'].elements['id_anula'].value = periodo_select;

                modalFunction.value = 'cobroAnularForm();';
                //set data modal
                modalSetParameters('danger', 'center', 'Cobros!', '<p>Esta seguro de querer anular este cobro del ' + periodo_fecha_select + '?</p><br>Motivo : <input type="text" autocomplete="off" class="form-control input w-70 left" id="cobro_motivo_anula" placeholder="Motivo Anulacion" onkeyup="txtValid(this);" onblur="txtValid(this);">', 'Cancelar', 'Anular');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Cobros!', resValidation, 'Cancelar', 'Volver');
                //function cancel
                modalFunction.value = 'cobroWarning();';
                modalF.modal();
            }
            break;

        default:
            break;
    }
}

function cobroSaveForm() {
    modalF = $('#modalForm');
    div_modulo_periodo = $("#div_periodos");

    modalF.modal('toggle');
    sendFormObject('formulario', div_modulo_periodo);

    //send push
    const token_user = document.forms['form_notificaciones'].elements['csrfmiddlewaretoken'].value;
    const id_send = document.forms['formulario'].elements['user_id_dpto'].value;
    const pdepa_user = document.forms['formulario'].elements['departamento'].value;

    const head = 'Cobro Realizado';
    const body = 'Dpto: ' + pdepa_user + '\nSe registraron sus pagos mensuales ' + '\nPuede verificar sus recibos ingresando al sistema';

    //console.log('id send: ', id_send);
    //console.log('body: ', body);

    if (id_send != '' && id_send != '0') {
        const url_push = document.forms['form_notificaciones'].elements['url_webpush'].value;

        const datos_push = {
            'head': head,
            'body': body,
            'id': id_send,
            'csrfmiddlewaretoken': token_user,
        }

        $("#div_push_result").html('send push');
        $("#div_push_result").load(url_push, datos_push, function () {
            //alert('push enviado');
        });
    }
}

function cobroAnularForm() {
    const c_motivo_anula = document.getElementById('cobro_motivo_anula');
    if (Trim(c_motivo_anula.value) == '') {
        c_motivo_anula.placeholder = "Debe Llenar el motivo";
        c_motivo_anula.focus();
    }
    else {
        const form_m_anula = document.forms['formulario_anular'].elements['motivo_anula'];
        form_m_anula.value = Trim(c_motivo_anula.value);
        modalF = $('#modalForm');
        div_modulo_periodo = $("#div_periodos");

        modalF.modal('toggle');
        sendFormObject('formulario_anular', div_modulo_periodo);
    }
}

function cobroWarning() {
    modalF = $('#modalForm');
    modalF.modal('toggle');
}

//cobros
function cobroVerifyCobro() {
    const valor_cobrar = Trim(document.getElementById('total_cobro').value);
    if (valor_cobrar == '') {
        return 'Debe seleccionar periodos para cobrar';
    }
    const monto_cobrar = parseFloat(valor_cobrar);
    if (monto_cobrar <= 0) {
        return 'Debe cobrar un monto mayor a cero';
    }

    const cobros_ids = Trim(document.getElementById('lista_cobros_ids').value);
    if (cobros_ids == '') {
        return 'Debe seleccionar periodos';
    }

    const div_cob = cobros_ids.split(';');
    let cobros_mandar = '';
    for (let i = 0; i < div_cob.length; i++) {
        //si es un periodo pendiente de cobro y se marca el check
        if (document.getElementById('chk_periodo_' + div_cob[i])) {
            const chk_pe = document.getElementById('chk_periodo_' + div_cob[i]);
            if (chk_pe.checked) {
                cobros_mandar += div_cob[i] + ';';
            }
        }
    }

    if (cobros_mandar == '') {
        return 'Debe seleccionar periodos';
    }
    cobros_mandar = cobros_mandar.substring(0, cobros_mandar.length - 1);

    const para_cobrar = document.forms['formulario'].elements['cobros_cobrar'];
    para_cobrar.value = cobros_mandar;

    return true;
}

//cobros anular
function cobroVerifyAnular() {
    const per_select = Trim(document.getElementById('periodo_seleccionado').value);
    const per_fecha_select = Trim(document.getElementById('periodo_fecha_seleccionado').value);
    if (per_select == '' || per_fecha_select == '') {
        return 'Debe seleccionar un periodo';
    }

    return true;
}

//seleccionando la fila de los departamentos
function cobroSelectFila(fila, departamento, user_id_dpto) {
    const departamentos_ids = Trim(document.getElementById('departamentos_ids').value);
    if (departamentos_ids != '') {
        const div_dep = departamentos_ids.split(';');
        for (let i = 0; i < div_dep.length; i++) {
            const original = document.getElementById('backfila_' + div_dep[i]).value;
            const fila_dep = document.getElementById('fila_' + div_dep[i]);
            fila_dep.className = 'pointer back' + original;
        }
        //seleccionanmos la fila
        const fila_select = document.getElementById('fila_' + fila);
        fila_select.className = 'pointer ' + 'backpedido';

        //recuperamos stock del producto
        url_main = document.getElementById('url_main').value;
        token = document.forms['formulario_dep'].elements['csrfmiddlewaretoken'].value;
        module_x = document.forms['formulario_dep'].elements['module_x'].value;
        ruta_imagen = url_empresa + '/static/img/pass/loading.gif';

        datos = {
            'module_x': module_x,
            'operation_x': 'data_periodos',
            'id': fila,
            'csrfmiddlewaretoken': token,
        }

        //asignamos el departamento id para cuando se guarde el cobro
        const depa_id = document.forms['formulario'].elements['id'];
        depa_id.value = fila;
        //departamento para el web push
        const depa_nombre = document.forms['formulario'].elements['departamento'];
        depa_nombre.value = departamento;
        //user dpto
        const user_id_d = document.forms['formulario'].elements['user_id_dpto'];
        user_id_d.value = user_id_dpto;

        const depa_id_anula = document.forms['formulario_anular'].elements['id'];
        depa_id_anula.value = fila;

        imagen = '<img src="' + ruta_imagen + '">';
        fila = $("#div_periodos");

        fila.html(imagen);
        fila.load(url_main, datos, function () {
            //termina de cargar la ventana
        });
    }
}

//seleccionando periodo para ver los detalles
function cobroDetallePeriodo(fila, fecha_periodo) {
    const cobros_ids = Trim(document.getElementById('lista_cobros_ids').value);
    if (cobros_ids != '') {
        const div_cob = cobros_ids.split(';');
        for (let i = 0; i < div_cob.length; i++) {
            const original = document.getElementById('backfila_periodo_' + div_cob[i]).value;
            const fila_cob = document.getElementById('periodo_' + div_cob[i]);

            //si es un periodo pendiente de cobro y se marca el check
            if (document.getElementById('chk_periodo_' + div_cob[i])) {
                const chk_pe = document.getElementById('chk_periodo_' + div_cob[i]);
                if (chk_pe.checked) {
                    fila_cob.className = 'pointer backpedido';
                }
                else {
                    fila_cob.className = 'pointer back' + original;
                }
            }
            else {
                fila_cob.className = 'pointer back' + original;
            }
        }
        //seleccionanmos la fila
        const fila_select = document.getElementById('periodo_' + fila);
        if (fila_select.className == 'pointer backcobrado') {
            fila_select.className = 'pointer backcobrado_resaltar';
        }
        else {
            //verificamos el check
            const chk_periodo = document.getElementById('chk_periodo_' + fila);
            if (chk_periodo.checked) {
                fila_select.className = 'pointer ' + 'backpedido';
            }
        }

        //marcamos el periodo
        const pe_select = document.getElementById('periodo_seleccionado');
        //console.log('periodo select..: ', fila);
        pe_select.value = fila;
        const pe_fecha_select = document.getElementById('periodo_fecha_seleccionado');
        pe_fecha_select.value = fecha_periodo;

        //recuperamos detalle del periodo
        url_main = document.getElementById('url_main').value;
        token = document.forms['formulario_periodo'].elements['csrfmiddlewaretoken'].value;
        module_x = document.forms['formulario_dep'].elements['module_x'].value;
        ruta_imagen = url_empresa + '/static/img/pass/loading2.gif';

        datos = {
            'module_x': module_x,
            'operation_x': 'data_detalles',
            'id': fila,
            'csrfmiddlewaretoken': token,
        }

        imagen = '<img src="' + ruta_imagen + '">';
        fila = $("#div_detalles");

        fila.html(imagen);
        fila.load(url_main, datos, function () {
            //termina de cargar la ventana
        });
    }
}

function cobroCheckCobro() {
    const cobros_ids = Trim(document.getElementById('lista_cobros_ids').value);
    let total_cobro = 0;

    if (cobros_ids != '') {
        const div_cob = cobros_ids.split(';');
        for (let i = 0; i < div_cob.length; i++) {
            //si es un periodo pendiente de cobro y se marca el check
            if (document.getElementById('chk_periodo_' + div_cob[i])) {
                const chk_pe = document.getElementById('chk_periodo_' + div_cob[i]);
                if (chk_pe.checked) {
                    const monto_cobro = parseFloat(document.getElementById('monto_periodo_' + div_cob[i]).value);
                    total_cobro += monto_cobro;
                }
            }
        }
    }
    const total_deuda = document.getElementById('total_cobro');
    total_deuda.value = redondeo(total_cobro, 2);
}

function cobroCalcularCambio() {
    const dato_total = Trim(document.getElementById('total_cobro').value);
    const cambio = document.getElementById('cambio');
    const dato_efectivo = document.getElementById('efectivo');
    let monto_efectivo = 0;
    if (Trim(dato_efectivo.value) != '') {
        monto_efectivo = parseFloat(dato_efectivo.value);
    }

    if (dato_total != '') {
        const monto_total = parseFloat(dato_total);
        const monto_cambio = monto_efectivo - monto_total;
        cambio.value = redondeo(monto_cambio, 2);
    }
    else {
        cambio.value = efectivo.value;
    }
}

function cobroVerificarBotones(cobro_id) {
    let btn_imprimir = false;
    let btn_imprimir_todo = false;
    let btn_anular = false;
    let btn_cobrar = false;

    if (document.getElementById('btn_imprimir')) {
        btn_imprimir = document.getElementById('btn_imprimir');
        btn_imprimir.disabled = true;
    }
    if (document.getElementById('btn_imprimir_todo')) {
        btn_imprimir_todo = document.getElementById('btn_imprimir_todo');
        btn_imprimir_todo.disabled = true;
    }
    if (document.getElementById('btn_anular')) {
        btn_anular = document.getElementById('btn_anular');
        btn_anular.disabled = true;
    }
    if (document.getElementById('btn_cobrar')) {
        btn_cobrar = document.getElementById('btn_cobrar');
        btn_cobrar.disabled = true;
    }

    //estado del cobro
    const estado_cobro = document.getElementById('estado_cobro_' + cobro_id).value;
    if (estado_cobro == '1') { //pendiente
        if (btn_imprimir) {
            btn_imprimir.disabled = false;
        }

        if (btn_cobrar) {
            //verificamos tambien el monto a cobrar
            const tiene_caja_activa = document.getElementById('tiene_caja').value;
            if (tiene_caja_activa == '1') {
                const monto_cobrar = Trim(document.getElementById('total_cobro').value);
                let valor_cobro = 0;
                if (monto_cobrar != '') {
                    valor_cobro = parseFloat(monto_cobrar);
                    if (valor_cobro > 0) {
                        btn_cobrar.disabled = false;
                    }
                }
            }
        }
    }
    else {
        if (btn_imprimir) { btn_imprimir.disabled = false; }
        if (btn_imprimir_todo) { btn_imprimir_todo.disabled = false; }
        if (btn_anular) { btn_anular.disabled = false; }
    }
}

function cobroImprimir() {
    const pe_select = document.getElementById('periodo_seleccionado').value;

    form_print_id = document.forms['form_print'].elements['id'];
    form_print_operation = document.forms['form_print'].elements['operation_x'];

    form_print_id.value = pe_select;
    form_print_operation.value = 'imprimir_cobro';
    document.forms['form_print'].submit();
}