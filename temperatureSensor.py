import glob
import requests
import time
from loguru import logger

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

postRequests = True
postUrl = 'http://172.20.108.153:3000/temp/room311'

@logger.catch
def postRequest(temperature):
        logger.info("sending temperature..")
        # Generate the correct json Body
        jsonBody = {
                'celsius': temperature
                }
        # Execute the post request with the correct json data and save the response
        response = requests.post(postUrl, json=jsonBody, timeout=10)
        logger.debug(response.json())

@logger.catch
def readTemperature():
        file = open(device_file, 'r')
        content = file.read()
        file.close()

        pos = content.rfind('t=') + 2
        temp = content[pos:]
        temperature = float(temp) / 1000
        logger.info(temperature)
        return temperature

while True:
    temperature = readTemperature()

    if postRequests:
        postRequest(temperature)

    time.sleep(1)
