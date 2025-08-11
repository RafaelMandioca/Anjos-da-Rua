from django.contrib import admin
from .models import CodigoAcesso, UF, StatusAtendimento

# Register your models here.

admin.site.register(CodigoAcesso)
admin.site.register(UF)
admin.site.register(StatusAtendimento)