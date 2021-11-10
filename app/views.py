# webpush
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from webpush import send_user_notification


@require_POST
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
