from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Disecto API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.ourapp.com/policies/terms/",
        contact=openapi.Contact(email="contact@expenses.local"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo/', include('demo.urls', namespace='demo')),
    path('stats/', include('covid_stat.urls', namespace='covid_stat')),
    path('chat/', include('chat_app.urls', namespace='chat_app')),
    path('', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
    path('api/api.json/', schema_view.without_ui(cache_timeout=0),name='schema-swagger-ui'),
    path('auth/', include('authentication.urls', namespace='authentication_app')),
    path('redoc/', schema_view.with_ui('redoc',cache_timeout=0), name='schema-redoc'),
]
