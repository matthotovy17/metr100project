# This file will serve as a function library to be used by core.py
# here is the curl command for the Accuweather api current conditions
# curl -X GET "http://dataservice.accuweather.com/currentconditions/v1/349291?apikey=d1w8pFazvk8uKC7AzmWAxWCNP1mtEZK3&details=true"
api = "d1w8pFazvk8uKC7AzmWAxWCNP1mtEZK3"
import requests
import json
import pandas as pd
from tabulate import tabulate
# display current conditions based on key
def get_conditions(key):
    conditions_url = "http://dataservice.accuweather.com/currentconditions/v1/349291?apikey=d1w8pFazvk8uKC7AzmWAxWCNP1mtEZK3&details=true"
    response = requests.get(conditions_url)
    json_version = response.json()
    #print("Current Conditions: {}".format(json_version[0].get('WeatherText')))
    return json_version[0]
    
def print_HistoryData():
    pd.set_option('display.max_rows', None)
    df = pd.read_csv (r'OmahaWeatherHistory copy.csv')
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

def createNewAlertCsv():
    pd.set_option('display.max_rows', None)
    df = pd.read_csv(r'cleanBZAlert.csv')
    test = df[df['ugc'].str.contains('NEZ')]
    test.to_csv(r'./cleanBZAlert2.csv', index=False)
    print(test['ugc'])
    #print(filteredDF)

def createNewWeatherDataCsv():
    pd.set_option('display.max_rows', None)
    
    df = pd.read_csv(r'OmahaWeatherHistory copy.csv')
    
    dates = pd.read_csv(r'uniqueStartAndEndTimes.csv')
    
    startDates = dates['utc_issue'].str[0:10]
    endDates = dates['utc_expire'].str[0:10]
    
    totalDates = startDates.append(endDates)
    uniqueDates = totalDates.unique()
    print(len(uniqueDates))
    
    filteredDF = df[df['dt_iso'].str[0:10].isin(uniqueDates)]
    filteredDF['visibility'] = filteredDF['visibility'] * 0.000621371
    filteredDF['wind_speed'] = filteredDF['wind_speed'] * 2.23694
    filteredDF.to_csv(r'newWeatherHistory.csv', index=False)
    print(tabulate(filteredDF, headers='keys', tablefmt='psql'))
    
def createMainDisplayCSV(): 
    print("main display csv")
    
    weatherHistory = pd.read_csv(r'newWeatherHistory.csv')
    dates = pd.read_csv(r'uniqueStartAndEndTimes.csv')
    alerts = pd.read_csv(r'cleanBZAlertNew.csv')
    codes = pd.read_csv(r'ugcCode.csv')
    
    mainDisplay = pd.DataFrame(columns=["Issue DT", "Expire DT", "Temperature Min", "Temperature Max", 
                                        "Temperature Avg", "Wind Spd Min", "Wind Spd Max","Wind Spd Avg", 
                                        "Visibility Min", "Visibility Max", "Visibility Avg", "Had Snowfall", "counties"])
    print(weatherHistory.columns)
    
    for index, row in dates.iterrows():
        startTime = row["utc_issue"]
        endTime = row["utc_expire"]
        
        startSearch = formatSearchTime(startTime, False)
        endSearch = formatSearchTime(endTime, True)
        
        subWeatherHistory = weatherHistory[(weatherHistory['dt_iso'] >= startSearch) & (weatherHistory['dt_iso'] <=endSearch)]
        
        minTemp = subWeatherHistory['temp'].min()
        maxTemp = subWeatherHistory['temp'].max()
        avgTemp = round(subWeatherHistory['temp'].mean(), 2)
        
        minWind = subWeatherHistory['wind_speed'].min()
        maxWind = subWeatherHistory['wind_speed'].max()
        avgWind = round(subWeatherHistory['wind_speed'].mean(), 2)
        
        minVis = subWeatherHistory['visibility'].min()
        maxvis = subWeatherHistory['visibility'].max()
        avgVis = round(subWeatherHistory['visibility'].mean(), 2)
        
        hadSnowFall = (True in set(subWeatherHistory['weather_main'].str.contains("Snow")) )| (True in set(subWeatherHistory['weather_description'].str.contains("Snow")))
        
        counties = getCounties(startTime, endTime, alerts, codes)
        mainDisplay.loc[len(mainDisplay.index)] = [startTime, endTime, minTemp, maxTemp, avgTemp, minWind, maxWind, avgWind, minVis, maxvis, avgVis, hadSnowFall, counties]
    
    # mainDisplay.loc[len(mainDisplay.index)] = ["Total", "Column", round(mainDisplay['Temperature Min'].mean(), 2), round(mainDisplay['Temperature Max'].mean(), 2), round(mainDisplay['Temperature Avg'].mean(), 2),  ]
    mainDisplay.to_csv(r'mainDisplay.csv', index=False)
        
    print(tabulate(mainDisplay, headers='keys', tablefmt='psql'))

def getCounties(startTime, endTime, alerts, codes):

    relevantAlerts = alerts[(alerts['utc_issue'] == startTime) & (alerts["utc_expire"] == endTime)]
    
    joined = pd.merge(relevantAlerts, codes, how="left", left_on="ugc", right_on="Z")
    
    return list(joined['Z'])
    
    
        
def getDisplayHourByHour(weatherHistory):
    return weatherHistory[["dt_iso", "temp", "visibility", "wind_speed", "weather_main", "weather_description"]]
    
    
        
        
        


def formatSearchTime (dt, isEndTime):
    if isEndTime:
        date = dt[0:10]
        hr = int(dt[11:13])
        minute = int(dt[14:16])
        
        if minute > 0:
            hr +=1
        
        hr = str(hr)
        
        if len(hr) == 1:
            hr = "0{}".format(hr)
        newDt = "{} {}:00:00 +0000 UTC".format(date, hr)
        return newDt
    else:
        date = dt[0:10]
        hr = dt[11:13]
        newDt = "{} {}:00:00 +0000 UTC".format(date, hr)
        return newDt
        
        
        
    