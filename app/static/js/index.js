/************************************************************************************/
/************************************************************************************/
/****************Desarrollador, Programador: Alan Claros Camacho ********************/
/****************E-mail: alan_Claros13@hotmail.com **********************************/
/************************************************************************************/
/************************************************************************************/

function load_login() {
	document.forms["formulario"].username.focus();
}

function verifyForm() {
	nombre = "username";
	objeto = document.forms["formulario"].elements[nombre];
	if (TrimDerecha(TrimIzquierda(objeto.value)) == "") {
		alert("Debe escribir el nombre de usuario");
		objeto.focus();
		return false;
	}

	nombre = "password";
	objeto = document.forms["formulario"].elements[nombre];
	if (TrimDerecha(TrimIzquierda(objeto.value)) == "") {
		alert("Debe escribir su password");
		objeto.focus();
		return false;
	}

	document.forms["formulario"].submit();

	return true;
}