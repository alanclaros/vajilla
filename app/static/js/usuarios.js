
function sendSearchUsuario() {
	div_modulo = $("#div_block_content");
	sendFormObject('search', div_modulo);
}

function sendFormUsuario(operation, message) {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				resControlModulo = controlModuloUsuario();
				if (resControlModulo === true) {
					modalFunction.value = 'usuarioSaveForm();';
					//set data modal
					modalSetParameters('success', 'center', 'Usuarios!', 'Esta seguro de querer adicionar este Usuario?', 'Cancelar', 'Guardar');
					modalF.modal();
				}
				else {
					//set data modal
					modalSetParameters('warning', 'center', 'Usuarios!', resControlModulo, 'Cancelar', 'Volver');
					//function cancel
					modalFunction.value = 'usuarioWarning();';
					modalF.modal();
				}
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Usuarios!', resValidation, 'Cancelar', 'Volver');
				//function cancel
				modalFunction.value = 'usuarioWarning();';
				modalF.modal();
			}
			break;

		case ('modify'):
			resValidation = verifyForm();
			if (resValidation === true) {
				resControlModulo = controlModuloUsuario();
				if (resControlModulo === true) {
					modalFunction.value = 'usuarioSaveForm();';
					//set data modal
					modalSetParameters('success', 'center', 'Usuarios!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
					modalF.modal();
				}
				else {
					//set data modal
					modalSetParameters('warning', 'center', 'Usuarios!', resControlModulo, 'Cancelar', 'Volver');
					//function cancel
					modalFunction.value = 'usuarioWarning();';
					modalF.modal();
				}
				// modalFunction.value = 'usuarioSaveForm();';
				// //set data modal
				// modalSetParameters('success', 'center', 'Usuarios!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
				// modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Usuarios!', resValidation, 'Cancelar', 'Volver');
				//function cancel
				modalFunction.value = 'usuarioWarning();';
				modalF.modal();
			}
			break;

		case ('delete'):
			modalFunction.value = 'usuarioDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Usuarios!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();

			break;

		default:
			break;
	}
}

function usuarioSaveForm() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function usuarioWarning() {
	modalF = $('#modalForm');
	modalF.modal('toggle');
}

function usuarioDelete() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}


//control especifico del modulo
function controlModuloUsuario() {
	metodo = document.getElementById("metodo").value;
	if (metodo == "add") {
		up = document.getElementById("password");
		user_password = TrimDerecha(TrimIzquierda(up.value));
		if (user_password == "") {
			//alert("Debe llenar este campo");
			//up.focus();
			return 'Debe llenar el password';
		}
	}
	if (metodo == "modify") {
		up = document.getElementById("password");
		cambiar = document.getElementById("cambiar").value;
		if (cambiar == "yes") {
			user_password = TrimDerecha(TrimIzquierda(up.value));
			if (user_password == "") {
				// alert("Debe llenar este campo");
				// up.focus();
				// return false;
				return 'Debe Llenar el nuevo password';
			}
		}
	}
	return true;
}

function deshabilitar(valor) {
	if (valor.value == "yes") {
		document.formulario.password.disabled = false;
		document.formulario.password.focus();
	}
	else {
		document.formulario.password.disabled = true;
	}
}

// function sendSearchUser() {
// 	token_search = document.forms['search'].elements['csrfmiddlewaretoken'].value;

// 	datos_search = {
// 		'module_x': document.forms['form_operation'].elements['module_x'].value,
// 		'csrfmiddlewaretoken': token_search,
// 		'search_button_x': 'acc',
// 	}
// 	datos_search['search_nombres'] = document.getElementById('search_nombres').value;
// 	datos_search['search_apellidos'] = document.getElementById('search_apellidos').value;
// 	datos_search['search_username'] = document.getElementById('search_username').value;

// 	div_modulo.html(imagen_modulo);
// 	div_modulo.load('/', datos_search, function () {
// 		//termina de cargar la ventana
// 	});
// }

// function mandarFormularioUser(operation, operation2, formulario, add_button, button_cancel) {
// 	if (verifyForm()) {
// 		document.forms[formulario].elements[add_button].disabled = true;
// 		document.forms[formulario].elements[button_cancel].disabled = true;

// 		//document.forms[formulario].submit();
// 		token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;

// 		datos_operation = {
// 			'module_x': document.forms['form_operation'].elements['module_x'].value,
// 			'csrfmiddlewaretoken': token_operation,
// 			'operation_x': operation,
// 		}
// 		//guardamos, modificamos o eliminamos datos
// 		datos_operation[operation2] = 'acc';
// 		datos_operation['id'] = document.forms['form_operation'].elements['id'].value;

// 		datos_operation['perfil'] = document.getElementById('perfil').value;
// 		datos_operation['notificacion'] = document.getElementById('notificacion').value;
// 		datos_operation['punto'] = document.getElementById('punto').value;
// 		datos_operation['caja'] = document.getElementById('caja').value;
// 		datos_operation['first_name'] = document.getElementById('first_name').value;
// 		datos_operation['last_name'] = document.getElementById('last_name').value;
// 		datos_operation['username'] = document.getElementById('username').value;
// 		datos_operation['password'] = document.getElementById('password').value;
// 		try {
// 			datos_operation['cambiar'] = document.getElementById('cambiar').value;
// 		}
// 		catch (e) {
// 			datos_operation['cambiar'] = 'no';
// 		}
// 		datos_operation['email'] = document.getElementById('email').value;
// 		try {
// 			datos_operation['activo'] = document.getElementById('activo').checked ? 1 : 0;
// 		}
// 		catch (e) {
// 			datos_operation['activo'] = 1;
// 		}
// 		for (i = 1; i <= 100; i++) {
// 			try {
// 				nombre = "modulo_" + i;
// 				aux = document.getElementById(nombre);
// 				datos_operation[nombre] = aux.checked ? 1 : 0;

// 				//adicion
// 				try {
// 					nombre2 = "modulo_" + i + "_ad";
// 					aux2 = document.getElementById(nombre2);
// 					datos_operation[nombre2] = aux2.checked ? 1 : 0;
// 				}
// 				catch (e) {

// 				}

// 				//modificacion
// 				try {
// 					nombre2 = "modulo_" + i + "_mo";
// 					aux2 = document.getElementById(nombre2);
// 					datos_operation[nombre2] = aux2.checked ? 1 : 0;
// 				}
// 				catch (e) {

// 				}

// 				//eliminacion
// 				try {
// 					nombre2 = "modulo_" + i + "_el";
// 					aux2 = document.getElementById(nombre2);
// 					datos_operation[nombre2] = aux2.checked ? 1 : 0;
// 				}
// 				catch (e) {

// 				}

// 				//anular
// 				try {
// 					nombre2 = "modulo_" + i + "_an";
// 					aux2 = document.getElementById(nombre2);
// 					datos_operation[nombre2] = aux2.checked ? 1 : 0;
// 				}
// 				catch (e) {

// 				}

// 				//imprimir
// 				try {
// 					nombre2 = "modulo_" + i + "_im";
// 					aux2 = document.getElementById(nombre2);
// 					datos_operation[nombre2] = aux2.checked ? 1 : 0;
// 				}
// 				catch (e) {

// 				}

// 				//permiso
// 				try {
// 					nombre2 = "modulo_" + i + "_pe";
// 					aux2 = document.getElementById(nombre2);
// 					datos_operation[nombre2] = aux2.checked ? 1 : 0;
// 				}
// 				catch (e) {

// 				}
// 			}
// 			catch (e) {

// 			}
// 		}

// 		// for (var key in datos_operation) {
// 		// 	if (datos_operation.hasOwnProperty(key)) {
// 		// 		console.log(key, datos_operation[key]);
// 		// 	}
// 		// }

// 		div_modulo.html(imagen_modulo);
// 		div_modulo.load('/', datos_operation, function () {
// 			//termina de cargar la ventana
// 		});
// 	}
// }

// function confirmarEliminarUser() {
// 	if (confirm('Esta seguro de querer eliminar este usuario?')) {
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

// 		datos_operation['username'] = document.getElementById('username').value;

// 		div_modulo.html(imagen_modulo);
// 		div_modulo.load('/', datos_operation, function () {
// 			//termina de cargar la ventana
// 		});
// 	}
// }