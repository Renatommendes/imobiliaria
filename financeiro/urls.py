from django.urls import path
from .views import boletos, editar_boleto, excluir_boleto

urlpatterns = [
    path('boletos/', boletos, name='boletos'),
    path('boletos/editar/<int:boleto_id>/', editar_boleto, name='editar_boleto'),
    path('boletos/excluir/<int:boleto_id>/', excluir_boleto, name='excluir_boleto'),
]
