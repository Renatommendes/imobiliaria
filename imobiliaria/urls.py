from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static  # Importe a função static
from clientes import views as clientes_views  # Importe as views do app clientes
from django.contrib.auth import views as auth_views
from clientes.views import user_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', clientes_views.home, name='home'),  # Adicione esta linha para a view home
    path('clientes/', include('clientes.urls')),
    path('usuarios/', user_list, name='user_list_direto'),
    path('financeiro/', include('financeiro.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),  # URLs de autenticação do Django
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Adicione esta linha