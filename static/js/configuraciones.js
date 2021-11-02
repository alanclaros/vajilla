/************************************************************************************/
/************************************************************************************/
/****************Desarrollador, Programador: Alan Claros Camacho ********************/
/****************E-mail: alan_Claros13@hotmail.com **********************************/
/************************************************************************************/
/************************************************************************************/

function usarFechaServidor() {
	fechaServidor = document.getElementById('usar_fecha_servidor').value;
	campoFecha = document.getElementById('fecha_sistema');
	if (fechaServidor === 'si') {
		campoFecha.disabled = true;
	}
	else {
		campoFecha.disabled = false;
	}
}

//guardamos
function mandarFormularioConfiguracion() {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');
	resValidation = verifyForm();

	if (resValidation === true) {
		modalFunction.value = 'configuracionesSaveForm();';
		//set data modal
		modalSetParameters('success', 'center', 'Configuraciones!', 'Esta seguro de querer guardar los datos?', 'Cancelar', 'Guardar');
		modalF.modal();
	}
	else {
		//set data modal
		modalSetParameters('warning', 'center', 'Configuraciones!', resValidation, 'Cancelar', 'Volver');

		//function cancel
		modalFunction.value = 'configuracionesWarning(modalF);';
		modalF.modal();
	}
}

function configuracionesSaveForm() {
	modalF = $('#modalForm');
	modalF.modal('toggle');

	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	//document.forms[formulario].submit();
	token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;
	module_x = document.forms['form_operation'].elements['module_x'].value;
	operation = document.forms['form_operation'].elements['operation_x'].value;

	var fd = new FormData();
	fd.append('csrfmiddlewaretoken', token_operation);
	fd.append('module_x', module_x);
	fd.append('operation_x', operation);
	fd.append('id', document.forms['form_operation'].elements['id'].value);
	fd.append('cant_per_page', document.getElementById('cant_per_page').value);
	fd.append('cant_lista_cobranza', document.getElementById('cant_lista_cobranza').value);
	fd.append('usar_fecha_servidor', document.getElementById('usar_fecha_servidor').value);
	fd.append('fecha_sistema', document.getElementById('fecha_sistema').value);
	fd.append('costo_m3', document.getElementById('costo_m3').value);
	fd.append('costo_minimo', document.getElementById('costo_minimo').value);
	fd.append('unidad_minima_m3', document.getElementById('unidad_minima_m3').value);
	fd.append('expensas_monto_m2', document.getElementById('expensas_monto_m2').value);

	div_modulo.html(imagen_modulo);

	let para_cargar = url_empresa;
	if (para_cargar != '') {
		para_cargar = url_empresa + '/';
	}

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

function configuracionesWarning(modalF) {
	//modalF = $('#modalForm');

	modalF.modal('toggle');
}