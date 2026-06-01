from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "GenAI Health Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('chat/', include('chatbot.urls')),
    path('checker/', include('ml_module.urls')),
    path('image-analysis/', include('image_module.urls')),
    path('drugs/', include('drugs.urls')),
    path('admin-panel/', include('admin_panel.urls', namespace='admin_panel')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
