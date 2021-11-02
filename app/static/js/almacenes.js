
function sendSearchAlmacen() {
	div_modulo = $("#div_block_content");
	sendFormObject('search', div_modulo);
}

function sendFormAlmacen(operation, message) {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'almacenSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Almacenes!', 'Esta seguro de querer adicionar este almacen?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Almacenes!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'almacenWarning();';
				modalF.modal();
			}
			break;

		case ('modify'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'almacenSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Almacenes!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Almacenes!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'almacenWarning();';
				modalF.modal();
			}
			break;

		case ('delete'):
			modalFunction.value = 'almacenDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Almacenes!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();

			break;

		default:
			break;
	}
}

function almacenSaveForm() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function almacenWarning() {
	modalF = $('#modalForm');
	modalF.modal('toggle');
}

function almacenDelete() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}
