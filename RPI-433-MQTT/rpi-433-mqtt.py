#!/usr/bin/python

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import configparser
from rpi_rf import RFDevice

def on_connect(client, userdata, flags, rc):
    print("Connected with code: " + str(rc))

def main():
    #Config
    config = configparser.ConfigParser()
    config.read('config.ini')
    cMqtt = config['MQTT']
    cGPIO = config['GPIO']
    
    #MQTT
    client = mqtt.Client()
    client.on_connect = on_connect
    ##client.on_message = on_message
    client.username_pw_set(cMqtt['username'], cMqtt['password'])
    client.connect(cMqtt['host'])
    client.loop_start()

    #RF
    rf = RFDevice(int(cGPIO['pin']))
    rf.enable_rx()
    rf.rx_callback

    timestamp = None
    while True:
        if rf.rx_code_timestamp != timestamp:
            timestamp = rf.rx_code_timestamp
            print(str(rf.rx_code))
        

    input("Press any key to exit..\n")


if __name__ == "__main__":
    main()