from celery import shared_task
from channels.layers import get_channel_layer
import asyncio
import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

COVID_API=os.getenv('COVID_API')

@shared_task(bind=True)
def update_covid_stat(self, countries):
    current_time = datetime.now()
    to = current_time.strftime("%Y-%m-%d")
    frm = (current_time-timedelta(7)).strftime("%Y-%m-%d")

    url = f"{COVID_API}{countries}/status/confirmed/date/{frm}"

    data=requests.get(url).json()
        
    # send data to group
    channel_layer = get_channel_layer()
    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)
    loop.run_until_complete(channel_layer.group_send("covid_track", {
        'type': 'send_covid_stats_update',
        'message': data
    }))

    return 'Done'
