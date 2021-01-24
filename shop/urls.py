from django.urls import path
from shop import views as shop_views

urlpatterns = [
    path('mercado/',shop_views.mercado,name='mercado'),
    path('suscripciones/',shop_views.suscripcion,name='suscripciones'),
    path('cliente/',shop_views.crear_cliente,name='crear_cliente'),
    path('ver-cliente/',shop_views.ver_clientes,name='ver-cliente')]
