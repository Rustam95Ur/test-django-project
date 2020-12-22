"""pg_game URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from pg_game.views import login_form, login_save
from pg_game.api_settings import ENABLE_FRONT
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

if ENABLE_FRONT:
    urlpatterns = [
        path('', include('histories.urls')),
        path('visits/', include('visits.urls')),
        path('settings/', include('settings.urls')),
        path('login', login_form, name='login_form'),
        path('login/save', login_save, name='login'),
        path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
        path('admin/', admin.site.urls),
    ]
else:
    schema_view = get_schema_view(
        openapi.Info(
            title="P&G GAME API",
            default_version='v1',
            terms_of_service='https://teams.microsoft.com/l/channel/19%3a0500266473c54945833ea4ea01535ba7%40thread.tacv2/%25D0%259E%25D0%25B1%25D1%2589%25D0%25B8%25D0%25B9?groupId=9f076737-c1e4-45d8-8af6-f086440fc090&tenantId=eb7cf5a2-73f5-4be5-8eda-c0264acb6e9e',
            description="API для итеграции c мобильным приложением.",
            contact=openapi.Contact(email="kurbanov.rustam@applecity.kz"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
    urlpatterns = [
        path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        path('api/v1/', include('api.urls')),
    ]
