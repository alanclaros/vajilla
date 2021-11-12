# webpush
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from webpush import send_user_notification

from pages.views import lista_para_notificar
from django.apps import apps

# @require_POST
# @csrf_exempt # del metodo original


def send_push(request):

    # # metodo original
    # try:
    #     body = request.body
    #     data = json.loads(body)
    #
    #     if 'head' not in data or 'body' not in data or 'id' not in data:
    #         return JsonResponse(status=400, data={"message": "Invalid data format"})
    #
    #     user_id = data['id']
    #     user = get_object_or_404(User, pk=user_id)
    #     payload = {'head': data['head'], 'body': data['body']}
    #     send_user_notification(user=user, payload=payload, ttl=1000)
    #
    #     return JsonResponse(status=200, data={"message": "Web push successful"})
    # except TypeError:
    #     return JsonResponse(status=500, data={"message": "An error occurred"})

    #print('gett....', request.GET.keys())
    if 'keypush' in request.GET.keys():
        # print('aaaaaaaaa')
        keypush = request.GET['keypush']
        #print('bbbbbb: ', keypush)
        if keypush != settings.KEY_PUSH:
            return JsonResponse(status=500, data={"message": "Send Webpush Error"})

        try:
            # usuarios autenticados
            user_adm = User.objects.get(pk=1)
            listado = lista_para_notificar(user_adm)

            lista_entregar = ''
            lista_recoger = ''
            lista_finalizar = ''
            for notificacion in listado['lista_notificaciones']:
                if notificacion['tipo'] == 'E':
                    lista_entregar += notificacion['tipo_notificacion'] + '|' + notificacion['descripcion'] + '||'

                if notificacion['tipo'] == 'R':
                    lista_recoger += notificacion['tipo_notificacion'] + '|' + notificacion['descripcion'] + '||'

                if notificacion['tipo'] == 'F':
                    lista_finalizar += notificacion['tipo_notificacion'] + '|' + notificacion['descripcion'] + '||'

            if len(lista_entregar) > 0:
                lista_entregar = lista_entregar[0:len(lista_entregar)-2]

            if len(lista_recoger) > 0:
                lista_recoger = lista_recoger[0:len(lista_recoger)-2]

            if len(lista_finalizar) > 0:
                lista_finalizar = lista_finalizar[0:len(lista_finalizar)-2]

            # lista de usuarios para mandar notificaciones
            status_activo = apps.get_model('status', 'Status').objects.get(pk=1)
            lista_user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.filter(status_id=status_activo, notificacion=1)
            lista_up_admin = ''
            lista_up_supervisor = ''
            lista_up_almacen = ''
            lista_up_cajero = ''

            for user_perfil in lista_user_perfil:
                if user_perfil.perfil_id.perfil_id == settings.PERFIL_ADMIN:
                    lista_up_admin += str(user_perfil.user_id.id) + '|'

                if user_perfil.perfil_id.perfil_id == settings.PERFIL_SUPERVISOR:
                    lista_up_supervisor += str(user_perfil.user_id.id) + '|'

                if user_perfil.perfil_id.perfil_id == settings.PERFIL_ALMACEN:
                    lista_up_almacen += str(user_perfil.user_id.id) + '|'

                if user_perfil.perfil_id.perfil_id == settings.PERFIL_CAJERO:
                    lista_up_cajero += str(user_perfil.user_id.id) + '|'

            #print('lista up admin: ', lista_up_admin)
            if len(lista_up_admin) > 0:
                lista_up_admin = lista_up_admin[0:len(lista_up_admin)-1]

            if len(lista_up_supervisor) > 0:
                lista_up_supervisor = lista_up_supervisor[0:len(lista_up_supervisor)-1]

            if len(lista_up_almacen) > 0:
                lista_up_almacen = lista_up_almacen[0:len(lista_up_almacen)-1]

            if len(lista_up_cajero) > 0:
                lista_up_cajero = lista_up_cajero[0:len(lista_up_cajero)-1]

            # webpush
            # entregas
            if len(lista_entregar) > 0:
                lista_usuarios = ''
                lista_usuarios += lista_up_admin + '|'
                lista_usuarios += lista_up_supervisor + '|'
                lista_usuarios += lista_up_almacen + '|'
                #lista_usuarios += lista_up_cajero + '|'

                if len(lista_usuarios) > 0:
                    lista_usuarios = lista_usuarios[0:len(lista_usuarios)-1]

                    lista_send = lista_entregar.split('||')
                    for notificacion in lista_send:
                        datos_notif = notificacion.split('|')
                        tipo = datos_notif[0]
                        notif = datos_notif[1]
                        if tipo == 'warning':
                            payload = {'head': 'Aviso - E', 'body': notif}
                            division_user = lista_usuarios.split('|')
                            for user_send in division_user:
                                try:
                                    user = get_object_or_404(User, pk=int(user_send))
                                    send_user_notification(user=user, payload=payload, ttl=1000)

                                except Exception as ex:
                                    print('Error send webpush: ', str(ex))

                        if tipo == 'danger':
                            payload = {'head': '*Alerta* - E', 'body': notif}
                            division_user = lista_usuarios.split('|')
                            for user_send in division_user:
                                try:
                                    user = get_object_or_404(User, pk=int(user_send))
                                    send_user_notification(user=user, payload=payload, ttl=1000)

                                except Exception as ex:
                                    print('Error send webpush: ', str(ex))

            # recogos
            if len(lista_recoger) > 0:
                lista_usuarios = ''
                lista_usuarios += lista_up_admin + '|'
                lista_usuarios += lista_up_supervisor + '|'
                lista_usuarios += lista_up_almacen + '|'
                #lista_usuarios += lista_up_cajero + '|'

                if len(lista_usuarios) > 0:
                    lista_usuarios = lista_usuarios[0:len(lista_usuarios)-1]

                    lista_send = lista_recoger.split('||')
                    for notificacion in lista_send:
                        datos_notif = notificacion.split('|')
                        tipo = datos_notif[0]
                        notif = datos_notif[1]
                        if tipo == 'warning':
                            payload = {'head': 'Aviso - R', 'body': notif}
                            division_user = lista_usuarios.split('|')
                            for user_send in division_user:
                                try:
                                    user = get_object_or_404(User, pk=int(user_send))
                                    send_user_notification(user=user, payload=payload, ttl=1000)

                                except Exception as ex:
                                    print('Error send webpush: ', str(ex))

                        if tipo == 'danger':
                            payload = {'head': '*Alerta* - R', 'body': notif}
                            division_user = lista_usuarios.split('|')
                            for user_send in division_user:
                                try:
                                    user = get_object_or_404(User, pk=int(user_send))
                                    send_user_notification(user=user, payload=payload, ttl=1000)

                                except Exception as ex:
                                    print('Error send webpush: ', str(ex))

            # finalizar
            if len(lista_finalizar) > 0:
                lista_usuarios = ''
                lista_usuarios += lista_up_admin + '|'
                lista_usuarios += lista_up_supervisor + '|'
                #lista_usuarios += lista_up_almacen + '|'
                lista_usuarios += lista_up_cajero + '|'

                if len(lista_usuarios) > 0:
                    lista_usuarios = lista_usuarios[0:len(lista_usuarios)-1]

                    lista_send = lista_finalizar.split('||')
                    for notificacion in lista_send:
                        datos_notif = notificacion.split('|')
                        tipo = datos_notif[0]
                        notif = datos_notif[1]
                        if tipo == 'warning':
                            payload = {'head': 'Aviso - F', 'body': notif}
                            division_user = lista_usuarios.split('|')
                            for user_send in division_user:
                                try:
                                    user = get_object_or_404(User, pk=int(user_send))
                                    send_user_notification(user=user, payload=payload, ttl=1000)

                                except Exception as ex:
                                    print('Error send webpush: ', str(ex))

                        if tipo == 'danger':
                            payload = {'head': '*Alerta* - F', 'body': notif}
                            division_user = lista_usuarios.split('|')
                            for user_send in division_user:
                                try:
                                    user = get_object_or_404(User, pk=int(user_send))
                                    send_user_notification(user=user, payload=payload, ttl=1000)

                                except Exception as ex:
                                    print('Error send webpush: ', str(ex))

            return JsonResponse(status=200, data={"message": "Web push successful"})

        except TypeError:
            return JsonResponse(status=500, data={"message": "Send Webpush Error 2"})

    try:
        if not 'head' in request.POST.keys() or not 'body' in request.POST.keys() or not 'id' in request.POST.keys():
            return JsonResponse(status=500, data={"message": "Send Webpush Error, error de parametros "})

        user_id = request.POST['id']
        head = request.POST['head']
        body = request.POST['body']
        payload = {'head': head, 'body': body}

        division_user = user_id.split('|')

        for user_send in division_user:
            # print('user send: ', user_send)
            try:
                user = get_object_or_404(User, pk=int(user_send))

                send_user_notification(user=user, payload=payload, ttl=1000)

            except Exception as ex:
                print('Error send webpush: ', str(ex))

        return JsonResponse(status=200, data={"message": "Web push successful"})

    except TypeError:
        return JsonResponse(status=500, data={"message": "Send Webpush Error"})
