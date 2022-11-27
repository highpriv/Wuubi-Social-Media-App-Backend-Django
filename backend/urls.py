from django.urls import path, re_path
from django.conf.urls import include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    path('admin/clearcache/', include('clearcache.urls')),
    re_path(r'^admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('tr/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('token-auth/', obtain_jwt_token),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
