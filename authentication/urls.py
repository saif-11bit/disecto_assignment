from django.urls import path
from .views import (
    ConsultantRegisterView,
    VisitorRegisterView,
    VerifyEmail,
    LoginView,
    LogoutAPIView,
    WorkingPeriodView
)

app_name='authentication_app'

urlpatterns = [
    path('conultant-register/',ConsultantRegisterView.as_view(),name='conultant-register'),
    path('visitor-register/',VisitorRegisterView.as_view(),name='visitor-register'),
    path('verify-email/',VerifyEmail.as_view(),name='verify-email'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutAPIView.as_view(),name='logout'),
    path('working-period/',WorkingPeriodView.as_view(),name='working-period'),
]
