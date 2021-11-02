# from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models.fields import CharField, DecimalField, IntegerField, BooleanField
from utils.custome_db_types import DateFieldCustome, DateTimeFieldCustome

from utils.dates_functions import get_date_show, get_month_3digits

from django.apps import apps
from django.conf import settings

from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta


def get_permissions_user(user, modulo):
    """
    get user permissions per module
    :param user: (object) user object
    :param modulo: (int) modulo id
    :return: (dict) user permissions
    """
    try:
        app_modulo = apps.get_model('permisos', 'Modulos')
        modulo_user = app_modulo.objects.get(pk=int(modulo))
        user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=user)

        app_user_modulos = apps.get_model('permisos', 'UsersModulos')
        user_modulo = app_user_modulos.objects.get(user_perfil_id=user_perfil, modulo_id=modulo_user)

        return user_modulo

    except Exception as ex:
        raise AttributeError('Error al recuperar permiso de usuario: ' + str(user), ', ' + str(modulo))


def get_user_permission_operation(user, modulo, operacion):
    """
    return True if user have permission for do operation (just admin user can see other sucursal objects) else False
    :param user: (object) user trying do operation
    :param modulo: (object) modulo id
    :param operacion: (str) operation needed
    :return: True if have permission else False
    """

    try:
        app_modulo = apps.get_model('permisos', 'Modulos')
        modulo_user = app_modulo.objects.get(pk=int(modulo))
        user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=user)

        app_user_modulo = apps.get_model('permisos', 'UsersModulos')
        user_modulo = app_user_modulo.objects.get(user_perfil_id=user_perfil, modulo_id=modulo_user)

        if user_modulo:
            if operacion == 'lista':
                if user_modulo.enabled:
                    return True

            if operacion == 'adicionar':
                if user_modulo.adicionar:
                    return True

            if operacion == 'modificar':
                if user_modulo.modificar:
                    return True

            if operacion == 'eliminar':
                if user_modulo.eliminar:
                    return True

            if operacion == 'anular':
                if user_modulo.anular:
                    return True

            if operacion == 'imprimir':
                if user_modulo.imprimir:
                    return True

            if operacion == 'permiso':
                if user_modulo.permiso:
                    return True

        # no tiene permiso false
        return False

    except Exception as ex:
        print(f"Error de permiso {user}, {modulo}, {operacion} : " + str(ex))
        return False


def get_system_settings():
    retorno = {}
    try:
        app_configuraciones = apps.get_model('configuraciones', 'Configuraciones')
        configuraciones_sistema = app_configuraciones.objects.get(pk=1)
        retorno = configuraciones_sistema.__dict__

    except Exception as ex:
        print('tabla configuraciones no cargada, ' + str(ex))

    return retorno


def current_date():
    datos_settings = get_system_settings()
    anio = '20' + str(datetime.now().year) if len(str(datetime.now().year)) == 2 else str(datetime.now().year)
    mes = '0' + str(datetime.now().month) if len(str(datetime.now().month)) == 1 else str(datetime.now().month)
    dia = '0' + str(datetime.now().day) if len(str(datetime.now().day)) == 1 else str(datetime.now().day)
    fecha = anio + '-' + mes + '-' + dia

    try:
        if datos_settings['usar_fecha_servidor'] == 'no':
            anio = '20' + str(datos_settings['fecha_sistema'].year) if len(str(datos_settings['fecha_sistema'].year)) == 2 else str(datos_settings['fecha_sistema'].year)
            mes = '0' + str(datos_settings['fecha_sistema'].month) if len(str(datos_settings['fecha_sistema'].month)) == 1 else str(datos_settings['fecha_sistema'].month)
            dia = '0' + str(datos_settings['fecha_sistema'].day) if len(str(datos_settings['fecha_sistema'].day)) == 1 else str(datos_settings['fecha_sistema'].day)
            fecha = anio + '-' + mes + '-' + dia
    except Exception as ex:
        print('tabla configuraciones(current date) no cargada, ' + str(ex))

    return fecha


def report_date():
    fecha = current_date()
    fecha = get_date_show(fecha=fecha, formato_ori='yyyy-mm-dd', formato='dd-MMM-yyyy HH:ii')

    return fecha


def get_sucursal_settings(sucursal_id):
    retorno = {}
    try:
        sucursal_datos = apps.get_model('configuraciones', 'Sucursales').objects.get(pk=int(sucursal_id))
        lista = sucursal_datos.__dict__
        retorno['empresa'] = lista['empresa']
        retorno['direccion'] = lista['direccion']
        retorno['ciudad'] = lista['ciudad']
        retorno['telefonos'] = lista['telefonos']
        retorno['actividad'] = lista['actividad']

    except Exception as ex:
        retorno['empresa'] = 'error'
        retorno['direccion'] = 'error'
        retorno['ciudad'] = 'error'
        retorno['telefonos'] = 'error'
        retorno['actividad'] = 'error'

    return retorno


def get_html_column(modelo, not_required, request, instancia, *args):
    """devuelve las restricciones segun el tipo de columna"""
    #print('modelo: ', modelo)
    lista_not_required = []
    if not_required != '':
        div_not = not_required.split(',')
        for not_req in div_not:
            lista_not_required.append(not_req.strip())

    retorno = {}
    for arg in args:
        columna = modelo._meta.get_field(arg)
        #print('columna: ', columna, ' ..lista_not_requ: ', lista_not_required)
        if isinstance(columna, CharField):
            if arg not in lista_not_required:
                retorno[arg] = 'maxlength="' + str(columna.max_length) + '" onkeyup="txtValid(this);" onblur="txtValid(this);" '
            else:
                retorno[arg] = 'maxlength="' + str(columna.max_length) + '" '

            if request:
                retorno[arg] += (' value="' + request.POST[arg].replace('"', '&quot;') + '"') + F' id="{arg}"' + F' name="{arg}"'
            else:
                if instancia:
                    # para el caso de campos nulos
                    if getattr(instancia, arg):
                        retorno[arg] += (' value="' + getattr(instancia, arg).replace('"', '&quot;') + '"' if instancia else '') + F' id="{arg}"' + F' name="{arg}"'
                    else:
                        retorno[arg] += F' value="" id="{arg}" name="{arg}" '
                else:
                    retorno[arg] += F' value="" id="{arg}" name="{arg}" '

        elif isinstance(columna, DecimalField):
            retorno[arg] = 'onkeyup="validarNumeroPunto(this);txtValid(this);" onblur="txtValid(this);" '
            if request:
                retorno[arg] += (' value="' + request.POST[arg] + '"') + F' id="{arg}"' + F' name="{arg}"'
            else:
                if instancia:
                    retorno[arg] += (' value="' + str(getattr(instancia, arg)) + '"' if instancia else '') + F' id="{arg}"' + F' name="{arg}"'
                else:
                    retorno[arg] += F' value="" id="{arg}" name="{arg}" '

        elif isinstance(columna, DateFieldCustome):
            retorno[arg] = 'readonly="readonly"' + F' id="{arg}"' + F' name="{arg}" '
            if request:
                retorno[arg] += ' value="' + request.POST[arg] + '" '
            else:
                if instancia:
                    retorno[arg] += ' value="' + get_date_show(fecha=getattr(instancia, arg), formato='dd-MMM-yyyy') + '" '
                else:
                    retorno[arg] += ' value="" '

        elif isinstance(columna, DateTimeFieldCustome):
            retorno[arg] = 'readonly="readonly"' + F' id="{arg}"' + F' name="{arg}"'
            if request:
                retorno[arg] += ' value="' + request.POST[arg] + '" '
            else:
                if instancia:
                    retorno[arg] += ' value="' + get_date_show(fecha=getattr(instancia, arg), formato='dd-MMM-yyyy') + '" '
                else:
                    retorno[arg] += ' value="" '

        elif isinstance(columna, BooleanField):
            retorno[arg] = '' + F' id="{arg}"' + F' name="{arg}" '

        elif isinstance(columna, IntegerField):
            retorno[arg] = 'onkeyup="validarNumero(this);txtValid(this);" onblur="txtValid(this);" '
            if request:
                retorno[arg] += (' value="' + request.POST[arg] + '"') + F' id="{arg}"' + F' name="{arg}" '
            else:
                if instancia:
                    retorno[arg] += (' value="' + str(getattr(instancia, arg)) + '"' if instancia else '') + F' id="{arg}"' + F' name="{arg}" '
                else:
                    retorno[arg] += F' value="" id="{arg}" name="{arg}" '

        else:
            retorno[arg] = 'sin tipo'

    return retorno
