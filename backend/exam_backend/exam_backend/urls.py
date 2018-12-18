"""exam_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from django.conf.urls.static import static
from django.conf import settings
import debug_toolbar

register_urlpatterns = [
    path('accounts/', include('rest_registration.api.urls')),
]

urlpatterns = [
    path('debug/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    url(r'^token-auth/', obtain_jwt_token),
    url(r'^token-verify/', verify_jwt_token),
    url(r'^token-refresh/', refresh_jwt_token),
    path('api/', include(register_urlpatterns)),
    path('api/', include('exam.urls')),
    path('api/', include('exam_auth.urls')),
    path('api/', include('exam_manage.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
