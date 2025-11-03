#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

from umqtt.robust import MQTTClient
import time

def getmessages(topic, msg):
    if topic == b'JorgePe/test':
        brick.display.text(msg)

client = MQTTClient('52dc166c-2de7-43c1-88ff-f80211c7a8f6','test.mosquitto.org')
client.connect()

client.publish('JorgePe/test','Listening')
client.set_callback(getmessages)
client.subscribe('JorgePe/test')
brick.display.text('Listening...')

while True:
    client.check_msg()
    time.sleep(0.1)