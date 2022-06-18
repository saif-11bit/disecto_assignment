from django.urls import path
from . import views

app_name='demo'

urlpatterns = [
    path('countrypicker/', views.countrypickerview, name="countrypicker"),
    path('covid/', views.covidtrackview, name="covid"),
    path('twitter_tweets/', views.twitter_tweets, name="twitter_tweets"),
    path('chat_list/', views.chat_list_view, name="chat_list"),
    path('myroom/', views.consultant_room, name="consultant_room"),
    path('<str:room_name>/', views.room, name="room"),
]
