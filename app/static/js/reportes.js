/************************************************************************************/
/************************************************************************************/
/****************Desarrollador, Programador: Alan Claros Camacho ********************/
/****************E-mail: alan_Claros13@hotmail.com **********************************/
/************************************************************************************/
/************************************************************************************/

//acc, control especifico del modulo
function arqueoCaja() {
	caja = document.getElementById('caja').value;
	fecha = document.getElementById('fecha').value;

	document.forms['form_print'].elements['operation_x2'].value = 'print';
	document.forms['form_print'].elements['id'].value = caja;
	document.forms['form_print'].elements['fecha'].value = fecha;

	document.forms['form_print'].submit();
}

//acc, ingresos a caja
function ingresosCaja() {
	// ciudad = document.getElementById('ciudad').value;
	// sucursal = document.getElementById('sucursal').value;
	ciudad = '1';
	sucursal = '1';

	caja = document.getElementById('caja').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_print'].elements['operation_x2'].value = 'print';
	document.forms['form_print'].elements['ciudad'].value = ciudad;
	document.forms['form_print'].elements['sucursal'].value = sucursal;
	document.forms['form_print'].elements['caja'].value = caja;
	document.forms['form_print'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_print'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_print'].elements['anulados'].value = anulados;

	document.forms['form_print'].submit();
}

//acc, ingresos a caja excel
function ingresosCajaExcel() {
	// ciudad = document.getElementById('ciudad').value;
	// sucursal = document.getElementById('sucursal').value;
	ciudad = '1';
	sucursal = '1';
	caja = document.getElementById('caja').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_excel'].elements['operation_x2'].value = 'print_excel';
	document.forms['form_excel'].elements['ciudad'].value = ciudad;
	document.forms['form_excel'].elements['sucursal'].value = sucursal;
	document.forms['form_excel'].elements['caja'].value = caja;
	document.forms['form_excel'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_excel'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_excel'].elements['anulados'].value = anulados;

	document.forms['form_excel'].submit();
}

//egresos de caja
function egresosCaja() {
	// ciudad = document.getElementById('ciudad').value;
	// sucursal = document.getElementById('sucursal').value;
	ciudad = '1';
	sucursal = '1';
	caja = document.getElementById('caja').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_print'].elements['operation_x2'].value = 'print';
	document.forms['form_print'].elements['ciudad'].value = ciudad;
	document.forms['form_print'].elements['sucursal'].value = sucursal;
	document.forms['form_print'].elements['caja'].value = caja;
	document.forms['form_print'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_print'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_print'].elements['anulados'].value = anulados;

	document.forms['form_print'].submit();
}

//egresos de caja excel
function egresosCajaExcel() {
	// ciudad = document.getElementById('ciudad').value;
	// sucursal = document.getElementById('sucursal').value;
	ciudad = '1';
	sucursal = '1';
	caja = document.getElementById('caja').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_excel'].elements['operation_x2'].value = 'print_excel';
	document.forms['form_excel'].elements['ciudad'].value = ciudad;
	document.forms['form_excel'].elements['sucursal'].value = sucursal;
	document.forms['form_excel'].elements['caja'].value = caja;
	document.forms['form_excel'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_excel'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_excel'].elements['anulados'].value = anulados;

	document.forms['form_excel'].submit();
}

//movimientos de caja
function movimientosCaja() {
	// ciudad = document.getElementById('ciudad').value;
	// sucursal = document.getElementById('sucursal').value;
	ciudad = '1';
	sucursal = '1';
	caja = document.getElementById('caja').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_print'].elements['operation_x2'].value = 'print';
	document.forms['form_print'].elements['ciudad'].value = ciudad;
	document.forms['form_print'].elements['sucursal'].value = sucursal;
	document.forms['form_print'].elements['caja'].value = caja;
	document.forms['form_print'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_print'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_print'].elements['anulados'].value = anulados;

	document.forms['form_print'].submit();
}

//movimientos de caja excel
function movimientosCajaExcel() {
	// ciudad = document.getElementById('ciudad').value;
	// sucursal = document.getElementById('sucursal').value;
	ciudad = '1';
	sucursal = '1';
	caja = document.getElementById('caja').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_print'].elements['operation_x2'].value = 'print_excel';
	document.forms['form_print'].elements['ciudad'].value = ciudad;
	document.forms['form_print'].elements['sucursal'].value = sucursal;
	document.forms['form_print'].elements['caja'].value = caja;
	document.forms['form_print'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_print'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_print'].elements['anulados'].value = anulados;

	document.forms['form_print'].submit();
}

//reportes cobros
function reportesCobros(tipo) {
	bloque = document.getElementById('bloque').value;
	piso = document.getElementById('piso').value;
	caja = document.getElementById('caja').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_print'].elements['operation_x2'].value = tipo;
	document.forms['form_print'].elements['caja'].value = caja;
	document.forms['form_print'].elements['bloque'].value = bloque;
	document.forms['form_print'].elements['piso'].value = piso;
	document.forms['form_print'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_print'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_print'].elements['anulados'].value = anulados;

	document.forms['form_print'].submit();
}

//reportes cobros mensuales
function reportesCobrosMensuales(tipo) {
	bloque = document.getElementById('bloque').value;
	piso = document.getElementById('piso').value;
	cobro_mensual = document.getElementById('cobro_mensual').value;
	caja = document.getElementById('caja').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_print'].elements['operation_x2'].value = tipo;
	document.forms['form_print'].elements['caja'].value = caja;
	document.forms['form_print'].elements['bloque'].value = bloque;
	document.forms['form_print'].elements['piso'].value = piso;
	document.forms['form_print'].elements['cobro_mensual'].value = cobro_mensual;
	document.forms['form_print'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_print'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_print'].elements['anulados'].value = anulados;

	document.forms['form_print'].submit();
}

//reportes cobros manuales
function reportesCobrosManuales(tipo) {
	bloque = document.getElementById('bloque').value;
	piso = document.getElementById('piso').value;
	cobro_manual = document.getElementById('cobro_manual').value;
	caja = document.getElementById('caja').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_print'].elements['operation_x2'].value = tipo;
	document.forms['form_print'].elements['caja'].value = caja;
	document.forms['form_print'].elements['bloque'].value = bloque;
	document.forms['form_print'].elements['piso'].value = piso;
	document.forms['form_print'].elements['cobro_manual'].value = cobro_manual;
	document.forms['form_print'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_print'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_print'].elements['anulados'].value = anulados;

	document.forms['form_print'].submit();
}

//reportes lecturas
function reportesLecturas(tipo) {
	bloque = document.getElementById('bloque').value;
	piso = document.getElementById('piso').value;
	caja = document.getElementById('caja').value;
	periodo_ini = document.getElementById('periodo_ini').value;
	periodo_fin = document.getElementById('periodo_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_print'].elements['operation_x2'].value = tipo;
	document.forms['form_print'].elements['caja'].value = caja;
	document.forms['form_print'].elements['bloque'].value = bloque;
	document.forms['form_print'].elements['piso'].value = piso;
	document.forms['form_print'].elements['periodo_ini'].value = periodo_ini;
	document.forms['form_print'].elements['periodo_fin'].value = periodo_fin;
	document.forms['form_print'].elements['anulados'].value = anulados;

	document.forms['form_print'].submit();
}

//reportes expensas
function reportesExpensas(tipo) {
	bloque = document.getElementById('bloque').value;
	piso = document.getElementById('piso').value;
	caja = document.getElementById('caja').value;
	periodo_ini = document.getElementById('periodo_ini').value;
	periodo_fin = document.getElementById('periodo_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_print'].elements['operation_x2'].value = tipo;
	document.forms['form_print'].elements['caja'].value = caja;
	document.forms['form_print'].elements['bloque'].value = bloque;
	document.forms['form_print'].elements['piso'].value = piso;
	document.forms['form_print'].elements['periodo_ini'].value = periodo_ini;
	document.forms['form_print'].elements['periodo_fin'].value = periodo_fin;
	document.forms['form_print'].elements['anulados'].value = anulados;

	document.forms['form_print'].submit();
}

//reportes cobros pendientes
function reportesCobrosPendientes(tipo) {
	bloque = document.getElementById('bloque').value;
	piso = document.getElementById('piso').value;
	periodo_ini = document.getElementById('periodo_ini').value;
	periodo_fin = document.getElementById('periodo_fin').value;

	document.forms['form_print'].elements['operation_x2'].value = tipo;
	document.forms['form_print'].elements['bloque'].value = bloque;
	document.forms['form_print'].elements['piso'].value = piso;
	document.forms['form_print'].elements['periodo_ini'].value = periodo_ini;
	document.forms['form_print'].elements['periodo_fin'].value = periodo_fin;

	document.forms['form_print'].submit();
}