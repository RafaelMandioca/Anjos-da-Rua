# anjosdaruaproject/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

# Importe diretamente do arquivo específico
from core.views.cadastros_gerais import index
from core.views import registro

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='core/auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registro/', registro.registro_veterinario, name='registro_veterinario'),
    
    # A linha abaixo foi alterada para remover o prefixo 'core/'
    path('', include('core.urls')), 
]