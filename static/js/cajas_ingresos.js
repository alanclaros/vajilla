
function sendSearchCajaIngreso() {
	div_modulo = $("#div_block_content");
	sendFormObject('search', div_modulo);
}

function sendFormCajaIngreso(operation, message) {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'cajaIngresoSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Cajas Ingresos!', 'Esta seguro de querer adicionar este ingreso?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Cajas Ingresos!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'cajaIngresoWarning();';
				modalF.modal();
			}
			break;

		// case ('modify'):
		// 	resValidation = verifyForm();
		// 	if (resValidation === true) {
		// 		modalFunction.value = 'cajaIngresoSaveForm();';
		// 		//set data modal
		// 		modalSetParameters('success', 'center', 'Cajas Ingresos!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
		// 		modalF.modal();
		// 	}
		// 	else {
		// 		//set data modal
		// 		modalSetParameters('warning', 'center', 'Cajas Ingresos!', resValidation, 'Cancelar', 'Volver');

		// 		//function cancel
		// 		modalFunction.value = 'cajaIngresoWarning();';
		// 		modalF.modal();
		// 	}
		// 	break;

		case ('anular'):
			resValidation = controlModuloIngresoCaja();
			console.log('resvalidation: ', resValidation);

			if (resValidation === true) {
				modalFunction.value = 'cajaIngresoAnular();';
				//set data modal
				modalSetParameters('danger', 'center', 'Cajas Ingresos!', 'Esta seguro de querer anular ' + message + '?', 'Cancelar', 'Anular');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Cajas Ingresos!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'cajaIngresoWarning();';
				modalF.modal();
			}
			break;

		default:
			break;
	}
}

function cajaIngresoSaveForm() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function cajaIngresoWarning() {
	modalF = $('#modalForm');
	modalF.modal('toggle');
}

function cajaIngresoAnular() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

//control especifico del modulo
function controlModuloIngresoCaja() {
	operation = document.getElementById('operation_x').value;
	if (operation == 'anular') {
		motivo = document.getElementById('motivo_anula');
		motivo_txt = Trim(motivo.value);
		if (motivo_txt == '') {
			return 'Debe llenar el motivo de anulacion';
		}
	}

	return true;
}

// function sendSearchCajaIngreso() {
// 	token_search = document.forms['search'].elements['csrfmiddlewaretoken'].value;

// 	datos_search = {
// 		'module_x': document.forms['form_operation'].elements['module_x'].value,
// 		'csrfmiddlewaretoken': token_search,
// 		'search_button_x': 'acc',
// 	}
// 	datos_search['search_fecha_ini'] = document.getElementById('search_fecha_ini').value;
// 	datos_search['search_fecha_fin'] = document.getElementById('search_fecha_fin').value;
// 	datos_search['search_caja'] = document.getElementById('search_caja').value;
// 	datos_search['search_concepto'] = document.getElementById('search_concepto').value;

// 	div_modulo.html(imagen_modulo);
// 	div_modulo.load('/', datos_search, function () {
// 		//termina de cargar la ventana
// 	});
// }


// function mandarFormularioCajaIngreso(operation, operation2, formulario, add_button, button_cancel) {
// 	if (verifyForm()) {
// 		document.forms[formulario].elements[add_button].disabled = true;
// 		document.forms[formulario].elements[button_cancel].disabled = true;

// 		//document.forms[formulario].submit();
// 		token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;
// 		module_x = document.forms['form_operation'].elements['module_x'].value;

// 		var fd = new FormData();
// 		fd.append('csrfmiddlewaretoken', token_operation);
// 		fd.append('module_x', module_x);
// 		fd.append('operation_x', operation);
// 		fd.append('id', document.forms['form_operation'].elements['id'].value);

// 		fd.append(operation2, 'acc');

// 		fd.append('caja', document.getElementById('caja').value);
// 		fd.append('monto', document.getElementById('monto').value);
// 		fd.append('fecha', document.getElementById('fecha').value);
// 		fd.append('concepto', document.getElementById('concepto').value);

// 		div_modulo.html(imagen_modulo);

// 		$.ajax({
// 			url: '/',
// 			type: 'post',
// 			data: fd,
// 			contentType: false,
// 			processData: false,
// 			success: function (response) {
// 				if (response != 0) {
// 					div_modulo.html(response);
// 				} else {
// 					alert('error al realizar la operacion, intentelo de nuevo');
// 				}
// 			},
// 		});
// 	}
// }

// function confirmarAnularCajaIngreso() {
// 	if (Trim(document.getElementById('motivo_anula').value) == '') {
// 		alert('Debe llenar el motivo');
// 		document.getElementById('motivo_anula').focus();
// 		return false;
// 	}

// 	if (confirm('Esta seguro de querer anular este ingreso?')) {
// 		token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;

// 		document.forms['formulario'].elements['add_button'].disabled = true;
// 		document.forms['formulario'].elements['button_cancel'].disabled = true;

// 		datos_operation = {
// 			'module_x': document.forms['form_operation'].elements['module_x'].value,
// 			'csrfmiddlewaretoken': token_operation,
// 			'operation_x': 'delete',
// 			'delete_x': 'acc',
// 		}
// 		datos_operation['id'] = document.forms['form_operation'].elements['id'].value;
// 		datos_operation['concepto'] = document.getElementById('concepto').value;
// 		datos_operation['motivo_anula'] = document.getElementById('motivo_anula').value;

// 		div_modulo.html(imagen_modulo);
// 		div_modulo.load('/', datos_operation, function () {
// 			//termina de cargar la ventana
// 		});
// 	}
// }