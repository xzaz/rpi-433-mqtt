#!/usr/bin/python

import sys
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import configparser
from rpi_rf import RFDevice

def on_connect(client, userdata, flags, rc):
    print("Connected with code: " + str(rc))

def main(argv):
    config = configparser.ConfigParser()
    config.read('config.ini')
    cMqtt = config['MQTT']
    client = mqtt.Client()
    client.on_connect = on_connect
    ##client.on_message = on_message
    client.username_pw_set(cMqtt['username'], cMqtt['password'])
    client.connect(cMqtt['host'])
    client.loop_start()
    input("Press any key to exit..\n")


if __name__ == "__main__":
    main(sys.argv)