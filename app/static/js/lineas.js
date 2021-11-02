
function mostrarImagenLinea(id) {
    document.form_img.id.value = id;
    document.form_img.submit();
}

function sendSearchLinea() {
    div_modulo = $("#div_block_content");
    sendFormObject('search', div_modulo);
}

function sendFormLinea(operation, message) {
    //modal function
    modalFunction = document.getElementById('modalFunctionSuccess');
    modalF = $('#modalForm');

    switch (operation) {
        case ('add'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'lineaSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Lineas!', 'Esta seguro de querer adicionar esta linea?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Lineas!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'lineaWarning();';
                modalF.modal();
            }
            break;

        case ('modify'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'lineaSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Lineas!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Lineas!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'lineaWarning();';
                modalF.modal();
            }
            break;

        case ('delete'):
            modalFunction.value = 'lineaDelete();';
            //set data modal
            modalSetParameters('danger', 'center', 'Lineas!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
            modalF.modal();

            break;

        default:
            break;
    }
}

function lineaSaveForm() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function lineaWarning() {
    modalF = $('#modalForm');
    modalF.modal('toggle');
}

function lineaDelete() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}