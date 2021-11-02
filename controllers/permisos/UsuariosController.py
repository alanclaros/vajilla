from controllers.DefaultValues import DefaultValues
from django.conf import settings
from permisos.models import Perfiles, UsersPerfiles, Modulos, UsersModulos
from django.apps import apps

# password
from django.contrib.auth.hashers import make_password

# transacciones
from django.db import transaction

from utils.validators import validate_string, validate_number_int, validate_email


class UsuariosController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)

        # redifiniendo valores de ValoresDefecto
        self.modelo_name = 'UsersPerfiles'
        self.modelo_id = 'user_perfil_id'  # id del usuario
        self.modelo_app = 'permisos'
        self.modulo_id = settings.MOD_USUARIOS

        # variables de session
        self.modulo_session = "usuarios"
        self.columnas.append('user_id__first_name')
        self.columnas.append('user_id__last_name')
        self.columnas.append('user_id__username')

        self.variables_filtros.append('search_nombres')
        self.variables_filtros.append('search_apellidos')
        self.variables_filtros.append('search_username')

        self.variables_filtros_defecto['search_nombres'] = ''
        self.variables_filtros_defecto['search_apellidos'] = ''
        self.variables_filtros_defecto['search_username'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"
        self.variable_order_type_value = "ASC"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {'configuraciones': 'Sucursales', 'configuraciones': 'Puntos'}

        # control del formulario
        # tipo|tamanio minimo|controlar|nombre|
        self.control_form = "txt|2|S|first_name|Nombres"
        self.control_form += ";txt|2|S|last_name|Apellidos"
        self.control_form += ";txt|2|S|username|Nombre de Usuario"

    def index(self, request):
        DefaultValues.index(self, request)
        self.filtros_modulo.clear()

        # si el usuario esta activo o no
        self.filtros_modulo['status_id_id__in'] = [self.activo, self.inactivo]
        self.filtros_modulo['user_perfil_id__gte'] = 1

        if self.variables_filtros_values['search_nombres'].strip() != "":
            self.filtros_modulo['user_id__first_name__icontains'] = self.variables_filtros_values['search_nombres'].strip()

        if self.variables_filtros_values['search_apellidos'].strip() != "":
            self.filtros_modulo['user_id__last_name__icontains'] = self.variables_filtros_values['search_apellidos'].strip()

        if self.variables_filtros_values['search_username'].strip() != "":
            self.filtros_modulo['user_id__username__icontains'] = self.variables_filtros_values['search_username'].strip()

        self.pagination()
        # asigamos la paginacion a la session
        request.session[self.modulo_session]['pages_list'] = self.pages_list

        # recuperamos los datos
        return self.get_list()

    def is_in_db(self, id, username, email):
        """verificamos si existe en la base de datos"""
        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        filtros = {}
        filtros['status_id_id__in'] = [self.activo, self.inactivo]
        filtros['user_id__username__iexact'] = username
        #filtros['email__iexact'] = email
        if id:
            cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        else:
            cantidad = modelo.objects.filter(**filtros).count()

        # si no existe
        if cantidad > 0:
            return True
        else:
            filtros = {}
            filtros['status_id_id__in'] = [self.activo, self.inactivo]
            filtros['user_id__email__iexact'] = email
            if id:
                cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
            else:
                cantidad = modelo.objects.filter(**filtros).count()
            # verificando email
            if cantidad > 0:
                return True

        return False

    def save(self, request, type='add'):
        """aniadimos usuario"""
        try:
            username_txt = validate_string('nombre usuario', request.POST['username'], remove_specials='yes')
            email_txt = validate_email('email', request.POST['email'], len_zero='yes')

            if not 'cambiar' in request.POST.keys():
                password_txt = validate_string('password', request.POST['password'])

            first_name = validate_string('nombres', request.POST['first_name'])
            last_name = validate_string('apellidos', request.POST['last_name'])
            perfil_id = validate_number_int('perfil', request.POST['perfil_id'])
            punto_id = validate_number_int('punto', request.POST['punto_id'])
            caja_id = validate_number_int('caja', request.POST['caja_id'])
            notificacion = validate_number_int('notificacion', request.POST['notificacion'])
            id = validate_number_int('id', request.POST['id'], len_zero='yes')

            if not self.is_in_db(id, username_txt, email_txt):

                with transaction.atomic():
                    if type == 'add':
                        if 'activo' in request.POST.keys():
                            status_user = 1  # django table
                            status_up = self.status_activo
                        else:
                            status_user = 0  # django table
                            status_up = self.status_inactivo

                        password_user = make_password(password_txt)
                        user = apps.get_model('auth', 'User')
                        usuario = user.objects.create(first_name=first_name, last_name=last_name,
                                                      username=username_txt, password=password_user, email=email_txt, is_active=status_user)
                        usuario.save()
                        #self.error_operation = ""

                        # relaciones y permisos
                        perfil = Perfiles.objects.get(pk=perfil_id)

                        user_perfil = UsersPerfiles.objects.create(user_id=usuario, perfil_id=perfil, punto_id=punto_id,
                                                                   caja_id=caja_id, notificacion=notificacion, status_id=status_up, created_at='now', updated_at='now')
                        user_perfil.save()

                        # usuarios modulos
                        UsersModulos.objects.filter(user_perfil_id=user_perfil).delete()
                        lista_modulos = Modulos.objects.all()
                        for modulo in lista_modulos:
                            # id modulo
                            modulo_id = modulo.modulo_id
                            # id user_modulo

                            nombre = 'modulo_' + str(modulo_id)
                            if nombre in request.POST.keys():
                                modulo_enabled = 1

                                if nombre + '_ad' in request.POST.keys():
                                    adicionar = 1
                                else:
                                    adicionar = 0

                                if nombre + '_mo' in request.POST.keys():
                                    modificar = 1
                                else:
                                    modificar = 0

                                if nombre + '_el' in request.POST.keys():
                                    eliminar = 1
                                else:
                                    eliminar = 0

                                if nombre + '_an' in request.POST.keys():
                                    anular = 1
                                else:
                                    anular = 0

                                if nombre + '_im' in request.POST.keys():
                                    imprimir = 1
                                else:
                                    imprimir = 0

                                if nombre + '_pe' in request.POST.keys():
                                    permiso = 1
                                else:
                                    permiso = 0

                                user_modulo = UsersModulos.objects.create(modulo_id=modulo, user_perfil_id=user_perfil, enabled=modulo_enabled, adicionar=adicionar,
                                                                          modificar=modificar, eliminar=eliminar, anular=anular, imprimir=imprimir, permiso=permiso)
                                user_modulo.save()
                            else:
                                user_modulo = UsersModulos.objects.create(modulo_id=modulo, user_perfil_id=user_perfil, enabled=0, adicionar=0,
                                                                          modificar=0, eliminar=0, anular=0, imprimir=0, permiso=0)
                                user_modulo.save()

                        self.error_operation = ''
                        return True

                    if type == 'modify':
                        if 'activo' in request.POST.keys():
                            status_user = 1  # django table
                            status_up = self.status_activo
                        else:
                            status_user = 0  # django table
                            status_up = self.status_inactivo

                        # recuperamos al usuario
                        user_perfil = UsersPerfiles.objects.get(pk=id)
                        usuario = apps.get_model('auth', 'User').objects.get(pk=user_perfil.user_id.id)
                        perfil = Perfiles.objects.get(pk=perfil_id)

                        usuario.first_name = first_name
                        usuario.last_name = last_name
                        usuario.email = email_txt
                        usuario.username = username_txt
                        # vemos si cambiar el password
                        if request.POST['cambiar'] == 'yes':
                            password_user = make_password(request.POST['password'])
                            usuario.password = password_user

                        usuario.is_active = status_user
                        usuario.save()

                        # actualizamos el perfil
                        user_perfil.perfil_id = perfil
                        user_perfil.punto_id = punto_id
                        user_perfil.caja_id = caja_id
                        user_perfil.notificacion = notificacion
                        user_perfil.updated_at = 'now'
                        user_perfil.status_id = status_up
                        user_perfil.save()

                        # usuarios modulos
                        UsersModulos.objects.filter(user_perfil_id=user_perfil).delete()

                        lista_modulos = Modulos.objects.all()

                        for modulo in lista_modulos:
                            # id modulo
                            modulo_id = modulo.modulo_id
                            # id user_modulo

                            nombre = 'modulo_' + str(modulo_id)
                            if nombre in request.POST.keys():
                                modulo_enabled = 1

                                if nombre + '_ad' in request.POST.keys():
                                    adicionar = 1
                                else:
                                    adicionar = 0

                                if nombre + '_mo' in request.POST.keys():
                                    modificar = 1
                                else:
                                    modificar = 0

                                if nombre + '_el' in request.POST.keys():
                                    eliminar = 1
                                else:
                                    eliminar = 0

                                if nombre + '_an' in request.POST.keys():
                                    anular = 1
                                else:
                                    anular = 0

                                if nombre + '_im' in request.POST.keys():
                                    imprimir = 1
                                else:
                                    imprimir = 0

                                if nombre + '_pe' in request.POST.keys():
                                    permiso = 1
                                else:
                                    permiso = 0

                                user_modulo = UsersModulos.objects.create(modulo_id=modulo, user_perfil_id=user_perfil, enabled=modulo_enabled, adicionar=adicionar,
                                                                          modificar=modificar, eliminar=eliminar, anular=anular, imprimir=imprimir, permiso=permiso)
                                user_modulo.save()
                            else:
                                user_modulo = UsersModulos.objects.create(modulo_id=modulo, user_perfil_id=user_perfil, enabled=0, adicionar=0,
                                                                          modificar=0, eliminar=0, anular=0, imprimir=0, permiso=0)
                                user_modulo.save()

                        self.error_operation = ""
                        return True

                    # default
                    self.error_operation = 'operation no valid'
                    return False
            else:
                self.error_operation = "Ya existe usuario o email: " + username_txt + " (" + email_txt + ")"
                return False

        except Exception as ex:
            print('ERROR, usuario: ' + str(ex))
            if type == 'add':
                self.error_operation = "Error al agregar el usuario, " + str(ex)
                return False

            if type == 'modify':
                self.error_operation = "Error al modificar el usuario, " + str(ex)
                return False

            # default
            self.error_operation = 'db operation no valid'
            return False

    def delete(self, id):
        """eliminamos"""
        try:
            with transaction.atomic():
                # users perfiles
                user_perfil = UsersPerfiles.objects.get(pk=id)
                user_perfil.status_id = self.status_eliminado
                user_perfil.deleted_at = 'now'
                user_perfil.save()

                # usuario
                modelo = apps.get_model('auth', 'User')
                objeto = modelo.objects.get(id=user_perfil.user_id.id)
                objeto.is_active = False
                objeto.save()

                # modelo = apps.get_model(self.modelo_app, self.modelo_name)
                # objeto = modelo.objects.get(pk=id)
                # objeto.is_active = False
                # objeto.save()

                # # users perfiles
                # user_perfil = UsersPerfiles.objects.get(user_id=objeto)
                # user_perfil.status_id = self.status_eliminado
                # user_perfil.save()

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = "Error al eliminar el usuario, " + str(ex)
            return False
