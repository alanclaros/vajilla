
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

//guardamos puntos almacenes
function guardarPuntosAlmacenes(formulario, add_button, button_cancel) {
	if (verifyForm()) {
		document.forms[formulario].elements[add_button].disabled = true;
		document.forms[formulario].elements[button_cancel].disabled = true;

		//document.forms[formulario].submit();
		token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;
		module_x = document.forms['form_operation'].elements['module_x'].value;
		module_x2 = document.forms['form_operation'].elements['module_x2'].value;

		var fd = new FormData();
		fd.append('csrfmiddlewaretoken', token_operation);
		fd.append('module_x', module_x);
		fd.append('module_x2', module_x2);
		fd.append('operation_x', 'puntos_almacenes')
		fd.append('operation_x2', 'modify_x')

		fd.append('id', document.forms['form_operation'].elements['id'].value);

		//almacenes ids
		almacenes_ids = document.forms['formulario'].elements['almacenes_ids'].value;
		div_almacenes = almacenes_ids.split('|');
		if (almacenes_ids != '') {
			for (ia = 0; ia < div_almacenes.length; ia++) {
				//alert(document.getElementById('almacen_' + div_almacenes[ia]).checked);
				if (document.getElementById('almacen_' + div_almacenes[ia]).checked) {
					fd.append('almacen_' + div_almacenes[ia], 1);
				}
			}
		}

		div_modulo.html(imagen_modulo);

		let para_cargar = url_empresa;
		if (para_cargar != '') {
			para_cargar = url_empresa + '/';
		}
		// div_modulo.load(para_cargar, datos_operation, function () {
		// 	//termina de cargar la ventana
		// });

		$.ajax({
			url: para_cargar,
			type: 'post',
			data: fd,
			contentType: false,
			processData: false,
			success: function (response) {
				if (response != 0) {
					div_modulo.html(response);
				} else {
					alert('error al realizar la operacion, intentelo de nuevo');
				}
			},
		});
	}
}
