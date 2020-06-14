#!/usr/bin/python

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import configparser
import time
import logging
import sys
import signal
import json
from rpi_rf import RFDevice

rfdevice = None

# pylint: disable=unused-argument
def exithandler(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)


logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

def on_connect(client, userdata, flags, rc):
    print("Connected with code: " + str(rc))

def main():
    #Config
    config = configparser.ConfigParser()
    config.read('config.ini')
    cMqtt = config['MQTT']
    cGPIO = config['GPIO']
    cDevices = config['DEVICES']
    
    #MQTT
    client = mqtt.Client()
    client.on_connect = on_connect
    ##client.on_message = on_message
    client.username_pw_set(cMqtt['username'], cMqtt['password'])
    client.connect(cMqtt['host'])
    client.loop_start()

    # RF
    signal.signal(signal.SIGINT, exithandler)
    rfdevice = RFDevice(int(cGPIO['pin']))
    rfdevice.enable_rx()
    timestamp = None
    logging.info("Listening for codes on GPIO " + str(cGPIO['pin']))

    devices = cDevices['devices'].split(';')

    for device in devices:
        client.publish("homeassistant/switch/rpi-433-mqtt/" + str(device) + "/config", json.dumps({"name" : str(device), "command_topic" : "homeassistant/switch/rpi-433-mqtt/" + str(device) + "/set", "state_topic" : "homeassistant/switch/rpi-433-mqtt/" + str(device) + "/state" }))

    while True:
        if rfdevice.rx_code_timestamp != timestamp:
            timestamp = rfdevice.rx_code_timestamp
            if str(rfdevice.rx_code) in devices:
                client.publish("homeassistant/switch/rpi-433-mqtt/" + str(rfdevice.rx_code) + "/set", "ON")

            logging.info(str(rfdevice.rx_code) +
                     " [pulselength " + str(rfdevice.rx_pulselength) +
                     ", protocol " + str(rfdevice.rx_proto) + "]")
        time.sleep(0.01)

    rfdevice.cleanup()    

if __name__ == "__main__":
    main()