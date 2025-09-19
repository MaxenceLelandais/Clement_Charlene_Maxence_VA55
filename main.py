#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.tools import wait

from src.controlleurs.MoteursControlleur import MoteursControlleur



# Create your objects here.
ev3 = EV3Brick()

moteur = MoteursControlleur()

while True:
    moteur.envoieCommandeMoteurs()

    wait(10)

