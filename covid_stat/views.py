from django.shortcuts import render
import requests
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
import tweepy
import pytz
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY=os.getenv('API_KEY')
API_SECRET=os.getenv('API_SECRET')
ACCESS_TOKEN=os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET=os.getenv('ACCESS_TOKEN_SECRET')
COVID_API=os.getenv('COVID_API')
COUNTRIES_API=os.getenv('COUNTRIES_API')

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, callback=None)
api = tweepy.API(auth)


class CountryPickerAPIView(APIView):
    
    def get(self, request):
        response = requests.get(COUNTRIES_API).json()
        return Response(response)


class CovidTrackerAPIView(APIView):
    
    def get(self, request):
        data = self.request.query_params
        country = data.get('country')
        current_time = datetime.now()
        # to = (current_time-timedelta(1)).strftime("%Y-%m-%d")
        frm = (current_time-timedelta(7)).strftime("%Y-%m-%d")

        url = f"{COVID_API}{country}/status/confirmed/date/{frm}"
        
        data=requests.get(url).json()
        return Response({'data':data, 'room_name':'track'})
    
    
class TwitterAPIView(APIView):
    
    def get(self, request):
        tweets = []
        current_time = datetime.now()
        a_day_before = current_time - timedelta(days=1)
        for i in api.search_tweets(q="#COVID19 #OMICRON", result_type='recent', count=20):
            if i.created_at.replace(tzinfo=pytz.utc) >= a_day_before.replace(tzinfo=pytz.utc):
                print(i.text)
                tweets.append({'id':i.id, 'text':i.text, 'tweeted_at':i.created_at})
                
        return Response(
            {'tweets': tweets}
        )
