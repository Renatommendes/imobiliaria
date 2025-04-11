from django.urls import path
from . import views
from .views import cadastrar_cliente, listar_clientes, excluir_cliente
from .views import user_list, editar_usuario, excluir_usuario
from .views import contratos, adicionar_contrato, listar_contratos, editar_contrato, excluir_contrato
from .views import criar_ordem_contrato,adicionar_fase,pagina_processos,  listar_ordens_contrato,processos, editar_arquivo_ordem, upload_contrato, submeter_arquivo, editar_ordem_contrato, excluir_ordem_contrato, visualizar_ordem_contrato, editar_upload_contrato, criar_etapa, avancar_etapa

urlpatterns = [
    path('listar/', listar_clientes, name='listar_clientes'),
    path('novo/', cadastrar_cliente, name='cadastrar_cliente'), 
    path('editar/<int:pk>/', cadastrar_cliente, name='editar_cliente'),
    path('signup/', views.signup, name='signup'),  # Adicione esta linha para a view signup
    path('excluir/<int:pk>/', excluir_cliente, name='excluir_cliente'),
    path("usuarios/", user_list, name="user_list"),
    path("usuarios/editar/<int:user_id>/", editar_usuario, name="editar_usuario"),
    path("usuarios/excluir/<int:user_id>/", excluir_usuario, name="excluir_usuario"),
    path('contratos/', contratos, name='contratos'),
    path("contratos/adicionar/", adicionar_contrato, name="adicionar_contrato"),
    path("contratos/listar_contratos", listar_contratos, name="listar_contratos"),
    path("contratos/editar_contratos/<int:contrato_id>/", editar_contrato, name="editar_contrato"),
    path("contratos/excluir_contrato/<int:contrato_id>/", excluir_contrato, name="excluir_contrato"),
    path('contratos/listar_ordens/', views.listar_ordens_contrato, name='listar_ordens_contrato'),
    path('contratos/criar/', views.criar_ordem_contrato, name='criar_ordem_contrato'),  # URL para criar
    path("contratos/upload/<int:ordem_id>/", upload_contrato, name="upload_contrato"),
    path('contratos/editar_ordem/<int:id>/', views.editar_ordem_contrato, name='editar_ordem_contrato'),  # URL para editar
    path("contratos/excluir_ordem/<int:ordem_id>/", excluir_ordem_contrato, name="excluir_ordem_contrato"),
    path('contratos/visualizar/<int:ordem_id>/', views.visualizar_ordem_contrato, name='visualizar_ordem_contrato'),
    path('contratos/editar_upload/<int:ordem_id>/', editar_upload_contrato, name='editar_upload_contrato'),
    path('contratos/criar_etapa/<int:usuario_id>/', criar_etapa, name='criar_etapa'),
    path('avancar_etapa/', views.avancar_etapa, name='avancar_etapa'),
    path("contratos/submeter/<int:ordem_id>/", submeter_arquivo, name="submeter_arquivo"),
    path("contratos/editar-arquivo/<int:ordem_id>/", editar_arquivo_ordem, name="editar_arquivo_ordem"),
    path('processos/', pagina_processos, name='pagina_processos'),
    path('processos/adicionar_fase/', adicionar_fase, name='adicionar_fase'),
    path('processos/adicionar_item/', views.adicionar_item_fase, name='adicionar_item_fase'),
    path('validar_etapa/<int:etapa_id>/', views.validar_etapa, name='validar_etapa'),
]