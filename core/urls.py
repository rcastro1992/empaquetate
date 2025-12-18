from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from web.views import UnifiedLoginView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Sitio público
    path('', include('web.urls')),

    # LOGIN unificado
    path('login/', UnifiedLoginView.as_view(), name='login'),

    # LOGOUT unificado
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
