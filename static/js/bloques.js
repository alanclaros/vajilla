/************************************************************************************/
/************************************************************************************/
/****************Desarrollador, Programador: Alan Claros Camacho ********************/
/****************E-mail: alan_Claros13@hotmail.com **********************************/
/************************************************************************************/
/************************************************************************************/

function sendSearchBloque() {
	div_modulo = $("#div_block_content");
	sendFormObject('search', div_modulo);
}

function sendFormBloque(operation, message) {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'bloqueSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Bloques!', 'Esta seguro de querer adicionar este bloque?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Bloques!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'bloqueWarning();';
				modalF.modal();
			}
			break;

		case ('modify'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'bloqueSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Bloques!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Bloques!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'bloqueWarning();';
				modalF.modal();
			}
			break;

		case ('delete'):
			modalFunction.value = 'bloqueDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Bloques!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();

			break;

		default:
			break;
	}
}

function bloqueSaveForm() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function bloqueWarning() {
	modalF = $('#modalForm');
	modalF.modal('toggle');
}

function bloqueDelete() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}