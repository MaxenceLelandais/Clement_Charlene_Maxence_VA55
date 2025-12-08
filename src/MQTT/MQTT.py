#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

from umqtt.robust import MQTTClient

class MQTT:

    def __init__(self):

        self.client = MQTTClient('robot1','10.12.203.73')
        # Connexion au broker
        self.client.set_callback(self.getmessages)
        self.client.connect()
        # S'abonne au topic pour recevoir les messages
        self.client.subscribe(b"robots/robot1/position")

    def getmessages(self, topic, msg):
        # Affiche le message reçu sur l'écran du robot
        brick.display.text(str(msg))

    def send_msg(self, message):
    
        self.client.publish(b"robots/robot1/position", message.encode("utf-8"))
        print("Message envoyé :", message)
        # Vérifie s'il y a des messages reçus
        self.client.check_msg()
