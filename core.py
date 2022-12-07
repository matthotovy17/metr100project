# This is the core file which will run our project
# here is the curl command for the Accuweather api current conditions
# curl -X GET "http://dataservice.accuweather.com/currentconditions/v1/349291?apikey=d1w8pFazvk8uKC7AzmWAxWCNP1mtEZK3&details=true"
import requests
import json
import functions

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


def isBlizardConditions(windSpeed, visibility, isSnowing, isSnowOnGround):
    return windSpeed >= 35 and visibility <= (1/4) and (isSnowing or isSnowOnGround)

def validateNumber(val):
    return 
def randomConditions():
    
    tempUpperBound = 32
    windSpeedMin = 35
    visibilityInMiles = 1/4
    isSnowing = False
    snowCurrentlyOnGround = False
    conditionsTimeSpanHours = 3
    
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
        print("Those conditions meet the criteria of a blizzard warning.")
    else :
        print("Those conditions do not meet the criteria of a blizzard warning for the following reasons:\n")
        noBlizzardReasons(windSpeed, visibility, isSnowing, isSnowOnGround, timeSpan)
        
def todaysWeatherConditions():
    conditions = functions.get_conditions(349291)
    
    temperatue = conditions["Temperature"]["Imperial"]["Value"]
    windSpeed = conditions["Wind"]["Speed"]["Imperial"]["Value"]
    isSnowing = conditions["HasPrecipitation"] and conditions["PrecipitationType"] == "Snow"
    isSnowingNY = "Yes" if isSnowing else "No"
    visibility = conditions["Visibility"]["Imperial"]["Value"]
    print("Wind Speed: ", windSpeed)
    print("Is it snowing?: ", isSnowingNY)
    print("Visibility (Miles): ", visibility)
    
    if isBlizardConditions(windSpeed, visibility, isSnowing, False):
        print("These conditions meet the criteria for a Blizzard Warning. If conditions have persisted for the last three hours than a Blizzard Warning should be issued.")
    else:
        print("These conditions do not meet the criteria for a Blizzard Warning for the following reasons: \n")
        noBlizzardReasons(windSpeed, visibility, isSnowing, False)
        

    
    
     
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
        functions.print_HistoryData()
        
    

    


__main__()