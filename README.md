# Disecto Task
Covid-Consultancy-Protal

## How to use it
1. Run this application:
    1. python manage.py makemigrations
    2. python manage.py migrate
    3. python manage.py runserver
    4. celery -A covid_consultancy.celery beat -l info
    5. celery -A covid_consultancy.celery worker --pool=solo -l info
2. Go to: http://localhost:8000/ to check docs(used swagger UI)
3. A demo version of this application is available on: http://localhost:8000/demo
4. Check different urls of demo app http://localhost:8000/demo/{}
5. To check covid stats:
    1. Select a country: http://localhost:8000/demo/countrypicker
    2. Click of submit
    3. Chart and stats will be shown of selected country
6. To consult with consultant:
    1. Goto: http://localhost:8000/demo/countrypicker/chat_list
    2. List Consultant will be shown with their current status
    3. Click on any online consultant you want to chat
7. If you are visitor:
    1. Goto: http://localhost:8000/demo/countrypicker/myroom
    2. chat with visitors
