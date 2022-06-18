from django.shortcuts import render
import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import tweepy
import pytz
from authentication.models import Consultant

load_dotenv()

API_KEY=os.getenv('API_KEY')
API_SECRET=os.getenv('API_SECRET')
ACCESS_TOKEN=os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET=os.getenv('ACCESS_TOKEN_SECRET')
COUNTRIES_API=os.getenv('COUNTRIES_API')
COVID_API=os.getenv('COVID_API')

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, callback=None)
api = tweepy.API(auth)


def countrypickerview(request):
    response=requests.get(COUNTRIES_API).json()
    return render(request, 'country_picker.html', {'data': response})


def covidtrackview(request):
    country = request.GET.get('country')
    current_time = datetime.now()
    frm = (current_time-timedelta(7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = f"{COVID_API}{country}/status/confirmed/date/{frm}"
    
    data=requests.get(url).json()
    active_cases = [i['Active'] for i in data]
    dates = [(i['Date']) for i in data]
    return render(request, 'covid_tracker.html', {'data': data, 'room_name': 'track', 'active_cases':active_cases, 'dates':dates})


def twitter_tweets(request):
    current_time = datetime.now()
    a_day_before = current_time - timedelta(days=1)
    tweets = [i for i in api.search_tweets(q="#COVID19 #OMICRON", result_type='recent', count=20) if i.created_at.replace(tzinfo=pytz.utc) >= a_day_before.replace(tzinfo=pytz.utc)]
    return render(request,'tweeter_tweets.html',{'tweets_context':tweets,'a_day_before':a_day_before})


def chat_list_view(request):
    if request.user.is_authenticated and request.user.is_visitor:
        consultants = Consultant.objects.all()
        return render(request, 'chat_list.html', {'consultants': consultants})


def room(request, room_name):
    if request.user.is_authenticated and request.user.is_visitor:
        return render(request, 'room.html', {
            'room_name': room_name
        })
    
def consultant_room(request):
    if request.user.is_authenticated and request.user.is_consultant:
        return render(request, 'room.html', {
            'room_name': request.user.id
        })
