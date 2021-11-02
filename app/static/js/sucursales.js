
function sendSearchSucursal() {
	div_modulo = $("#div_block_content");
	sendFormObject('search', div_modulo);
}

function sendFormSucursal(operation, message) {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'sucursalSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Sucursales!', 'Esta seguro de querer adicionar esta sucursal?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Sucursales!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'sucursalWarning();';
				modalF.modal();
			}
			break;

		case ('modify'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'sucursalSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Sucursales!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Sucursales!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'sucursalWarning();';
				modalF.modal();
			}
			break;

		case ('delete'):
			modalFunction.value = 'sucursalDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Sucursales!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();

			break;

		default:
			break;
	}
}

function sucursalSaveForm() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function sucursalWarning() {
	modalF = $('#modalForm');
	modalF.modal('toggle');
}

function sucursalDelete() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}
