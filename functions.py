# This file will serve as a function library to be used by core.py
# here is the curl command for the Accuweather api current conditions
# curl -X GET "http://dataservice.accuweather.com/currentconditions/v1/349291?apikey=d1w8pFazvk8uKC7AzmWAxWCNP1mtEZK3&details=true"
import requests
import json
import pandas as pd

# display current conditions based on key
def get_conditions(key):
    conditions_url = 'https://dataservice.accuweather.com/currentconditions/v1/'f'?apikey={api}'.format(key)
    response = requests.get(conditions_url)
    json_version = response.json()
    print("Current Conditions: {}".format(json_version[0].get('WeatherText')))
    return json_version
    
def print_HistoryData():
    pd.set_option('display.max_rows', None)
    df = pd.read_csv (r'OmahaWeatherHistory copy 2.csv')
    print("Eppley Airfield Historic Weather Data\n")
    print("Cordinates:(41.301475,-95.894521) \n")
    df.pop('dt') 
    df.pop('lat')
    df.pop('lon')
    df.pop('city_name')
    df.pop('sea_level')
    df.pop('grnd_level')
    df.pop('timezone')
    df.pop('weather_icon')
    df.pop('weather_description')
    df.pop('wind_gust')
    df.pop('weather_id')
    df.pop('clouds_all')
    print(df)
