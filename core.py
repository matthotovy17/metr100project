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
    
    temp = input("Temperature (Degrees Farenheit): ")
    temp = float(temp)
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
    
    if temp <= 32 and windSpeed >= 35 and visibility <= (1/4) and (isSnowing or isSnowOnGround) and timeSpan >= 3:
        print("Those conditions meet the criteria of a blizzard warning.")
    else :
        print("Those conditions do not meet the criteria of a blizzard warning.")
    
     
    
    
    

def __main__():
    print("hello")
    
    val = prompt1()
    
    while not validatePrompt1(val):
        val = notValidPrompt()
        
    if val == "1":
        print("1")
        randomConditions()
    elif val =="2":
        print("2")
    elif val =="2":
        print("3")
        
    

    


__main__()