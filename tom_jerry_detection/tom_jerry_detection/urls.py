from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('detector/', include('detector.urls')),  # Isso já está correto
    path('', include('detector.urls')),  # Adiciona esta linha para corresponder ao caminho vazio
]

# Servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
