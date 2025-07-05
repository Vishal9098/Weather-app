from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):
    if request.method == 'POST' and 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'indore'

    weather_api_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=3f9f021f3d5e3fc1006dea85eb6b9cdf'
    PARAMS = {'units': 'metric'}

    # Replace with your actual Google API key
    GOOGLE_API_KEY = 'YOUR_GOOGLE_API_KEY'
    SEARCH_ENGINE_ID = '26cd83dd9c4724988'

    # Prepare image search query
    query = city + " 1920x1080"
    start = 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    try:
        image_data = requests.get(city_url).json()
        search_items = image_data.get("items")
        image_url = search_items[1]['link'] if search_items and len(search_items) > 1 else ""
    except Exception as e:
        image_url = ""
        print("Image fetch error:", e)

    try:
        weather_data = requests.get(weather_api_url, params=PARAMS).json()
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except KeyError:
        messages.error(request, 'Entered data is not available to API')
        day = datetime.date.today()
        return render(request, 'weatherapp/index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'indore',
            'exception_occurred': True,
            'image_url': image_url
        })






















    