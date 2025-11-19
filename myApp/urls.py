from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('detalle_sala/<int:id>', views.detalle_sala, name='detalle_sala'),
    path('crear_reserva/', views.crear_reserva, name='crear_reserva'),
]