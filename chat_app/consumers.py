from datetime import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from authentication.models import Consultant, WorkingPeriod


class ChatConsumer(AsyncWebsocketConsumer):
    
    @sync_to_async
    def track_working_period(self, user_id, disconnect_time):
        start_time = self.scope['cookies']['start_time']
        workingperiod = WorkingPeriod()
        workingperiod.consultant = Consultant.objects.get(user_id=user_id)
        workingperiod.start_time=start_time
        workingperiod.end_time=disconnect_time
        workingperiod.save()
        del self.scope['cookies']['start_time']
    
    @sync_to_async
    def check_consultant_online(self, room_name):
        consultant = Consultant.objects.filter(user=room_name).first()
        if consultant.status == 'BUSY' or consultant.status == 'ONLINE':
            return True
        return False
    
    
    @sync_to_async
    def update_consultant_status_to_online(self, user_id):
        consultant = Consultant.objects.filter(user=user_id).first()
        consultant.status = 'ONLINE'
        consultant.save()
        
    @sync_to_async
    def update_consultant_status_to_busy(self, room_name):
        consultant = Consultant.objects.filter(user=room_name).first()
        consultant.status = 'BUSY'
        consultant.save()
    
    @sync_to_async
    def update_consultant_status_to_offline(self, user_id):
        consultant = Consultant.objects.filter(user=user_id).first()
        consultant.status = 'OFFLINE'
        consultant.save()


    @sync_to_async
    def check_if_consultant_or_visitor_disconnect(self, room_name, user_id):
        # check if consultant
        consultant = Consultant.objects.filter(user=user_id).first()

        if consultant:
            # change consultant status to offline
            consultant.status = 'OFFLINE'
            consultant.save()
        else:
            # check if consultant is online or not
            consultant = Consultant.objects.filter(user=room_name).first()
            if consultant.status == 'BUSY':
                consultant.status = 'ONLINE'
                consultant.save()
    
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        self.user_id = self.scope['user'].id

        if self.scope['user'].is_consultant:
            await self.update_consultant_status_to_online(self.user_id)
            self.scope['cookies']['start_time'] = datetime.now()
        elif self.scope['user'].is_visitor:
            await self.update_consultant_status_to_busy(self.room_name)

        await self.accept()
        

    async def disconnect(self, close_code):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        disconnect_time = datetime.now()
        self.user_id = self.scope['user'].id

        if self.scope['user'].is_consultant:
            await self.update_consultant_status_to_offline(self.user_id)
            await self.track_working_period(self.user_id, disconnect_time)
        elif self.scope['user'].is_visitor:
            is_online = await self.check_consultant_online(self.room_name)
            if is_online:
                await self.update_consultant_status_to_online(self.room_name)
        
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
