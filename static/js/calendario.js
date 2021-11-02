
function sendSearchCalendario() {
    div_modulo = $("#div_block_content");
    sendFormObject('search', div_modulo);
}

function calendarioSearchPeriodo(periodo) {
    const periodo_form = document.forms['search'].elements['search_periodo'];
    periodo_form.value = periodo;
    sendSearchCalendario();
}

function calendarioShowDia(dia) {
    //registramos el dia en los otros forms
    const form_dia = document.forms['form_registrar_actividad'].elements['dia'];
    form_dia.value = dia;

    //span de nueva actividad y listado de actividades
    const span_periodo_actual = document.getElementById('span_periodo_actual').innerHTML;
    const span_nuevo = document.getElementById('span_nueva_actividad_periodo');
    span_nuevo.innerHTML = dia + '-' + span_periodo_actual;

    //quitando mensajes
    const res_act = $('#div_resultado_actividad');
    res_act.html('&nbsp;');

    const modalA = $('#modalActividad');
    modalA.modal();
}

function calendarioRegistrarActividad() {
    const hora_ini = document.getElementById('hora_ini').value;
    const minuto_ini = document.getElementById('minuto_ini').value;
    const hora_fin = document.getElementById('hora_fin').value;
    const minuto_fin = document.getElementById('minuto_fin').value;
    const actividad_id = document.getElementById('actividad_id').value;
    const detalle_actividad = document.getElementById('detalle_actividad').value;

    const btn_guardar = document.getElementById('btn_solicitar_actividad');
    const div_resultado = $('#div_resultado_actividad');

    const inicio = parseInt(hora_ini + minuto_ini);
    const fin = parseInt(hora_fin + minuto_fin);
    if (inicio >= fin) {
        div_resultado.html('<span class="font14 red">La hora de inicio no puede ser mayor o igual a la hora final</span>');
        return false;
    }

    //llenamos el formulario
    document.forms['form_registrar_actividad'].elements['hora_ini'].value = hora_ini;
    document.forms['form_registrar_actividad'].elements['minuto_ini'].value = minuto_ini;
    document.forms['form_registrar_actividad'].elements['hora_fin'].value = hora_fin;
    document.forms['form_registrar_actividad'].elements['minuto_fin'].value = minuto_fin;
    document.forms['form_registrar_actividad'].elements['actividad'].value = actividad_id;
    document.forms['form_registrar_actividad'].elements['detalle'].value = detalle_actividad;

    const token_send = document.forms['form_registrar_actividad'].elements['csrfmiddlewaretoken'].value;
    const datos_send = {
        'module_x': document.forms['form_registrar_actividad'].elements['module_x'].value,
        'operation_x': document.forms['form_registrar_actividad'].elements['operation_x'].value,
        'csrfmiddlewaretoken': token_send,
        'hora_ini': hora_ini,
        'minuto_ini': minuto_ini,
        'hora_fin': hora_fin,
        'minuto_fin': minuto_fin,
        'actividad': actividad_id,
        'detalle': detalle_actividad,
        'dia': document.forms['form_registrar_actividad'].elements['dia'].value
    }

    btn_guardar.disabled = true;
    const ruta_imagen2 = url_empresa + '/static/img/pass/loading.gif';
    const imagen_mo = '<img src="' + ruta_imagen2 + '">';
    div_resultado.html(imagen_mo);

    let para_cargar = url_empresa;
    if (para_cargar != '') {
        para_cargar = url_empresa + '/';
    }

    div_resultado.load(para_cargar, datos_send, function () {
        //verificamos por error
        if (document.getElementById('resultado_existe_error')) {
            const ver_error = document.getElementById('resultado_existe_error').value;
            if (ver_error == '1') {
                btn_guardar.disabled = false;
            }
            else {
                //recargamos el calendario
                //const button_back = $('#button_volver');
                //button_back.click();
                const modalAct2 = $('#modalActividad');
                modalAct2.modal('hide');
                setTimeout(function () { sendSearchCalendario(); }, 1000);

                //webpush usuarios
                const perfil_dpto = document.forms['form_registrar_actividad'].elements['perfil_dpto'].value;
                const dpto_user = document.forms['form_registrar_actividad'].elements['departamento_usuario'].value;
                const actividad_user = document.getElementById('actividad_id');
                const text_actividad = actividad_user.options[actividad_user.selectedIndex].text;
                const mes_user = document.getElementById('span_periodo_actual').innerHTML;
                const dia_user = document.forms['form_registrar_actividad'].elements['dia'].value;
                const token_user = document.forms['form_registrar_actividad'].elements['csrfmiddlewaretoken'].value;

                if (perfil_dpto == '4') {
                    //soo perfil departamento manda notificacion de reserva
                    const head = 'Solicitud Reserva';
                    const body = 'Dpto: ' + dpto_user + '\nActividad: ' + text_actividad + '\nFecha: ' + dia_user + '-' + mes_user + "\nHorario: " + hora_ini + ':' + minuto_ini + '-' + hora_fin + ':' + minuto_fin;
                    const id = document.getElementById('lista_notificacion').value;

                    //btn_push= document.getElementById('btn_webpush');
                    url_push = document.forms['form_notificaciones'].elements['url_webpush'].value;

                    datos_push = {
                        'head': head,
                        'body': body,
                        'id': id,
                        'csrfmiddlewaretoken': token_user,
                    }

                    $("#div_push_result").html('send push');
                    $("#div_push_result").load(url_push, datos_push, function () {
                        //alert('push enviado');
                    });
                }
            }
        }
        else {
            btn_guardar.disabled = false;
        }
    });
}

function calendarioShowActividades(dia) {
    //quitando mensajes
    const res_act = $('#div_resultado_listado_' + dia);
    res_act.html('&nbsp;');

    const modalListado = $('#modalListado_' + dia);
    modalListado.modal();
}

//confirmamos o eliminamos actividad
function calendarioConfirmarActividad(calendario_id, fecha_txt, departamento, hora_ini, hora_fin, user_perfil, perfil_departamento, actividad, user_id_dpto) {
    const pfecha = document.getElementById('span_confirmar_fecha');
    const pdepa = document.getElementById('span_confirmar_departamento');
    const phora_ini = document.getElementById('span_confirmar_hora_ini');
    const phora_fin = document.getElementById('span_confirmar_hora_fin');
    const pactividad = document.getElementById('span_confirmar_actividad');
    const pdetalle = document.getElementById('span_confirmar_detalle');

    //web push user dpto
    const user_dpto = document.forms['form_registrar_actividad'].elements['user_id_dpto'];
    user_dpto.value = user_id_dpto;

    pfecha.innerHTML = fecha_txt;
    pdepa.innerHTML = departamento;
    phora_ini.innerHTML = hora_ini;
    phora_fin.innerHTML = hora_fin;
    pactividad.innerHTML = actividad;
    pdetalle.innerHTML = document.getElementById('detalle_' + calendario_id).value;

    //forms de confirmacion y eliminacion
    const frm_conf = document.forms['form_confirmar_actividad'].elements['id'];
    frm_conf.value = calendario_id;
    const frm_anular = document.forms['form_anular_actividad'].elements['id'];
    frm_anular.value = calendario_id;

    //quitando mensajes
    const res_conf = $('#div_resultado_confirmar');
    res_conf.html('&nbsp;');

    const modalC = $('#modalConfirmar');
    modalC.modal();
}

//confirmar actividad
function calendarioConfirmarSuccess() {
    //mostramos mensaje de confirmacion
    const res_conf = $('#div_resultado_confirmar');
    msg = '<br><p>Esta Seguro de Confirmar esta Actividad?</p><button class="btn btn-primary btn-sm" onclick="calendarioConfirmarSend();"><i class="nav-icon fas fa-save"></i>&nbsp;&nbsp;Confirmar</button>';
    res_conf.html(msg);
}

//eliminar actividad
function calendarioEliminarActividad() {
    //mostramos mensaje de confirmacion
    const res_conf = $('#div_resultado_confirmar');
    msg = '<br><p>Esta Seguro de Eliminar esta Actividad?</p><button class="btn btn-danger btn-sm" onclick="calendarioEliminarSend();"><i class="nav-icon far fa-times-circle"></i>&nbsp;&nbsp;Eliminar</button>';
    res_conf.html(msg);
}

//enviar confirmar
function calendarioConfirmarSend() {
    const token_send = document.forms['form_confirmar_actividad'].elements['csrfmiddlewaretoken'].value;
    const datos_send = {
        'module_x': document.forms['form_confirmar_actividad'].elements['module_x'].value,
        'operation_x': document.forms['form_confirmar_actividad'].elements['operation_x'].value,
        'csrfmiddlewaretoken': token_send,
        'id': document.forms['form_confirmar_actividad'].elements['id'].value
    }

    const btn_conf = document.getElementById('btn_confirmar_confirmar');
    btn_conf.disabled = true;
    let btn_el = null;
    if (document.getElementById('btn_confirmar_eliminar')) {
        btn_el = document.getElementById('btn_confirmar_eliminar');
        btn_el.disabled = true;
    }

    const ruta_imagen2 = url_empresa + '/static/img/pass/loading.gif';
    const imagen_mo = '<img src="' + ruta_imagen2 + '">';
    const div_conf = $('#div_resultado_confirmar');
    div_conf.html(imagen_mo);

    let para_cargar = url_empresa;
    if (para_cargar != '') {
        para_cargar = url_empresa + '/';
    }

    div_conf.load(para_cargar, datos_send, function () {
        //verificamos por error
        if (document.getElementById('resultado_existe_error')) {
            const ver_error = document.getElementById('resultado_existe_error').value;
            if (ver_error == '1') {
                btn_conf.disabled = false;
                if (document.getElementById('btn_confirmar_eliminar')) {
                    btn_el.disabled = false;
                }
            }
            else {
                //recargamos el calendario
                const modalAct2 = $('#modalConfirmar');
                modalAct2.modal('hide');
                setTimeout(function () { sendSearchCalendario(); }, 1000);

                //send push
                const pfecha_user = document.getElementById('span_confirmar_fecha').innerHTML;
                const pdepa_user = document.getElementById('span_confirmar_departamento').innerHTML;
                const phora_ini_user = document.getElementById('span_confirmar_hora_ini').innerHTML;
                const phora_fin_user = document.getElementById('span_confirmar_hora_fin').innerHTML;
                const pactividad_user = document.getElementById('span_confirmar_actividad').innerHTML;
                const pdetalle_user = document.getElementById('span_confirmar_detalle').innerHTML;
                const token_user = document.forms['form_confirmar_actividad'].elements['csrfmiddlewaretoken'].value;

                const head = 'Reserva Confirmada';
                const body = 'Dpto: ' + pdepa_user + '\nActividad: ' + pactividad_user + '\nFecha: ' + pfecha_user + "\nHorario: " + phora_ini_user + '-' + phora_fin_user;
                const id = document.forms['form_registrar_actividad'].elements['user_id_dpto'].value;

                //btn_push= document.getElementById('btn_webpush');
                const url_push = document.forms['form_notificaciones'].elements['url_webpush'].value;

                const datos_push = {
                    'head': head,
                    'body': body,
                    'id': id,
                    'csrfmiddlewaretoken': token_user,
                }

                $("#div_push_result").html('send push');
                $("#div_push_result").load(url_push, datos_push, function () {
                    //alert('push enviado');
                });

            }
        }
        else {
            btn_conf.disabled = false;
            if (document.getElementById('btn_confirmar_eliminar')) {
                btn_el.disabled = false;
            }
        }
    });
}

//enviar anular
function calendarioEliminarSend() {
    const token_send = document.forms['form_anular_actividad'].elements['csrfmiddlewaretoken'].value;
    const datos_send = {
        'module_x': document.forms['form_anular_actividad'].elements['module_x'].value,
        'operation_x': document.forms['form_anular_actividad'].elements['operation_x'].value,
        'csrfmiddlewaretoken': token_send,
        'id': document.forms['form_anular_actividad'].elements['id'].value
    }

    const btn_el = document.getElementById('btn_confirmar_eliminar');
    btn_el.disabled = true;
    let btn_conf = null;
    if (document.getElementById('btn_confirmar_confirmar')) {
        btn_conf = document.getElementById('btn_confirmar_confirmar');
        btn_conf.disabled = true;
    }

    const ruta_imagen2 = url_empresa + '/static/img/pass/loading.gif';
    const imagen_mo = '<img src="' + ruta_imagen2 + '">';
    const div_conf = $('#div_resultado_confirmar');
    div_conf.html(imagen_mo);

    let para_cargar = url_empresa;
    if (para_cargar != '') {
        para_cargar = url_empresa + '/';
    }

    div_conf.load(para_cargar, datos_send, function () {
        //verificamos por error
        if (document.getElementById('resultado_existe_error')) {
            const ver_error = document.getElementById('resultado_existe_error').value;
            if (ver_error == '1') {
                btn_el.disabled = false;
                if (document.getElementById('btn_confirmar_confirmar')) {
                    btn_conf.disabled = false;
                }
            }
            else {
                //recargamos el calendario
                const modalAct2 = $('#modalConfirmar');
                modalAct2.modal('hide');
                setTimeout(function () { sendSearchCalendario(); }, 1000);

                //send push
                const perfil_dpto = document.forms['form_registrar_actividad'].elements['perfil_dpto'].value;
                const pfecha_user = document.getElementById('span_confirmar_fecha').innerHTML;
                const pdepa_user = document.getElementById('span_confirmar_departamento').innerHTML;
                const phora_ini_user = document.getElementById('span_confirmar_hora_ini').innerHTML;
                const phora_fin_user = document.getElementById('span_confirmar_hora_fin').innerHTML;
                const pactividad_user = document.getElementById('span_confirmar_actividad').innerHTML;
                const pdetalle_user = document.getElementById('span_confirmar_detalle').innerHTML;
                const token_user = document.forms['form_confirmar_actividad'].elements['csrfmiddlewaretoken'].value;

                const head = 'Reserva Eliminada';
                const body = 'Dpto: ' + pdepa_user + '\nActividad: ' + pactividad_user + '\nFecha: ' + pfecha_user + "\nHorario: " + phora_ini_user + '-' + phora_fin_user;
                let id_send = '';
                if (perfil_dpto == '4') {
                    //departamento manda a los usuarios del sistema
                    id_send = document.getElementById('lista_notificacion').value;
                }
                else {
                    //usuario sistema manda al departamento
                    id_send = document.forms['form_registrar_actividad'].elements['user_id_dpto'].value;
                }


                //btn_push= document.getElementById('btn_webpush');
                const url_push = document.forms['form_notificaciones'].elements['url_webpush'].value;

                const datos_push = {
                    'head': head,
                    'body': body,
                    'id': id_send,
                    'csrfmiddlewaretoken': token_user,
                }

                $("#div_push_result").html('send push');
                $("#div_push_result").load(url_push, datos_push, function () {
                    //alert('push enviado');
                });
            }
        }
        else {
            btn_el.disabled = false;
            if (document.getElementById('btn_confirmar_confirmar')) {
                btn_conf.disabled = false;
            }
        }
    });
}


//eliminar actividad show para usuario distinto a departamento
function calendarioEliminarShow(dia, calendario_id, dpto, hora_ini, hora_fin, actividad, user_id_dpto, fecha) {
    //asignamos para la confirmacion
    document.forms['form_anular_actividad'].elements['departamento'].value = dpto;
    document.forms['form_anular_actividad'].elements['actividad'].value = actividad;
    document.forms['form_anular_actividad'].elements['hora_ini'].value = hora_ini;
    document.forms['form_anular_actividad'].elements['hora_fin'].value = hora_fin;
    document.forms['form_anular_actividad'].elements['user_id_dpto'].value = user_id_dpto;
    document.forms['form_anular_actividad'].elements['fecha'].value = fecha;

    //mostramos mensaje de confirmacion
    const res_conf = $('#div_resultado_listado_' + dia);
    const span_calendario = document.getElementById('span_calendario_' + calendario_id).innerHTML;

    const frm_anular = document.forms['form_anular_actividad'].elements['id'];
    frm_anular.value = calendario_id;

    msg = '<br><p>Esta Seguro de Eliminar esta Actividad?</p><p>' + span_calendario + '</p><button class="btn btn-danger btn-sm" id="btn_lista_del_' + calendario_id + '" onclick="calendarioEliminarSendUser(' + "'" + dia + "','" + calendario_id + "'" + ');"><i class="nav-icon far fa-times-circle"></i>&nbsp;&nbsp;Eliminar</button>';
    res_conf.html(msg);
}

//enviar anular por usuario 
function calendarioEliminarSendUser(dia, calendario_id) {
    const token_send = document.forms['form_anular_actividad'].elements['csrfmiddlewaretoken'].value;
    const datos_send = {
        'module_x': document.forms['form_anular_actividad'].elements['module_x'].value,
        'operation_x': 'anular_actividad_user',
        'csrfmiddlewaretoken': token_send,
        'id': document.forms['form_anular_actividad'].elements['id'].value,
        'dia': dia
    }

    const btn_el = document.getElementById('btn_lista_del_' + calendario_id);
    btn_el.disabled = true;

    const ruta_imagen2 = url_empresa + '/static/img/pass/loading.gif';
    const imagen_mo = '<img src="' + ruta_imagen2 + '">';
    const div_conf = $('#div_resultado_listado_' + dia);
    div_conf.html(imagen_mo);

    let para_cargar = url_empresa;
    if (para_cargar != '') {
        para_cargar = url_empresa + '/';
    }

    div_conf.load(para_cargar, datos_send, function () {
        //verificamos por error
        if (document.getElementById('resultado_existe_error_' + dia)) {
            const ver_error = document.getElementById('resultado_existe_error_' + dia).value;
            if (ver_error == '1') {
                btn_el.disabled = false;
            }
            else {
                //recargamos el calendario
                const modalAct2 = $('#modalListado_' + dia);
                modalAct2.modal('hide');
                setTimeout(function () { sendSearchCalendario(); }, 1000);

                //send push
                //const perfil_dpto = document.forms['form_registrar_actividad'].elements['perfil_dpto'].value;
                const pfecha_user = document.forms['form_anular_actividad'].elements['fecha'].value;
                const pdepa_user = document.forms['form_anular_actividad'].elements['departamento'].value;
                const phora_ini_user = document.forms['form_anular_actividad'].elements['hora_ini'].value;
                const phora_fin_user = document.forms['form_anular_actividad'].elements['hora_fin'].value;
                const pactividad_user = document.forms['form_anular_actividad'].elements['actividad'].value;
                //const pdetalle_user = document.getElementById('span_confirmar_detalle').innerHTML;
                const token_user = document.forms['form_anular_actividad'].elements['csrfmiddlewaretoken'].value;
                const id_send = document.forms['form_anular_actividad'].elements['user_id_dpto'].value;

                const head = 'Reserva Eliminada';
                const body = 'Dpto: ' + pdepa_user + '\nActividad: ' + pactividad_user + '\nFecha: ' + pfecha_user + "\nHorario: " + phora_ini_user + '-' + phora_fin_user;

                //console.log('id send: ', id_send);
                //console.log('body: ', body);

                //solo usuarios del sistema eliminan y mandan a los usuarios depa si corresponde
                if (id_send != '' && id_send != '0') {
                    const url_push = document.forms['form_notificaciones'].elements['url_webpush'].value;

                    const datos_push = {
                        'head': head,
                        'body': body,
                        'id': id_send,
                        'csrfmiddlewaretoken': token_user,
                    }

                    $("#div_push_result").html('send push');
                    $("#div_push_result").load(url_push, datos_push, function () {
                        //alert('push enviado');
                    });
                }

            }
        }
        else {
            btn_el.disabled = false;
        }
    });
}