from rest_framework import status
from rest_framework.response import Response
from authentication.models import Consultant
from rest_framework.views import APIView
from .permissions import (
    OnlyVisitor,
    OnlyConsultant,
)
from authentication.serializers import (
    ConsultantSerializer
)
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class ChatListView(generics.ListCreateAPIView):
    queryset = Consultant.objects.all()
    serializer_class = ConsultantSerializer
    permission_classes = [IsAuthenticated, OnlyVisitor]
    

class RoomAPI(APIView):
    
    permission_classes = [IsAuthenticated, OnlyVisitor] 
    def get(self, request, room_name):
        consultant = Consultant.objects.filter(user=room_name).first()
        if consultant.status=='ONLINE':
            return Response({
                'room_name': room_name
            })
        return Response({'error':'Error!'},status=status.HTTP_403_FORBIDDEN)


class ConsultantRoomAPI(APIView):
    
    permission_classes = [IsAuthenticated,OnlyConsultant]
    def get(self, request):
        
        return Response({'room_name': request.user.id})