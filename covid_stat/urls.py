from django.urls import path
from . import views

app_name='covid_stat'

urlpatterns = [
    path('', views.CountryPickerAPIView.as_view(), name='countries'),
    path('covid/', views.CovidTrackerAPIView.as_view(), name='covidtrack'),
    path('tweets/', views.TwitterAPIView.as_view(), name='tweets'),
]
