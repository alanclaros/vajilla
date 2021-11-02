
function sendSearchCliente() {
	div_modulo = $("#div_block_content");
	sendFormObject('search', div_modulo);
}

function sendFormCliente(operation, message) {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'clienteSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Clientes!', 'Esta seguro de querer adicionar este cliente?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Clientes!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'clienteWarning();';
				modalF.modal();
			}
			break;

		case ('modify'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'clienteSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Clientes!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Clientes!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'clienteWarning();';
				modalF.modal();
			}
			break;

		case ('delete'):
			modalFunction.value = 'clienteDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Clientes!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();

			break;

		default:
			break;
	}
}

function clienteSaveForm() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function clienteWarning() {
	modalF = $('#modalForm');
	modalF.modal('toggle');
}

function clienteDelete() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}