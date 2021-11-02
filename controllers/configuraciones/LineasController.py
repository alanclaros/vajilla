from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from utils.validators import validate_number_int, validate_string
from controllers.SystemController import SystemController
import os
from os import remove

# imagenes
from django.core.files.base import ContentFile
from PIL import Image


class LineasController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Lineas'
        self.modelo_id = 'linea_id'
        self.modelo_app = 'configuraciones'
        self.modulo_id = settings.MOD_LINEAS

        # variables de session
        self.modulo_session = "lineas"
        self.columnas.append('linea')
        self.columnas.append('codigo')

        self.variables_filtros.append('search_linea')
        self.variables_filtros.append('search_codigo')

        self.variables_filtros_defecto['search_linea'] = ''
        self.variables_filtros_defecto['search_codigo'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {'productos': 'Productos'}

        # control del formulario
        self.control_form = "txt|2|S|linea|Linea"
        self.control_form += ";txt|2|S|codigo|Codigo"

    def index(self, request):
        DefaultValues.index(self, request)
        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.activo, self.inactivo]

        # linea
        if self.variables_filtros_values['search_linea'].strip() != "":
            self.filtros_modulo['linea__icontains'] = self.variables_filtros_values['search_linea'].strip()

        # codigo
        if self.variables_filtros_values['search_codigo'].strip() != "":
            self.filtros_modulo['codigo__icontains'] = self.variables_filtros_values['search_codigo'].strip()

        # paginacion, paginas y definiendo el LIMIT *,*
        self.pagination()
        # asigamos la paginacion a la session
        request.session[self.modulo_session]['pages_list'] = self.pages_list

        # recuperamos los datos
        return self.get_list()

    def is_in_db(self, id, nuevo_valor):
        """verificamos si existe en la base de datos"""
        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        filtros = {}
        filtros['status_id_id__in'] = [self.activo, self.inactivo]
        filtros['linea__in'] = [nuevo_valor]
        if id > 0:
            cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        else:
            cantidad = modelo.objects.filter(**filtros).count()

        # si no existe
        if cantidad > 0:
            return True

        return False

    def save(self, request, type='add'):
        """aniadimos una nueva linea"""
        system_controller = SystemController()

        try:
            linea_txt = validate_string('linea', request.POST['linea'], remove_specials='yes')
            codigo_txt = validate_string('codigo', request.POST['codigo'], remove_specials='yes')
            descripcion = validate_string('descripcion', request.POST['descripcion'], remove_specials='yes', len_zero='yes')
            linea_superior_id = validate_number_int('linea_superior_id', request.POST['linea_superior_id'])
            id = validate_number_int('id', request.POST['id'], len_zero='yes')

            if not self.is_in_db(id, linea_txt):
                if 'activo' in request.POST.keys():
                    status_linea = self.status_activo
                else:
                    status_linea = self.status_inactivo

                if 'linea_principal' in request.POST.keys():
                    linea_principal = 1
                else:
                    linea_principal = 0

                aux = {}
                aux['nombre_archivo'] = ''
                aux['nombre_archivo_thumb'] = ''
                if 'imagen1' in request.FILES.keys():
                    uploaded_filename = request.FILES['imagen1'].name.strip()

                    if uploaded_filename != '':
                        aux = system_controller.nombre_imagen('lineas', uploaded_filename)
                        # aux = system_controller self.nombre_imagen(uploaded_filename)

                        full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'lineas', aux['nombre_archivo'])
                        full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'lineas', aux['nombre_archivo_thumb'])

                        fout = open(full_filename, 'wb+')
                        file_content = ContentFile(request.FILES['imagen1'].read())
                        for chunk in file_content.chunks():
                            fout.write(chunk)
                        fout.close()

                        # creamos el thumb
                        imagen = Image.open(full_filename)
                        max_size = (settings.PRODUCTOS_THUMB_WIDTH, settings.PRODUCTOS_THUMB_HEIGHT)
                        imagen.thumbnail(max_size)
                        imagen.save(full_filename_thumb)

                if type == 'add':
                    linea = apps.get_model('configuraciones', 'Lineas').objects.create(linea=linea_txt, codigo=codigo_txt, linea_principal=linea_principal, linea_superior_id=linea_superior_id,
                                                                                       descripcion=descripcion, imagen=aux['nombre_archivo'], imagen_thumb=aux['nombre_archivo_thumb'], status_id=status_linea, created_at='now', updated_at='now')
                    linea.save()
                    self.error_operation = ""
                    return True

                if type == 'modify':
                    linea = apps.get_model('configuraciones', 'Lineas').objects.get(pk=id)
                    # verificamos imagen
                    if linea.imagen != '':
                        full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'lineas', linea.imagen)
                        full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'lineas', linea.imagen_thumb)

                        if os.path.exists(full_filename):
                            remove(full_filename)
                        if os.path.exists(full_filename_thumb):
                            remove(full_filename_thumb)

                    if aux['nombre_archivo'] != '':
                        # guardamos la nueva imagen
                        linea.imagen = aux['nombre_archivo']
                        linea.imagen_thumb = aux['nombre_archivo_thumb']

                    # datos
                    linea.status_id = status_linea
                    linea.linea = linea_txt
                    linea.codigo = codigo_txt
                    linea.linea_principal = linea_principal
                    linea.linea_superior_id = linea_superior_id
                    linea.descripcion = descripcion
                    linea.updated_at = 'now'
                    linea.save()
                    self.error_operation = ""
                    return True

                self.error_operation = 'Operation no valid'
                return False

            else:
                self.error_operation = "Ya existe esta linea: " + linea_txt
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar la linea, " + str(ex)
            return False
