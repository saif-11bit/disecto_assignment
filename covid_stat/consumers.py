import json
from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import copy

class CovidStatsConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def addToCeleryBeat(self, countries):
        task_name = f"{countries}_task"
        task = PeriodicTask.objects.filter(name=task_name).first()
        if task:
            pass
        else:
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=20,
                period=IntervalSchedule.SECONDS
            )
            task = PeriodicTask.objects.create(
                interval=schedule,
                name=task_name,
                task="covid_stat.tasks.update_covid_stat",
                args=json.dumps([countries])
            )
            self.scope['cookies'][task_name] = 1
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'covid_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # parse queryString
        query_params = parse_qs(self.scope["query_string"].decode())

        countries = query_params["country"]
        
        if len(countries) == 1:
            self.scope['cookies']['country'] = countries[0]
            await self.addToCeleryBeat(countries[0])

        await self.accept()
        
    
    async def disconnect(self, close_code):
        # remove from cookies
        del self.scope['cookies']['country']
        print("Deleted:", self.scope["cookies"])
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
                'type': 'send_update',
                'message': message
            }
        )

    # Receive message from room group
    async def send_covid_stats_update(self, event):
        message = event['message']
        message = copy.copy(message)
        country_selected = self.scope['cookies']['country']
        if message[0]['Country'] == country_selected:
        
            print('running......')
            # Send message to WebSocket
            await self.send(text_data=json.dumps(message))
