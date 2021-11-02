
function sendSearchPiso() {
    div_modulo = $("#div_block_content");
    sendFormObject('search', div_modulo);
}

function sendFormPiso(operation, message) {
    //modal function
    modalFunction = document.getElementById('modalFunctionSuccess');
    modalF = $('#modalForm');

    switch (operation) {
        case ('add'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'pisoSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Pisos!', 'Esta seguro de querer adicionar este piso?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Pisos!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'pisoWarning();';
                modalF.modal();
            }
            break;

        case ('modify'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'pisoSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Pisos!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Pisos!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'pisoWarning();';
                modalF.modal();
            }
            break;

        case ('delete'):
            modalFunction.value = 'pisoDelete();';
            //set data modal
            modalSetParameters('danger', 'center', 'Pisos!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
            modalF.modal();

            break;

        default:
            break;
    }
}

function pisoSaveForm() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function pisoWarning() {
    modalF = $('#modalForm');
    modalF.modal('toggle');
}

function pisoDelete() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}