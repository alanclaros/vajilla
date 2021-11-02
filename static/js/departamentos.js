
function sendSearchDepartamento() {
    div_modulo = $("#div_block_content");
    sendFormObject('search', div_modulo);
}

function sendFormDepartamento(operation, message) {
    //modal function
    modalFunction = document.getElementById('modalFunctionSuccess');
    modalF = $('#modalForm');

    switch (operation) {
        case ('add'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'departamentoSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Departamentos!', 'Esta seguro de querer adicionar este departamento?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Departamentos!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'departamentoWarning();';
                modalF.modal();
            }
            break;

        case ('modify'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'departamentoSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Departamentos!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Departamentos!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'departamentoWarning();';
                modalF.modal();
            }
            break;

        case ('delete'):
            modalFunction.value = 'departamentoDelete();';
            //set data modal
            modalSetParameters('danger', 'center', 'Departamentos!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
            modalF.modal();

            break;

        default:
            break;
    }
}

function departamentoSaveForm() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function departamentoWarning() {
    modalF = $('#modalForm');
    modalF.modal('toggle');
}

function departamentoDelete() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}
