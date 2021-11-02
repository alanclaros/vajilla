
function sendSearchCobroManual() {
    div_modulo = $("#div_block_content");
    sendFormObject('search', div_modulo);
}

function sendFormCobroManual(operation, message) {
    //modal function
    modalFunction = document.getElementById('modalFunctionSuccess');
    modalF = $('#modalForm');

    switch (operation) {
        case ('add'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'cobroManualSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Cobros Manuales!', 'Esta seguro de querer adicionar este cobro Manual?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Cobros Manuales!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'cobroManualWarning();';
                modalF.modal();
            }
            break;

        case ('modify'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'cobroManualSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Cobros Manuales!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Cobros Manuales!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'cobroManualWarning();';
                modalF.modal();
            }
            break;

        case ('delete'):
            modalFunction.value = 'cobroManualDelete();';
            //set data modal
            modalSetParameters('danger', 'center', 'Cobros Manuales!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
            modalF.modal();

            break;

        default:
            break;
    }
}

function cobroManualSaveForm() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function cobroManualWarning() {
    modalF = $('#modalForm');
    modalF.modal('toggle');
}

function cobroManualDelete() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function cManMontoPorcentaje() {
    monto_porcentaje = document.getElementById('monto_porcentaje').value;
    //console.log('monto porcentaje: ', monto_porcentaje);
    monto_bs = document.getElementById('monto_bs');
    porcentaje = document.getElementById('porcentaje');
    if (monto_porcentaje == 'monto') {
        monto_bs.value = '';
        monto_bs.readOnly = false;
        porcentaje.value = '0';
        porcentaje.readOnly = true;
        porcentaje.readOnly = 'readonly';
    }
    else {
        monto_bs.value = '0';
        monto_bs.readOnly = true;
        monto_bs.readOnly = 'readonly';
        porcentaje.value = '';
        porcentaje.readOnly = false;
    }
}