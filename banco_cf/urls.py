from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404, handler403


urlpatterns = [
    path('cards/', include('cards.urls')),
    path('', include('accounts.urls')),
    path('admin', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Handling 404 and 403 errors
handler404 = 'cards.views.error_404'
handler403 = 'cards.views.error_404'
