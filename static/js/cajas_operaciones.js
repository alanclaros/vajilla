
// //control especifico del modulo
// function controlModulo() {

// 	return true;
// }

//inicio de caja
function sendFormCajaIniciar(operation, message) {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	switch (operation) {
		case ('add'):
			modalFunction.value = 'cajaIniciarSaveForm();';
			//set data modal
			modalSetParameters('success', 'center', 'Cajas!', 'Esta seguro de iniciar esta Caja?', 'Cancelar', 'Guardar');
			modalF.modal();
			break;

		case ('delete'):
			modalFunction.value = 'cajaIniciarDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Cajas!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();
			break;

		default:
			break;
	}
}

function cajaIniciarSaveForm() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function cajaIniciarDelete() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

//recepcion de caja
function sendFormCajaIniciarRecibir(operation, message) {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	switch (operation) {
		case ('add'):
			modalFunction.value = 'cajaIniciarRecibirSaveForm();';
			//set data modal
			modalSetParameters('success', 'center', 'Cajas!', 'Esta seguro de recibir esta Caja?', 'Cancelar', 'Guardar');
			modalF.modal();
			break;

		case ('delete'):
			modalFunction.value = 'cajaIniciarRecibirDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Cajas!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();
			break;

		default:
			break;
	}
}

function cajaIniciarRecibirSaveForm() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function cajaIniciarRecibirDelete() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

//cierre de caja
function sendFormCajaCerrar(operation, message) {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	switch (operation) {
		case ('add'):
			modalFunction.value = 'cajaCerrarSaveForm();';
			//set data modal
			modalSetParameters('success', 'center', 'Cajas!', 'Esta seguro de cerrar esta Caja?', 'Cancelar', 'Guardar');
			modalF.modal();
			break;

		case ('delete'):
			modalFunction.value = 'cajaCerrarDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Cajas!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();
			break;

		default:
			break;
	}
}

function cajaCerrarSaveForm() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function cajaCerrarDelete() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

//cierre de caja recibir
function sendFormCajaCerrarRecibir(operation, message) {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	switch (operation) {
		case ('add'):
			modalFunction.value = 'cajaCerrarRecibirSaveForm();';
			//set data modal
			modalSetParameters('success', 'center', 'Cajas!', 'Esta seguro de cerrar esta Caja?', 'Cancelar', 'Guardar');
			modalF.modal();
			break;

		case ('delete'):
			modalFunction.value = 'cajaCerrarRecibirDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Cajas!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();
			break;

		default:
			break;
	}
}

function cajaCerrarRecibirSaveForm() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function cajaCerrarRecibirDelete() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

//validando monedas
function validarNumeroCO(nombre) {
	tipo = typeof (nombre);
	if (tipo == 'object') {
		campo = nombre;
	}
	if (tipo == "string") {
		campo = document.getElementById(nombre);
	}
	//alert(campo);
	var tam = campo.value.length;
	var valor = "";
	var letra = "";
	var nuevo_valor = "";
	for (i = 0; i < tam; i++) {
		valor = campo.value.substring(i, (i + 1));
		letra = valor.toUpperCase();
		if (letra == "1" || letra == "2" || letra == "3" || letra == "4" || letra == "5" || letra == "6" || letra == "7" || letra == "8" || letra == "9" || letra == "0" || letra == "-") {
			nuevo_valor = nuevo_valor + letra;
		}
	}
	campo.value = nuevo_valor;

	lista_monedas = document.getElementById('lista_monedas').value;
	div = lista_monedas.split('||');
	total = 0;
	for (i = 0; i < div.length; i++) {
		div2 = div[i].split('|');
		aux = 'moneda_' + div2[0];
		moneda = TrimDerecha(TrimIzquierda(document.getElementById(aux).value));
		if (moneda.length > 0) {
			total = total + (parseFloat(moneda) * parseFloat(div2[1]));
		}
	}

	//total
	objeto = document.getElementById('total');
	objeto.value = redondeo(total, 2);
}

// function mandarFormularioIniciar(operation, operation2, formulario, add_button, button_cancel) {
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

// 		for (mid = 1; mid <= 100; mid++) {
// 			try {
// 				fd.append('moneda_' + mid, document.getElementById('moneda_' + mid).value);
// 			}
// 			catch (e) {

// 			}
// 		}

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


// function mandarFormularioIniciarCancelar(operation, operation2, formulario, add_button, button_cancel) {
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

// 		for (mid = 1; mid <= 100; mid++) {
// 			try {
// 				fd.append('moneda_' + mid, document.getElementById('moneda_' + mid).value);
// 			}
// 			catch (e) {

// 			}
// 		}

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


// function mandarFormularioIniciarRecibir(operation, operation2, formulario, add_button, button_cancel) {
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

// 		for (mid = 1; mid <= 100; mid++) {
// 			try {
// 				fd.append('moneda_' + mid, document.getElementById('moneda_' + mid).value);
// 			}
// 			catch (e) {

// 			}
// 		}

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


// function mandarFormularioIniciarRecibirCancelar(operation, operation2, formulario, add_button, button_cancel) {
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

// 		for (mid = 1; mid <= 100; mid++) {
// 			try {
// 				fd.append('moneda_' + mid, document.getElementById('moneda_' + mid).value);
// 			}
// 			catch (e) {

// 			}
// 		}

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


// function mandarFormularioEntregar(operation, operation2, formulario, add_button, button_cancel) {
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

// 		for (mid = 1; mid <= 100; mid++) {
// 			try {
// 				fd.append('moneda_' + mid, document.getElementById('moneda_' + mid).value);
// 			}
// 			catch (e) {

// 			}
// 		}

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


// function mandarFormularioEntregarCancelar(operation, operation2, formulario, add_button, button_cancel) {
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

// 		for (mid = 1; mid <= 100; mid++) {
// 			try {
// 				fd.append('moneda_' + mid, document.getElementById('moneda_' + mid).value);
// 			}
// 			catch (e) {

// 			}
// 		}

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


// function mandarFormularioEntregarRecibir(operation, operation2, formulario, add_button, button_cancel) {
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

// 		for (mid = 1; mid <= 100; mid++) {
// 			try {
// 				fd.append('moneda_' + mid, document.getElementById('moneda_' + mid).value);
// 			}
// 			catch (e) {

// 			}
// 		}

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


// function mandarFormularioEntregarRecibirCancelar(operation, operation2, formulario, add_button, button_cancel) {
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

// 		for (mid = 1; mid <= 100; mid++) {
// 			try {
// 				fd.append('moneda_' + mid, document.getElementById('moneda_' + mid).value);
// 			}
// 			catch (e) {

// 			}
// 		}

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