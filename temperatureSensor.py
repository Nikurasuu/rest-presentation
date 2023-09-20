import glob
import requests
import time
from loguru import logger

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

postRequests = True
postUrl = 'http://172.20.170.52:3000/temp'

@logger.catch
def postRequest(temperature):
        logger.info("sending temperature..")
        response = requests.post(postUrl, json={'celsius': temperature}, timeout=10)
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
