from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('cerrar/', views.cerrar_sesion, name='cerrar'),
    path('logout/', views.exit, name='exit'),
    path('lugares/', views.catalogo_lugares, name='catalogo'),
    path('lugares/agregar/', views.agregar_lugar, name='agregar_lugar'),
    path('lugares/<int:id>/', views.lugar_detalle, name='lugar_detalle'),
    path('lugares/<int:id>/editar/', views.editar_lugar, name='editar_lugar'),
    path('lugares/<int:id>/eliminar/', views.eliminar_lugar, name='eliminar_lugar'),
    path('acerca/', views.acerca, name='acerca'),
    path('contacto/', views.contacto, name='contacto'),
    path('blog/', views.blog, name='blog'),
    path('error/error_403/', views.error403, name='error_403'),
    path('mi-agenda/', views.mi_agenda, name='mi_agenda'),
    path('favoritos/', views.lugares_favoritos, name='favoritos'),
    path('proximos/', views.proximos_viajes, name='proximos'),
    path('agregar/<int:lugar_id>/', views.agregar_a_agenda, name='agregar_a_agenda'),
    path('favorito/<int:agenda_id>/', views.marcar_favorito, name='marcar_favorito'),
    path('agenda/editar/<int:agenda_id>/', views.editar_agenda, name='editar_agenda'),
    path('agenda/eliminar/<int:agenda_id>/', views.eliminar_agenda, name='eliminar_agenda'),
    path('filtrar/', views.filtrar_lugares, name='filtrar_lugares'),
]