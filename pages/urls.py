from django.urls import path
from pages.views import notificaciones_pagina, index, notificaciones_push

urlpatterns = [
    path('', index, name='index'),

    path('notificacionespagina/', notificaciones_pagina, name='notificaciones_pagina'),
    path('notificacionespush/', notificaciones_push, name='notificaciones_push'),
]
