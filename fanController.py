from gpiozero import LED
from loguru import logger
import requests
import time

getURL = "http://172.20.108.153:3000/temp/room311/latest"

fan = LED(26)

@logger.catch
def getTemperature():
    logger.info("getting Temperature..")
    response = requests.get(getURL, timeout=10) # Execute the request and save it in response
    logger.debug(response.json())
    temperature = response.json()['celsius'] # Extract the celsius temperature from the response Json Data
    logger.info("received Temperature: " + str(temperature))
    return temperature

def activateFan(status):
    logger.info("changing fan status to " + str(status))
    if status == True:
        fan.on()
    else:
        fan.off()

while True:
    currentTemperature = getTemperature()

    # currentTemperature will be the wrong Type if getTemperature fails
    # Check if it is a NoneType and change it to int
    if currentTemperature is None:
        logger.error("temperature Type is wrong, changing it to 0")
        currentTemperature = 0

    if currentTemperature > 24:
        activateFan(True)
    else:
        activateFan(False)
    time.sleep(2)
