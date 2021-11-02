
function sendSearchIA() {
	div_modulo = $("#div_block_content");
	sendFormObject('search', div_modulo);
}

function sendFormIA(operation, message) {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'IASaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Ingresos Almacen!', 'Esta seguro de querer adicionar este ingreso a Almacen?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Ingresos Almacen!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'IAWarning();';
				modalF.modal();
			}
			break;

		case ('anular'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'IAAnular();';
				//set data modal
				modalSetParameters('danger', 'center', 'Ingresos Almacen!', 'Esta seguro de querer anular ' + message + '?', 'Cancelar', 'Anular');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Ingresos Almacen!', resValidation, 'Cancelar', 'Volver');
				//function cancel
				modalFunction.value = 'IAWarning();';
				modalF.modal();
			}

			break;

		default:
			break;
	}
}

function IASaveForm() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function IAWarning() {
	modalF = $('#modalForm');
	modalF.modal('toggle');
}

function IAAnular() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function seleccionAlmacenIA() {
	//almacen
	almacen = document.getElementById('almacen');
	div_datos = $('#div_listap');
	if (almacen.value == '0') {
		div_datos.fadeOut('slow');
	}
	else {
		div_datos.fadeIn('slow');
	}
}

function seleccionPIA(numero_registro, producto, id) {
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	//verificamos que no repita productos
	for (i = 1; i <= 50; i++) {
		aux_p = document.getElementById('producto_' + i);
		if (parseInt(numero_registro) != i && aux_p.value == id) {
			//alert('ya selecciono este producto');
			tb2 = document.getElementById('tb2_' + numero_registro);
			tb2.focus();
			tb2.value = '';
			modalSetParameters('warning', 'center', 'Ingresos Almacen!', 'ya selecciono este producto', 'Cancelar', 'Volver');
			modalFunction.value = 'IAWarning();';
			modalF.modal();
			return false;
		}
	}

	//asignamos
	obj_aux = document.getElementById("producto_" + numero_registro);
	obj_aux.value = id;

	//alert(numero);alert(id);
	numero = parseInt(numero_registro);
	numero_int = numero + 1;
	if (numero_int <= 50) {
		numero_str = numero_int.toString();
		nombre_actual = "fila_" + numero_str;
		//alert(nombre_actual);
		objeto_actual = document.getElementById(nombre_actual);
		objeto_actual.style.display = "block";
		objeto_actual.style.display = "";
	}
}

//calculamos el total
function calcularTotalesIA() {
	limite = 50;

	total_todo = 0;

	for (i = 1; i <= limite; i++) {
		cantidad = document.getElementById("cantidad_" + i.toString());
		costo = document.getElementById("costo_" + i.toString());
		total = document.getElementById("total_" + i.toString());

		//valores
		cantidad_s = Trim(cantidad.value);
		costo_s = Trim(costo.value);

		if (cantidad_s != "" && costo_s != "") {
			total_v = parseFloat(cantidad_s) * parseFloat(costo_s);
			total_v2 = redondeo(total_v, 2);
			total_todo = total_todo + parseFloat(total_v2);
			total.value = total_v2;
		}
	}

	obj_total = document.getElementById('total');
	obj_total.value = redondeo(total_todo, 2);
}


function validarFilaIA(fila) {
	cantidad = document.getElementById("cantidad_" + fila.toString());
	costo = document.getElementById("costo_" + fila.toString());
	total = document.getElementById("total_" + fila.toString());
	tb2 = document.getElementById("tb2_" + fila.toString());
	producto = document.getElementById("producto_" + fila.toString());

	cant_val = Trim(cantidad.value);
	costo_val = Trim(costo.value);
	tb2_val = Trim(tb2.value);
	pro_val = Trim(producto.value);

	//no selecciono ningun producto
	if (tb2_val == '') {
		cantidad.value = '';
		costo.value = '';
		total.value = '';
		producto.value = '0';
	}
	else {
		//escribio un producto, verificamos si selecciono
		if (pro_val == '0') {
			//alert('Debe Seleccionar un Producto');
			cantidad.value = '';
			costo.value = '';
			total.value = '';
		}
	}
}
