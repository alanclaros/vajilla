from django.urls import path
from pages.views import notificaciones_pagina, index

urlpatterns = [
    path('', index, name='index'),

    path('notificacionespagina/', notificaciones_pagina, name='notificaciones_pagina'),
]
