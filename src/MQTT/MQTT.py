#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.parameters import Color
from pybricks.tools import print, wait

from umqtt.robust import MQTTClient

class MQTT:

    def __init__(self, robot_id='robot1'):
        self.robot_id = robot_id
        self.client = MQTTClient(robot_id, '10.12.203.73')
        
        # État actuel de l'ordre reçu
        self.ordre_actuel = "GO"
        
        # Connexion au broker
        self.client.set_callback(self.getmessages)
        self.client.connect()
        
        # S'abonne au topic pour recevoir les ORDRES du contrôleur
        topic_ordre = b"controleur/" + robot_id.encode() + b"/ordre"
        self.client.subscribe(topic_ordre)
        print("Abonné à:", topic_ordre)

    def getmessages(self, topic, msg):
        """Callback appelé quand un message est reçu"""
        message = msg.decode('utf-8')
        print("Ordre reçu:", message)
        
        # Affiche sur l'écran du robot
        brick.display.clear()
        brick.display.text("Ordre: " + message, (0, 50))
        
        # Mettre à jour l'ordre
        if message == "GO":
            self.ordre_actuel = "GO"
            brick.light(Color.GREEN)
        elif message == "STOP":
            self.ordre_actuel = "STOP"
            brick.light(Color.RED)

    def get_ordre(self):
        """Retourne l'ordre actuel après vérification des messages"""
        self.client.check_msg()
        return self.ordre_actuel

    def send_msg(self, message):
        """Envoie un message de position/état"""
        topic = b"robots/" + self.robot_id.encode() + b"/position"
        self.client.publish(topic, message.encode("utf-8"))
        print("Envoyé:", message)
        self.client.check_msg()
    
    def signaler_entree(self, voie):
        """Signale l'entrée dans la zone de stockage"""
        if voie == "GAUCHE":
            self.send_msg("ENTREE BOUCLE : GAUCHE")
        else:
            self.send_msg("ENTREE BOUCLE : DROITE")
    
    def signaler_sortie(self):
        """Signale la sortie de la zone de conflit"""
        self.send_msg("SORTIE")
