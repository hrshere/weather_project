import datetime

import requests
from django.shortcuts import render


# Create your views here.
def index(request):
    API_KEY = ""#put your API key here
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    # refer -> https://openweathermap.org/forecast5
    forcast_url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}"#updated url --> its free

    if request.method == "POST":
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)


        # to tackle KeyError at /'coord'--> we won't call the API if no value for city1 provided
        if city1:
            weather_data1, daily_forcasts1 = fetch_weather_and_forcast(city1,API_KEY,current_weather_url,forcast_url)
        else:
            return render(request, "weather_app/index.html")

        if city2:
            weather_data2, daily_forcasts2 = fetch_weather_and_forcast(city2, API_KEY, current_weather_url,forcast_url)
        else:
            weather_data2, daily_forcasts2 = None, None
        
        context = {
            "weather_data1": weather_data1,
            "daily_forcasts1": daily_forcasts1,
            "weather_data2": weather_data2,
            "daily_forcasts2": daily_forcasts2
        }

        return render(request, "weather_app/index.html",context)
    else:
        return render(request, "weather_app/index.html")
    
def fetch_weather_and_forcast(city,api_key,current_weather_url, forcast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'],response['coord']['lon'] # don't need asyn prog??
    forcast_response = requests.get(forcast_url.format(lat,lon,api_key)).json()

    weather_data = {
        "city": city,
        "temperature": round(response['main']['temp'] - 273.15, 2),
        "description": response['weather'][0]['description'],
        "icon": response['weather'][0]['icon']
    }

    daily_forcasts = []
    # note - changes done as per new url response json
    for daily_data in forcast_response['list'][:5]:
        daily_forcasts.append({
            "day": datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A"),
            "min_temp": round(daily_data['main']['temp_min'] - 273.15, 2),
            "max_temp": round(daily_data['main']['temp_max'] - 273.15, 2),
            "description": daily_data['weather'][0]['description'],
            "icon": daily_data['weather'][0]['icon'],
            "date_time":daily_data['dt_txt']

        })
    print(daily_forcasts)


    return weather_data, daily_forcasts
