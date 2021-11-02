
//control especifico del modulo
function sendSearchProducto() {
	div_modulo = $("#div_block_content");
	sendFormObject('search', div_modulo);
}

function sendFormProducto(operation, message) {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'productoSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Productos!', 'Esta seguro de querer adicionar este producto?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Productos!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'productoWarning();';
				modalF.modal();
			}
			break;

		case ('modify'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'productoSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Productos!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Productos!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'productoWarning();';
				modalF.modal();
			}
			break;

		case ('delete'):
			modalFunction.value = 'productoDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Productos!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();

			break;

		default:
			break;
	}
}

function productoSaveForm() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function productoWarning() {
	modalF = $('#modalForm');
	modalF.modal('toggle');
}

function productoDelete() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

//busqueda de productos relacionados
function buscarProductosRelacionados() {

	linea = Trim(document.getElementById('br_linea').value);
	producto = Trim(document.getElementById('br_producto').value);
	codigo = Trim(document.getElementById('br_codigo').value);

	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	url_main = document.getElementById('url_main').value;

	operation_mandar = document.forms['form_operation'].elements['operation_x'].value;
	pid = document.forms['form_operation'].elements['id'].value;

	datos_busqueda = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'operation_x': 'buscar_producto_relacionado',
		'linea': linea,
		'producto': producto,
		'codigo': codigo,
		'operation_mandar': operation_mandar,
		'pid': pid,
		'csrfmiddlewaretoken': token,
	}

	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	$("#div_busqueda_relacionados").html(imagen);
	$("#div_busqueda_relacionados").load(url_main, datos_busqueda, function () {
		//termina de cargar ajax
	});
}

//minimizar busqueda productos relacionados
function minimizarBusquedaRelacionado() {
	$("#div_busqueda_relacionados").html('<i>resultado busqueda</i>');
}

//selecionamos el producto relacionado
function seleccionarProductoRelacionado(producto_id) {
	producto_nombre = Trim(document.getElementById('productor_nombre_' + producto_id).value);

	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	url_main = document.getElementById('url_main').value;

	datos_producto = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'operation_x': 'producto_relacionado',
		'producto_id': producto_id,
		'producto': producto_nombre,
		'csrfmiddlewaretoken': token,
	}

	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	$("#lista_productos_relacionados").html(imagen);
	$("#lista_productos_relacionados").load(url_main, datos_producto, function () {
		//termina de cargar ajax
	});
}

//quitamos el producto del combo
function quitarProductoRelacionado(producto_relacionado_id) {
	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	url_main = document.getElementById('url_main').value;

	datos_quitar = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'operation_x': 'quitar_producto_relacionado',
		'producto_relacionado_id': producto_relacionado_id,
		'csrfmiddlewaretoken': token,
	}

	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	$("#lista_productos_relacionados").html(imagen);
	$("#lista_productos_relacionados").load(url_main, datos_quitar, function () {
		//termina de cargar ajax
	});
}

//cargamos imagen con ajax
function cargarImagen() {
	posicion = document.getElementById('posn_1');
	posicion_valor = Trim(posicion.value);

	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	valor_imagen = Trim(document.getElementById('imagen1').value);
	if (valor_imagen == '') {
		//alert('debe seleccionar una imagen');
		modalSetParameters('warning', 'center', 'Productos!', 'Debe seleccionar una imagen', 'Cancelar', 'Volver');
		modalFunction.value = 'productoWarning();';
		modalF.modal();
		return false;
	}

	if (posicion_valor == '') {
		//alert('Debe llenar la posicion');
		//posicion.focus();
		modalSetParameters('warning', 'center', 'Productos!', 'Debe llenar la posicion', 'Cancelar', 'Volver');
		modalFunction.value = 'productoWarning();';
		modalF.modal();
		return false;
	}

	//boton de la imagen
	boton_imagen = document.getElementById('btn_imagen');
	boton_imagen.disabled = true;

	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	url_main = document.getElementById('url_main').value;
	pid = document.getElementById('pid').value;
	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	module_x = document.forms['form_operation'].elements['module_x'].value;

	var fd = new FormData();
	//alert(fd);
	var files = $('#imagen1')[0].files[0];
	//alert(files);
	fd.append('imagen1', files);
	fd.append('module_x', module_x);
	//alert(fd);
	fd.append('operation_x', 'add_imagen');
	fd.append('csrfmiddlewaretoken', token);
	fd.append('pid', pid);
	fd.append('posicion', posicion_valor);

	$.ajax({
		url: url_main,
		type: 'post',
		data: fd,
		contentType: false,
		processData: false,
		success: function (response) {
			if (response != 0) {

				datos_imagen = {
					'module_x': module_x,
					'operation_x': 'lista_imagenes',
					'pid': pid,
					'csrfmiddlewaretoken': token,
				}

				$("#div_lista_imagenes").html(imagen);
				$("#div_lista_imagenes").load(url_main, datos_imagen, function () {
					//termina de cargar ajax
					boton_imagen.disabled = false;
				});
				//alert('cargado');
			} else {
				alert('no se pudo cargar la imagen, intentelo de nuevo');
				boton_imagen.disabled = false;
			}
		},
	});

}

//mostramos la imagen
function mostrarImagen(pid) {
	document.form_img.id.value = pid;
	document.form_img.submit();
}

//eliminar imagen
function eliminarImagen(pid) {
	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	url_main = document.getElementById('url_main').value;

	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	module_x = document.forms['form_operation'].elements['module_x'].value;

	datos_imagen = {
		'module_x': module_x,
		'operation_x': 'eliminar_imagen',
		'id': pid,
		'csrfmiddlewaretoken': token,
	}

	$("#div_lista_imagenes").html(imagen);
	$("#div_lista_imagenes").load(url_main, datos_imagen, function () {
		//termina de cargar ajax
		//boton_imagen.disabled = false;
	});

}

async function formularioImagenProducto(operation, operation2, formulario, add_button, button_cancel) {

	document.forms[formulario].elements[add_button].disabled = true;
	document.forms[formulario].elements[button_cancel].disabled = true;

	var fd = new FormData(document.forms['formulario']);

	//mostramos valores
	// for (var pair of fd.entries()) {
	// 	console.log(pair[0] + ', ' + pair[1]);
	// }

	div_modulo.html(imagen_modulo);

	let para_cargar = url_empresa;
	if (para_cargar != '') {
		para_cargar = url_empresa + '/';
	}

	let result;

	try {
		result = await $.ajax({
			url: para_cargar,
			method: 'POST',
			type: 'POST',
			cache: false,
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
			error: function (qXHR, textStatus, errorThrown) {
				console.log(errorThrown);
				console.log(qXHR);
				console.log(textStatus);
			},
		});
		//alert(result);
	}
	catch (e) {
		console.error(e);
	}
}
