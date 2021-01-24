from django.urls import path
from openpay_shop import views as openpay_views

urlpatterns = [
    path('tienda/',openpay_views.compra,name='tienda'),
    path('suscripcion/',openpay_views.suscripcion,name='suscripcion'),
    path('nuevo-cliente/',openpay_views.nuevo_cliente,name='nuevo-cliente'),
    path('planes/',openpay_views.planes,name='planes'),
    path('registro-cliente/<str:plan>',openpay_views.registro_cliente,name='registro_cliente'),
    ]
