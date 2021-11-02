function sendSearchCajaMovimiento() {
	div_modulo = $("#div_block_content");
	sendFormObject('search', div_modulo);
}

function sendFormCajaMovimiento(operation, message) {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'cajaMovimientoSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Cajas Movimientos!', 'Esta seguro de querer adicionar este movimiento?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Cajas Movimientos!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'cajaMovimientoWarning();';
				modalF.modal();
			}
			break;

		case ('anular'):
			resValidation = controlModuloCajaMovimiento();

			if (resValidation === true) {
				modalFunction.value = 'cajaMovimientoAnular();';
				//set data modal
				modalSetParameters('danger', 'center', 'Cajas Movimientos!', 'Esta seguro de querer anular ' + message + '?', 'Cancelar', 'Anular');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Cajas Movimientos!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'cajaMovimientoWarning();';
				modalF.modal();
			}
			break;

		default:
			break;
	}
}

function cajaMovimientoSaveForm() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function cajaMovimientoWarning() {
	modalF = $('#modalForm');
	modalF.modal('toggle');
}

function cajaMovimientoAnular() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

//control especifico del modulo
function controlModuloCajaMovimiento() {
	caja1 = document.getElementById('caja1');
	caja1_value = caja1.value;
	caja2 = document.getElementById('caja2');
	caja2_value = caja2.value;

	if (caja1_value == '0' || caja1_value == '') {
		return 'debe seleccionar una caja de origen';
	}

	if (caja2_value == '0') {
		return 'debe seleccionar una caja de destino';
	}

	operation = document.getElementById('operation_x').value;
	if (operation == 'anular' || operation == 'anular_guardar' || operation == 'anular_recepcion_guardar') {
		motivo = document.getElementById('motivo_anula');
		motivo_txt = Trim(motivo.value);
		if (motivo_txt == '') {
			return 'debe llenar el motivo';
		}
	}

	return true;
}

function cambiarSaldo() {
	caja1 = document.getElementById('caja1');
	caja1_valor = caja1.value;
	label_saldo = document.getElementById('lbl_saldo');

	lista_saldo = document.getElementById('lista_saldo_origen').value;
	if (lista_saldo.length > 0) {
		division = lista_saldo.split(";;");

		for (i = 0; i < division.length; i++) {
			div2 = division[i].split('|');
			if (caja1_valor == div2[0]) {
				label_saldo.innerHTML = div2[1];
			}
		}
	}
}

//caja movimiento recibe
function sendFormCajaMovimientoRecibe(operation, message) {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	switch (operation) {
		case ('add'):
			modalFunction.value = 'cajaMovimientoRecibeSaveForm();';
			//set data modal
			modalSetParameters('success', 'center', 'Cajas Movimientos!', 'Esta seguro de querer recibir este movimiento?', 'Cancelar', 'Recibir');
			modalF.modal();
			break;

		case ('anular'):
			resValidation = controlModuloCajaMovimiento();
			if (resValidation === true) {
				modalFunction.value = 'cajaMovimientoRecibeAnular();';
				//set data modal
				modalSetParameters('danger', 'center', 'Cajas Movimientos!', 'Esta seguro de querer anular ' + message + '?', 'Cancelar', 'Anular');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Cajas Movimientos!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'cajaMovimientoRecibeWarning();';
				modalF.modal();
			}
			break;

		default:
			break;
	}
}

function cajaMovimientoRecibeWarning() {
	modalF = $('#modalForm');
	modalF.modal('toggle');
}

function cajaMovimientoRecibeSaveForm() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function cajaMovimientoRecibeAnular() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}
