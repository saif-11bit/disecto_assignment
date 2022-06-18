from django.urls import path
from . import views

app_name='chat_app'

urlpatterns = [
    path('', views.ChatListView.as_view(), name="chat_list"),
    path('consultant/myroom/', views.ConsultantRoomAPI.as_view(), name='consultant-room'),
    path('<str:room_name>/', views.RoomAPI.as_view(), name='room'),
]
