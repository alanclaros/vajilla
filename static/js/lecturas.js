
function sendSearchLectura() {
    div_modulo = $("#div_block_content");
    sendFormObject('search', div_modulo);
}

function sendFormLectura(operation, message) {
    //modal function
    modalFunction = document.getElementById('modalFunctionSuccess');
    modalF = $('#modalForm');

    switch (operation) {
        case ('save'):
            resValidation = lecturaVerifyDepartamentos();
            if (resValidation === true) {
                modalFunction.value = 'lecturaSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Lecturas!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Lecturas!', resValidation, 'Cancelar', 'Volver');
                //function cancel
                modalFunction.value = 'lecturaWarning();';
                modalF.modal();
            }
            break;

        default:
            break;

        case ('periodo'):
            resValidation = lecturaVerifyPeriodo();
            if (resValidation === true) {
                //cantidad de cobros mensuales
                cant_cm_periodo = parseInt(document.forms['formulario_periodo'].elements['cantidad_cm_periodo'].value);
                if (cant_cm_periodo > 0) {
                    modalFunction.value = 'lecturaSaveFormPeriodo();';
                    //set data modal
                    modalSetParameters('warning', 'center', 'Lecturas!', 'Existe ' + cant_cm_periodo + ' departamentos con cobros realizados<br>Se asignara los cobros SOLO a los otros departamentos<br>Esta seguro de querer continuar?', 'Cancelar', 'Guardar');
                    modalF.modal();
                }
                else {
                    modalFunction.value = 'lecturaSaveFormPeriodo();';
                    //set data modal
                    modalSetParameters('success', 'center', 'Lecturas!', 'Se asignara estos cobros a todos los departamentos<br>Esta seguro de querer guardar estos datos para el periodo?', 'Cancelar', 'Guardar');
                    modalF.modal();
                }
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Lecturas!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'lecturaWarning();';
                modalF.modal();
            }
            break;
    }
}

function lecturaSaveForm() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.getElementById('add_btn_x').disabled = true;
    document.getElementById('add_btn_x2').disabled = true;

    sendFormObject('formulario', div_modulo);
}

function lecturaSaveFormPeriodo() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario_periodo'].elements['add_button'].disabled = true;

    sendFormObject('formulario_periodo', div_modulo);
}

function lecturaWarning() {
    modalF = $('#modalForm');
    modalF.modal('toggle');
}

function lecturaVerifyPeriodo() {
    cm_ids = Trim(document.forms['formulario_periodo'].elements['cobros_mensuales_ids'].value);
    if (cm_ids != '') {
        div_cm = cm_ids.split(';');
        for (ci = 0; ci < div_cm.length; ci++) {
            check_cm = document.getElementById('cobro_mensual_' + div_cm[ci]);
            monto_cobrar_cm = document.getElementById('monto_cobrar_' + div_cm[ci]);
            if (check_cm.checked) {
                if (Trim(monto_cobrar_cm.value) == '') {
                    return 'Debe llenar el monto a cobrar';
                }
            }
        }
    }

    return true;
}

//mostrando los cobros mensuales por departamento
function showCMD(div_id) {
    div_cm = document.getElementById(div_id);
    div_cm.style.display = '';
}

function closeCMD(div_id) {
    div_cm = document.getElementById(div_id);
    div_cm.style.display = 'none';
}

function showManuales(div_id) {
    div_cm = document.getElementById(div_id);
    div_cm.style.display = '';
}

function closeManuales(div_id) {
    div_cm = document.getElementById(div_id);
    div_cm.style.display = 'none';
}

//calculo consumo
function lecturaCalcularConsumo(dpid) {
    const costo_m3 = parseFloat(document.forms['formulario'].elements['costo_m3_' + dpid].value);
    const costo_minimo = parseFloat(document.forms['formulario'].elements['costo_minimo'].value);
    const unidad_minima_m3 = parseFloat(document.forms['formulario'].elements['unidad_minima_m3'].value);
    const obj_consumo = document.getElementById('consumo_' + dpid);

    if (Trim(document.getElementById('lectura_' + dpid).value) != '') {
        // console.log('costo_m3: ', costo_m3);
        // console.log('costo_minimo: ', costo_minimo);
        // console.log('unidad_minima_m3: ', unidad_minima_m3);

        const lectura_departamento = parseFloat(document.getElementById('lectura_' + dpid).value);
        const lectura_anterior = parseFloat(document.getElementById('lectura_anterior_' + dpid).value);
        const diferencia = (lectura_departamento - lectura_anterior);

        // console.log('lect dep: ', lectura_departamento);
        // console.log('lect ant: ', lectura_anterior);
        // console.log('diferencia: ', diferencia);

        let consumo = 0;
        if (diferencia <= unidad_minima_m3) {
            consumo = redondeo(costo_minimo, 2);
            //console.log('minimo');
        }
        else {
            //console.log('mayor: ', diferencia);
            const saldo = diferencia - unidad_minima_m3;
            consumo = costo_minimo + (saldo * costo_m3);
            consumo = redondeo(consumo, 2);
        }
        obj_consumo.value = consumo;
    }
    else {
        obj_consumo.value = '0';
    }
}

//cobros mensuales
function lecturaCheckMensual(dpid) {
    const cobros_mensuales_ids = document.forms['formulario'].elements['cobros_mensuales_ids'].value;
    const div_cobros = cobros_mensuales_ids.split(';');
    let total_mensuales = 0;

    for (let i = 0; i < div_cobros.length; i++) {
        const nombre_check = "me_chk_" + dpid + "_" + div_cobros[i];
        const obj_check = document.getElementById(nombre_check);
        if (obj_check) {
            if (obj_check.checked) {
                const nombre_val = 'me_val_' + dpid + '_' + div_cobros[i];
                const valor = parseFloat(document.getElementById(nombre_val).value);
                total_mensuales += valor;
            }
        }
    }
    const obj_total_me = document.getElementById('total_mensuales_' + dpid);
    obj_total_me.value = redondeo(total_mensuales, 2);
}

//cobros manuales
function lecturaCheckManual(dpid) {
    const cobros_manuales_ids = document.forms['formulario'].elements['cobros_manuales_ids'].value;
    const div_cobros = cobros_manuales_ids.split(';');
    let total_manuales = 0;

    for (let i = 0; i < div_cobros.length; i++) {
        const nombre_check = "ma_chk_" + dpid + "_" + div_cobros[i];
        const obj_check = document.getElementById(nombre_check);
        if (obj_check) {
            if (obj_check.checked) {
                const nombre_val = 'ma_val_' + dpid + '_' + div_cobros[i];
                const valor = parseFloat(document.getElementById(nombre_val).value);
                total_manuales += valor;
            }
        }
    }
    const obj_total_ma = document.getElementById('total_manuales_' + dpid);
    obj_total_ma.value = redondeo(total_manuales, 2);
}

//total cobros
function lecturaTotal(dpid) {
    const lectura_actual = Trim(document.getElementById('lectura_' + dpid).value);
    let suma_total = 0;
    if (lectura_actual != '') {
        const consumo = parseFloat(document.getElementById('consumo_' + dpid).value);
        const total_expensas = parseFloat(document.getElementById('total_expensas_' + dpid).value);
        const total_mensuales = parseFloat(document.getElementById('total_mensuales_' + dpid).value);
        const total_manuales = parseFloat(document.getElementById('total_manuales_' + dpid).value);
        suma_total = consumo + total_expensas + total_mensuales + total_manuales;
    }
    const obj_total = document.getElementById('monto_bs_' + dpid);
    obj_total.value = redondeo(suma_total, 2);
}

//lecturas de los departamentos
function lecturaVerifyDepartamentos() {
    const departamentos_ids = Trim(document.getElementById('departamentos_ids').value);
    if (departamentos_ids != '') {
        const div_dep = departamentos_ids.split(';');
        for (let i = 0; i < div_dep.length; i++) {
            const lectura_dep = Trim(document.getElementById('lectura_' + div_dep[i]).value);
            if (lectura_dep === '') {
                return 'Debe llenar todas las lecturas';
            }
        }
    }
    return true;
}