# anjosdaruaproject/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

# CORRETO: Importe diretamente do arquivo específico dentro do pacote views.
from core.views.cadastros_gerais import index

urlpatterns = [
    path('admin/', admin.site.urls),
    # Agora a referência a 'index' funcionará
    path('', index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='core/auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('core/', include('core.urls')), 
]