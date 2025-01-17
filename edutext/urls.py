"""
URL configuration for edutext project.

This module defines the root URL configuration for the EduText project.
It includes:
- Admin interface URLs
- API v1 endpoints for authentication and core functionality
- API documentation endpoints (Swagger/ReDoc)
- Media file serving in development

For more information on URL configuration, see:
https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),
    
    # API v1 endpoints
    path('api/v1/', include('authentication.urls')),
    path('api/v1/', include('core.urls')),
    
    # API documentation endpoints
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # Raw OpenAPI schema
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger UI
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # ReDoc UI
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files in development
