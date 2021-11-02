from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from django.db import transaction
from clientes.models import Clientes

from utils.validators import validate_string, validate_number_int, validate_email


class ClientesController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Clientes'
        self.modelo_id = 'cliente_id'
        self.modelo_app = 'clientes'
        self.modulo_id = settings.MOD_CLIENTES

        # variables de session
        self.modulo_session = "clientes"
        self.columnas.append('apellidos')
        self.columnas.append('nombres')
        self.columnas.append('ci_nit')

        self.variables_filtros.append('search_apellidos')
        self.variables_filtros.append('search_nombres')
        self.variables_filtros.append('search_ci_nit')

        self.variables_filtros_defecto['search_apellidos'] = ''
        self.variables_filtros_defecto['search_nombres'] = ''
        self.variables_filtros_defecto['search_ci_nit'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"
        self.variable_order_type_value = 'ASC'

        # tablas donde se debe verificar para eliminar
        #self.modelos_eliminar = {'clientes': 'ClientesDivisas'}
        self.modelos_eliminar = {'ventas': 'Ventas'}

        # control del formulario
        self.control_form = "txt|2|S|apellidos|Apellidos;"
        self.control_form += "txt|2|S|nombres|Nombres"
        #self.control_form += "txt|2|S|ci_nit|"

    def index(self, request):
        DefaultValues.index(self, request)
        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.activo, self.inactivo]
        self.filtros_modulo['cliente_id__gt'] = 1
        # apellidos
        if self.variables_filtros_values['search_apellidos'].strip() != "":
            self.filtros_modulo['apellidos__icontains'] = self.variables_filtros_values['search_apellidos'].strip()
        # nombres
        if self.variables_filtros_values['search_nombres'].strip() != "":
            self.filtros_modulo['nombres__icontains'] = self.variables_filtros_values['search_nombres'].strip()
        # ci_dni
        if self.variables_filtros_values['search_ci_nit'].strip() != "":
            self.filtros_modulo['ci_nit__icontains'] = self.variables_filtros_values['search_ci_nit'].strip()

        # paginacion, paginas y definiendo el LIMIT *,*
        self.pagination()
        # asigamos la paginacion a la session
        request.session[self.modulo_session]['pages_list'] = self.pages_list

        # recuperamos los datos
        return self.get_list()

    def is_in_db(self, id, nuevo_valor):
        """verificamos si existe en la base de datos"""
        if nuevo_valor == '':
            # dejamos guardar sin nit
            return False

        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        filtros = {}
        filtros['status_id_id__in'] = [self.activo, self.inactivo]
        filtros['ci_nit__iexact'] = nuevo_valor

        if id:
            cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        else:
            cantidad = modelo.objects.filter(**filtros).count()

        # si no existe
        if cantidad > 0:
            return True

        return False

    def save(self, request, type='add'):
        """aniadimos un nuevo cliente"""
        try:
            ci_nit_txt = validate_string('ci/nit', request.POST['ci_nit'], remove_specials='yes', len_zero='yes')
            apellidos_txt = validate_string('apellidos', request.POST['apellidos'], remove_specials='yes')
            nombres_txt = validate_string('nombres', request.POST['nombres'], remove_specials='yes')
            telefonos_txt = validate_string('telefonos', request.POST['telefonos'], remove_specials='yes', len_zero='yes')
            direccion_txt = validate_string('direccion', request.POST['direccion'], remove_specials='yes', len_zero='yes')
            email_txt = validate_email('email', request.POST['email'], len_zero='yes')
            razon_social_txt = validate_string('razon_social', request.POST['razon_social'], remove_specials='yes', len_zero='yes')
            factura_a_txt = validate_string('factura_a', request.POST['factura_a'], remove_specials='yes', len_zero='yes')
            activo = 1 if 'activo' in request.POST.keys() else 0
            id = validate_number_int('id', request.POST['id'], len_zero='yes')

            # # verificamos ci_nit, apellidos y nombres
            # cliente_verificar = Clientes.objects.filter(ci_nit=ci_nit_txt, apellidos=apellidos_txt, nombres=nombres_txt)
            # if cliente_verificar:
            #     self.error_operation = 'ya existe este cliente: ' + apellidos_txt + ' ' + nombres_txt + ' CI/NIT: ' + ci_nit_txt
            #     return False

            if not self.is_in_db(id, ci_nit_txt):
                # activo
                if activo == 1:
                    status_cliente = self.status_activo
                else:
                    status_cliente = self.status_inactivo

                # punto
                usuario = request.user
                usuario_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=usuario)
                punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=usuario_perfil.punto_id)

                datos = {}
                datos['id'] = id
                datos['apellidos'] = apellidos_txt
                datos['nombres'] = nombres_txt
                datos['ci_nit'] = ci_nit_txt
                datos['telefonos'] = telefonos_txt
                datos['direccion'] = direccion_txt
                datos['email'] = email_txt
                datos['razon_social'] = razon_social_txt
                datos['factura_a'] = factura_a_txt
                datos['created_at'] = 'now'
                datos['updated_at'] = 'now'
                datos['user_perfil_id'] = usuario_perfil
                datos['status_id'] = status_cliente
                datos['punto_id'] = punto

                if self.save_db(type, **datos):
                    self.error_operation = ""
                    return True
                else:
                    self.error_operation = 'error al agregar el cliente'
                    return False
            else:
                self.error_operation = "Ya existe este ci/nit: " + ci_nit_txt
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar cliente, " + str(ex)
            return False

    def save_db(self, type='add', **datos):
        """aniadimos a la base de datos"""
        if not self.is_in_db(datos['id'], datos['ci_nit']):
            try:
                if type == 'add':
                    with transaction.atomic():
                        campos_add = {}
                        campos_add['apellidos'] = datos['apellidos']
                        campos_add['nombres'] = datos['nombres']
                        campos_add['ci_nit'] = datos['ci_nit']
                        campos_add['telefonos'] = datos['telefonos']
                        campos_add['direccion'] = datos['direccion']
                        campos_add['email'] = datos['email']
                        campos_add['razon_social'] = datos['razon_social']
                        campos_add['factura_a'] = datos['factura_a']
                        campos_add['created_at'] = datos['created_at']
                        campos_add['updated_at'] = datos['updated_at']
                        campos_add['user_perfil_id'] = datos['user_perfil_id']
                        campos_add['status_id'] = datos['status_id']
                        campos_add['punto_id'] = datos['punto_id']

                        cliente_add = Clientes.objects.create(**campos_add)
                        cliente_add.save()

                        return True

                if type == 'modify':
                    with transaction.atomic():
                        campos_update = {}
                        campos_update['apellidos'] = datos['apellidos']
                        campos_update['nombres'] = datos['nombres']
                        campos_update['ci_nit'] = datos['ci_nit']
                        campos_update['telefonos'] = datos['telefonos']
                        campos_update['direccion'] = datos['direccion']
                        campos_update['email'] = datos['email']
                        campos_update['razon_social'] = datos['razon_social']
                        campos_update['factura_a'] = datos['factura_a']
                        campos_update['updated_at'] = datos['updated_at']
                        campos_update['status_id'] = datos['status_id']

                        cliente_update = Clientes.objects.filter(pk=datos['id'])
                        cliente_update.update(**campos_update)

                        self.error_operation = ''
                        return True

                self.error_operation = 'Operation no valid'
                return False

            except Exception as ex:
                self.error_operation = 'error de argumentos, ' + str(ex)
                print('ERROR clientes add, '+str(ex))
                return False
        else:
            self.error_operation = "Ya existe este ci/nit: " + datos['ci_nit']
            return False

    def buscar_cliente(self, ci_nit='', apellidos='', nombres=''):
        """busqueda de clientes"""
        filtros = {}
        filtros['status_id__in'] = [self.activo]

        if ci_nit.strip() != '':
            filtros['ci_nit__iexact'] = ci_nit
        if apellidos.strip() != '':
            filtros['apellidos__icontains'] = apellidos
        if nombres.strip() != '':
            filtros['nombres__icontains'] = nombres

        Clientes_lista = Clientes.objects.filter(**filtros).order_by('apellidos', 'nombres')[0:30]

        return Clientes_lista
