
function sendSearchPunto() {
	div_modulo = $("#div_block_content");
	sendFormObject('search', div_modulo);
}

function sendFormPunto(operation, message) {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'puntoSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Puntos!', 'Esta seguro de querer adicionar este Punto?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Puntos!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'puntoWarning();';
				modalF.modal();
			}
			break;

		case ('modify'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'puntoSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Puntos!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Puntos!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'puntoWarning();';
				modalF.modal();
			}
			break;

		case ('delete'):
			modalFunction.value = 'puntoDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Puntos!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();

			break;

		default:
			break;
	}
}

function puntoSaveForm() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function puntoWarning() {
	modalF = $('#modalForm');
	modalF.modal('toggle');
}

function puntoDelete() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}
