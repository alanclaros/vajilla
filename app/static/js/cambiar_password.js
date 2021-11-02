/************************************************************************************/
/************************************************************************************/
/****************Desarrollador, Programador: Alan Claros Camacho ********************/
/****************E-mail: alan_Claros13@hotmail.com **********************************/
/************************************************************************************/
/************************************************************************************/

async function cambiarPassword() {
	actual = document.getElementById('actual');
	nuevo = document.getElementById('nuevo');
	nuevo2 = document.getElementById('nuevo2');

	if (Trim(actual.value) == '') {
		alert('debe llenar su password');
		actual.focus();
		return false;
	}

	if (Trim(nuevo.value) == '') {
		alert('debe llenar su nuevo password');
		nuevo.focus();
		return false;
	}

	if (Trim(nuevo2.value) == '') {
		alert('debe llenar la repeticion de su password');
		nuevo2.focus();
		return false;
	}

	if (Trim(nuevo.value) != Trim(nuevo2.value)) {
		alert('La repeticion de password debe coincidir');
		nuevo2.focus();
		return false;
	}

	btn_a = document.formulario.add_button;
	btn_a.disabled = true;

	//document.formulario.submit();
	var fd = new FormData(document.forms['formulario']);

	div_modulo.html(imagen_modulo);

	let result;

	try {
		result = await $.ajax({
			url: '/',
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
				console.log(errorThrown); console.log(qXHR); console.log(textStatus);
			},
		});
		//alert(result);
	}
	catch (e) {
		console.error(e);
	}
}