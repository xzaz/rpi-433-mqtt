#!/usr/bin/python

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import configparser
import time
import warnings

try:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
except RuntimeError:
    warnings.warn("This can only be run on a Raspberry PI", RuntimeWarning)

def read_timings(rx_pin):
    print("reading timings on rx pin: " + str(rx_pin))
    capture = []
    while True:
        start = time.time()
        if GPIO.wait_for_edge(rx_pin, GPIO.BOTH, timeout=1000):
            print(GPIO.input(rx_pin))
            #capture.append((time.time() - start, GPIO.input(rx_pin)))

        elif len(capture) < 5:  # Any pattern is likely larger than 5 bits
            print('len from capture lower then 5')
            capture = []
        else:
            return capture


def record(rxpin):
    print("recording")
    GPIO.setup(rxpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    sample = read_timings(rxpin)
    print('Recorded', len(sample), 'bit transitions')
    return sample

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

    while True:
        print(record(int(cGPIO['pin'])))
        
    input("Press any key to exit..\n")


if __name__ == "__main__":
    main()