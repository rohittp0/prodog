from typing import Any

from django.conf import settings
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

urlpatterns = [
    path('healthcheck/', lambda request: JsonResponse({"status": "ok"})),
]

if settings.DEBUG:
    schema_view: Any = get_schema_view(
        openapi.Info(
            title="Lascade API",
            default_version='v0',
            description="API documentation for Lascade Server",
        ),
        public=False,
        permission_classes=[permissions.IsAdminUser],  # Ensures we have a staff user
    )

    urlpatterns += [
        path('admin/', admin.site.urls),
        path(r'', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
        path(r'docs', schema_view.with_ui('redoc'), name='schema-redoc-ui'),
        path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    ]
