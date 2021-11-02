
function sendSearchCobroMensual() {
    div_modulo = $("#div_block_content");
    sendFormObject('search', div_modulo);
}

function sendFormCobroMensual(operation, message) {
    //modal function
    modalFunction = document.getElementById('modalFunctionSuccess');
    modalF = $('#modalForm');

    switch (operation) {
        case ('add'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'cobroMensualSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Cobros Mensuales!', 'Esta seguro de querer adicionar este cobro mensual?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Cobros Mensuales!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'cobroMensualWarning();';
                modalF.modal();
            }
            break;

        case ('modify'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'cobroMensualSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Cobros Mensuales!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Cobros Mensuales!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'cobroMensualWarning();';
                modalF.modal();
            }
            break;

        case ('delete'):
            modalFunction.value = 'cobroMensualDelete();';
            //set data modal
            modalSetParameters('danger', 'center', 'Cobros Mensuales!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
            modalF.modal();

            break;

        default:
            break;
    }
}

function cobroMensualSaveForm() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function cobroMensualWarning() {
    modalF = $('#modalForm');
    modalF.modal('toggle');
}

function cobroMensualDelete() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function cmCalcularMontoCobrar() {
    const monto_bol = Trim(document.getElementById('monto_bs').value);
    const span_monto_dividido = document.getElementById('span_monto_dividido');
    const span_numero_departamentos = document.getElementById('span_numero_departamentos');

    if (monto_bol == '') {
        span_monto_dividido.innerHTML = '0';
    }
    else {
        const numero_departamentos = parseInt(span_numero_departamentos.innerHTML);
        if (numero_departamentos > 0) {
            const newMonto = redondeo(parseFloat(monto_bol) / numero_departamentos, 2);
            span_monto_dividido.innerHTML = newMonto;
        }
        else {
            span_monto_dividido.innerHTML = '0';
        }
    }
}