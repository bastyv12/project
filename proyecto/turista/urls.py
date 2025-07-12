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
]