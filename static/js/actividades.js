
function sendSearchActividad() {
    div_modulo = $("#div_block_content");
    sendFormObject('search', div_modulo);
}

function sendFormActividad(operation, message) {
    //modal function
    modalFunction = document.getElementById('modalFunctionSuccess');
    modalF = $('#modalForm');

    switch (operation) {
        case ('add'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'actividadSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Actividades!', 'Esta seguro de querer adicionar esta actividad?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Actividades!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'actividadWarning();';
                modalF.modal();
            }
            break;

        case ('modify'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'actividadSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Actividades!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Actividades!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'actividadWarning();';
                modalF.modal();
            }
            break;

        case ('delete'):
            modalFunction.value = 'actividadDelete();';
            //set data modal
            modalSetParameters('danger', 'center', 'Actividades!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
            modalF.modal();

            break;

        default:
            break;
    }
}

function actividadSaveForm() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function actividadWarning() {
    modalF = $('#modalForm');
    modalF.modal('toggle');
}

function actividadDelete() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}