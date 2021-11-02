
function sendSearchAsignarCM() {
    div_modulo = $("#div_block_content");
    sendFormObject('search', div_modulo);
}

function sendFormAsignarCM(operation, message) {
    //modal function
    modalFunction = document.getElementById('modalFunctionSuccess');
    modalF = $('#modalForm');

    switch (operation) {
        case ('save'):
            resValidation = asignarCMVerifyDepartamentos();
            if (resValidation === true) {
                modalFunction.value = 'asignarCMSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Asignar Cobros Manuales!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Asignar Cobros Manuales!', resValidation, 'Cancelar', 'Volver');
                //function cancel
                modalFunction.value = 'asignarCMWarning();';
                modalF.modal();
            }
            break;

        default:
            break;
    }
}

function asignarCMSaveForm() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.getElementById('add_btn_x').disabled = true;
    document.getElementById('add_btn_x2').disabled = true;

    sendFormObject('formulario', div_modulo);
}

function asignarCMWarning() {
    modalF = $('#modalForm');
    modalF.modal('toggle');
}

//lecturas de los departamentos
function asignarCMVerifyDepartamentos() {

    //const departamentos_ids = Trim(document.getElementById('departamentos_ids').value);

    // if (departamentos_ids != '') {
    //     const div_dep = departamentos_ids.split(';');
    //     for (let i = 0; i < div_dep.length; i++) {
    //         const lectura_dep = Trim(document.getElementById('lectura_' + div_dep[i]).value);
    //         if (lectura_dep === '') {
    //             return 'Debe llenar todas las lecturas';
    //         }
    //     }
    // }
    return true;
}

function acmTodosDepartamentos() {
    const check_dep = document.getElementById('mt_dep');
    const todos = document.getElementById('todos_departamentos');
    if (check_dep.checked) {
        todos.value = "1";
        const check_lista = document.getElementById('marcar_todo');
        check_lista.checked = true;
        acmListaDepartamentos();
    }
    else {
        todos.value = '0';
    }
}

function acmListaDepartamentos() {
    const check_lista = document.getElementById('marcar_todo');
    const deps_ids = Trim(document.getElementById('departamentos_ids').value);
    if (deps_ids != '') {
        const div_dep = deps_ids.split(';');
        for (let i = 0; i < div_dep.length; i++) {
            if (document.getElementById('chk_cobro_manual_' + div_dep[i])) {
                const obj_lista = document.getElementById('chk_cobro_manual_' + div_dep[i]);
                if (check_lista.checked) {
                    obj_lista.checked = true;
                }
                else {
                    obj_lista.checked = false;
                }
            }
        }
    }
}