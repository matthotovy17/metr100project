# This is the core file which will run our project
# here is the curl command for the Accuweather api current conditions
# curl -X GET "http://dataservice.accuweather.com/currentconditions/v1/349291?apikey=d1w8pFazvk8uKC7AzmWAxWCNP1mtEZK3&details=true"
import requests
import json
import functions
import pandas as pd
from tabulate import tabulate

# get the current conditions for Omaha: 349291 is the location key for Omaha
#response = functions.get_conditions(349291)

def prompt1():
    print("Welcome to the blizzard information center! \nWhat would you like to do?\n")
    
    print("1) Check if weather conditions meet the criteria for a blizzard.")
    print("2) Check if today's weather constitutes a blizzard.")
    print("3) Check what the weather was like during historical blizzard warnings.\n")
    
    val = input("Please type the corresponding number of what you would like to do: ")
    
    return val

def notValidPrompt():
    val = input("Not a valid input, pleasae select either 1, 2, or 3: ")
    return val
    
    
def validatePrompt1(val):
    return val == "1" or val == "2" or val == "3" 

def blizardConditionsBlurb():
    print("""\n\nThere are 3 major criteria for a blizard warning:
          - Large amounts of snow or blowing snow.
          - Winds greater than 35 mph.
          - Visibility below a quarter of a mile for at least 3 hours.""")
def isBlizardConditions(windSpeed, visibility, isSnowing, isSnowOnGround):
    return windSpeed >= 35 and visibility <= (1/4) and (isSnowing or isSnowOnGround)

def validateNumber(val):
    return 
def randomConditions():

    isSnowing = False

    
    print("You will be prompted to enter in several weather condtions and at the end will be told if they meet the criteria for a blizzard.")
    
    windSpeed = input("Wind Speed (MPH): ")
    windSpeed = float(windSpeed)
    visibility = input("Visibility (Miles): ")
    visibility = float(visibility)
    isSnowing = input("Is it snowing? (Y/N): ")
    isSnowing = isSnowing == "Y"
    isSnowOnGround = input("Is there snow currently on the ground? (Y/N): ")
    isSnowOnGround = isSnowOnGround == "Y"
    timeSpan = input("How long have these conditions been present? (Hours): ")
    timeSpan = float(timeSpan)
    
    if isBlizardConditions(windSpeed, visibility, isSnowing, isSnowOnGround) and timeSpan >= 3:
        print("Those conditions meet the criteria of a blizzard warning.\n")
    else :
        print("Those conditions do not meet the criteria of a blizzard warning for the following reasons:\n")
        noBlizzardReasons(windSpeed, visibility, isSnowing, isSnowOnGround, timeSpan)
        
    blizardConditionsBlurb()
    
    print("""\n\n Do you want to try again? (Y) 
          Go back to the main menu? (menu) 
          or Quit the application? (quit)""")
    
    val = input()
    
    if val == "Y":
        randomConditions()
    elif val == "menu":
        __main__()
    elif val == "quit":
        exit()
        
def todaysWeatherConditions():
    conditions = functions.get_conditions(349291)
    
    temperatue = conditions["Temperature"]["Imperial"]["Value"]
    windSpeed = conditions["Wind"]["Speed"]["Imperial"]["Value"]
    isSnowing = conditions["HasPrecipitation"] and conditions["PrecipitationType"] == "Snow"
    isSnowingNY = "Yes" if isSnowing else "No"
    visibility = conditions["Visibility"]["Imperial"]["Value"]
    print("\n\nRelevant Weather Conditions")
    print("Wind Speed: ", windSpeed)
    print("Is it snowing?: ", isSnowingNY)
    print("Visibility (Miles): ", visibility)
    
    if isBlizardConditions(windSpeed, visibility, isSnowing, False):
        print("These conditions meet the criteria for a Blizzard Warning. If conditions have persisted for the last three hours than a Blizzard Warning should be issued.")

    else:
        print("These conditions do not meet the criteria for a Blizzard Warning for the following reasons: \n")
        noBlizzardReasons(windSpeed, visibility, isSnowing, False)
    
    blizardConditionsBlurb()
    
    print("""Would you like to 'quit' the appilcation or go to the main 'menu'? """)
    val = input()
    
    if val == 'quit':
        exit()
    elif val == "menu":
        __main__()
        

    
    
     
## TODO: create function that lists the reasons why the blizzard wanring does not work

def noBlizzardReasons(windSpeed, visibility, isSnowing, isSnowOnGround, timeSpan=None):
    if windSpeed < 35:
        print("The wind speed is not fast enough.")
    if visibility > (1/4):
        print("The visibility is too far.")
    if not(isSnowing or isSnowOnGround):
        print("There is not avialable snow for the wind to blow.")
    if (timeSpan is not None) and (timeSpan < 3):
        print("The present conditions have not persisted long enough.")
    

def historicalWeatherData(fromCounty=False):
    mainDisplay = pd.read_csv(r'mainDisplay.csv')
    historicalData = pd.read_csv(r'newWeatherHistory.csv')
    alerts = pd.read_csv(r'cleanBZAlertNew.csv')
    codes = pd.read_csv(r'ugcCode.csv')
    times = pd.read_csv(r'uniqueStartAndEndTimes.csv')
    
    if fromCounty:
        countyRoute(codes, historicalData, mainDisplay)
    
    print("""Welcome time traveler! Below is a list of all the blizzard warnings issued by OAX in the last 20 years.
          Additionally, we have done some aggregates of the weather while the warning was in affect. 
          If you would like to see the hour by hour weather during one of the alerts just type in the number.
          If you would like to only see the warnings for a specific county type in 'c'.
          If you would like to return to the main menu, type in 'menu'.
          If you would like to quit the application, type in 'quit'.""")
    
    mdt = mainDisplay
    
    ["Total", "Column", round(mdt['Temperature Min'].mean(), 2), round(mdt['Temperature Max'].mean(), 2), round(mdt['Temperature Avg'].mean(), 2),  
                               round(mdt['Wind Spd Min'].mean(), 2), round(mdt['Wind Spd Max'].mean(), 2), round(mdt['Wind Spd Avg'].mean(), 2),
                               round(mdt['Visibility Min'].mean(), 2), round(mdt['Visibility Max'].mean(), 2), round(mdt['Visibility Avg'].mean(), 2),
                               sum(mdt['Had Snowfall']), []]
    
    print("""Averages of values from the table:
          Average Temperature Min: {}
          Average Temperature Max: {}
          Average Temperature Avg: {}
          Average Wind Spd Min: {}
          Average Wind Spd Max: {}
          Average Wind Spd Avg: {}
          Average Visibility Min: {}
          Average Visibility Max: {}
          Average Visibility Avg: {}
          Number of Alerts with Snowfall: {}""".format(round(mdt['Temperature Min'].mean(), 2), round(mdt['Temperature Max'].mean(), 2), round(mdt['Temperature Avg'].mean(), 2),  
                               round(mdt['Wind Spd Min'].mean(), 2), round(mdt['Wind Spd Max'].mean(), 2), round(mdt['Wind Spd Avg'].mean(), 2),
                               round(mdt['Visibility Min'].mean(), 2), round(mdt['Visibility Max'].mean(), 2), round(mdt['Visibility Avg'].mean(), 2),
                               sum(mdt['Had Snowfall'])))
    
    print("These averages look pretty convincing that Eppley Airfield reports blizzard warning conditions or at least close to blizzar warning conditions, when a blizzard wanring is issued.")
    print("However if you take a look at the table below there are some outliers. Take a look at number 49 for instance. Having a minimum visibility of 6.2 miles? That seems a bit odd.")
    print("Investigate more by exploring the differences between counties. We suggest looking at Douglas county (which is where Eppley Airfield is located) and Knox county (which is on the Northern boarder of Nebraska).")
    print(tabulate(mainDisplay.loc[:, mainDisplay.columns != "counties"], headers='keys', tablefmt='psql'))
    
    val = input()
    
    if val == "c":
        countyRoute(codes, historicalData, mainDisplay)
    elif val == "menu":
        __main__()
    elif val == "quit":
        exit()
    elif val.isdigit():
        num = int(val)
        hourByHour(mainDisplay.iloc[num], historicalData)
        
def hourByHour(mdRow, weatherHistory, fromCounty=False): 
    
    
    startDate = mdRow["Issue DT"]
    endDate = mdRow["Expire DT"]
    print("Now showing hour by hour from {} to {}".format(startDate, endDate))
    searchStart = functions.formatSearchTime(startDate, False)
    searchEnd = functions.formatSearchTime(endDate, True)
    
    subWeatherHistory = weatherHistory[(weatherHistory['dt_iso'] >= searchStart) & (weatherHistory['dt_iso'] <= searchEnd)]
    displayHBH = functions.getDisplayHourByHour(subWeatherHistory)
    
    print(tabulate(displayHBH, headers='keys', tablefmt='psql'))
    
    print("""If you would like to go back to the main menu type in 'menu'.
          If you would like to go back to the aggregate table type in 'back'.
          If you would like to quit the application type 'quit'\n\n""")
    if fromCounty:
        print("You can also go back and slect another county by typing in 'c'.")
    val = input()
    
    if val == 'menu':
        __main__()
    elif val == "back":
        historicalWeatherData()
    elif val == "quit":
        exit()
    elif val == "c":
        historicalWeatherData(True)
    

def countyRoute(codes, historicalData, mainDisplay):
    print("""Below are a list of counties that blizzard warnings were sent out to.
          You can select a county by typing in the corresponding number.
          This will filter down the alerts to the specific counties.
          Or you can 'quit', go 'back' to the aggregate board, or go back to the 'menu'.""")

    
    print(tabulate(codes[['County']], headers='keys', tablefmt='psql'))
    val = input()
    
    if val == 'quit':
        exit()
    elif val == "back":
        historicalWeatherData()
    elif val == "menu":
        __main__()
    elif val.isdigit():
        val = int(val)
        countyRow = codes.iloc[val]
        filterByCounty(countyRow, historicalData, mainDisplay)
    
    
    
def filterByCounty(countyRow, historicalData, mainDisplay):
    print("You have chose alerts for {} County".format(countyRow['County']))
    
    if countyRow['County'] == "Knox":
        print("""Even though Knox county is located in Northern Nebraska, OAX is still responsible for sending out blizzard warnings for it.
              This can result in major differences between what we expect weather to be in a blizzard warning and what Eppley Airfield reports.
              However, this is not always the case, and some times, Eppley Airfield experiences very similar weather.
              Take a look at a few of the hour by hour weather reports for different blizzard alert sections and see how volatile they can be.""")
    
    if countyRow['County'] == "Douglas":
        print("""Since Douglas county is where Eppley Airfield is located and (OAX is located there as well) we see weather conditions that align well with our criteria for a blizzard warning.""")
    
    print("""From here you can select another county by typing in 'c'.
          'quit' the application. Go to the main 'menu'.
          Or select a blizzard warning and see the hour by hour by typing in the number associated with it""")
    
    mdCounty = mainDisplay[[countyRow['Z'] in i for i in mainDisplay['counties']]]
    
    print(tabulate(mdCounty.loc[:, mdCounty.columns != "counties"], headers='keys', tablefmt='psql'))
    
    val = input();
    
    if val == "c":
        historicalWeatherData(True)
    elif val == "quit":
        exit()
    elif val == "menu":
        __main__()
    elif val.isdigit():
        val = int(val)
        mdRow = mainDisplay.iloc[val]
        hourByHour(mdRow, historicalData, True)
    
    

def __main__():
    print("Hello")
    
    val = prompt1()
    
    while not validatePrompt1(val):
        val = notValidPrompt()
        
    if val == "1":
        randomConditions()
    elif val =="2":
        todaysWeatherConditions()
    elif val =="3":
        historicalWeatherData()

__main__()

print("Thanks for joining us! Have a great day!")