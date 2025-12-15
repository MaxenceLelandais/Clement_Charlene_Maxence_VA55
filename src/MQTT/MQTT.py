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
        
        # Pour le mode peloton
        self.distance_securite = 200  # Distance de sécurité à maintenir en mm
        self.distance_robot_devant = None  # Distance du robot qui précède
        
        # Connexion au broker
        self.client.set_callback(self.getmessages)
        self.client.connect()
        
        # S'abonne au topic pour recevoir les ORDRES du contrôleur
        topic_ordre = b"controleur/" + robot_id.encode() + b"/ordre"
        self.client.subscribe(topic_ordre)
        print("Abonné à:", topic_ordre)
        
        # S'abonne aux distances de tous les robots (pour le peloton)
        self.client.subscribe(b"robots/+/distance")
        print("Abonné aux distances des robots")

    def getmessages(self, topic, msg):
        """Callback appelé quand un message est reçu"""
        topic_str = topic.decode('utf-8')
        message = msg.decode('utf-8')
        
        # Si c'est une distance d'un autre robot (pour le peloton)
        if '/distance' in topic_str:
            # On ignore, c'est Node-RED qui gère la liste
            return
        
        print("Ordre reçu:", message)
        
        # Affiche sur l'écran du robot
        brick.display.clear()
        brick.display.text("Ordre: " + message, (0, 50))
        
        # Parser les ordres
        if message == "GO":
            self.ordre_actuel = "GO"
            self.distance_robot_devant = None
            brick.light(Color.GREEN)
        elif message == "STOP":
            self.ordre_actuel = "STOP"
            self.distance_robot_devant = None
            brick.light(Color.RED)
        elif message.startswith("FOLLOW"):
            # Format: "FOLLOW:200" (distance du robot devant en mm)
            self.ordre_actuel = "FOLLOW"
            parts = message.split(':')
            if len(parts) >= 2:
                self.distance_robot_devant = float(parts[1])
            brick.light(Color.ORANGE)

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
    
    def signaler_entree(self, voie, distance_zone_conflit):
        """Signale l'entrée dans la zone de stockage avec la distance à la zone de conflit"""
        if voie == "GAUCHE":
            self.send_msg("ENTREE:GAUCHE:" + str(int(distance_zone_conflit)))
        else:
            self.send_msg("ENTREE:DROITE:" + str(int(distance_zone_conflit)))
    
    def envoyer_distance(self, distance_zone_conflit):
        """Envoie la distance par rapport à la zone de conflit (pour peloton et coopératif)"""
        topic = b"robots/" + self.robot_id.encode() + b"/distance"
        message = str(int(distance_zone_conflit))
        self.client.publish(topic, message.encode("utf-8"))
        self.client.check_msg()
    
    def get_distance_robot_devant(self):
        """Retourne la distance du robot qui précède (pour le peloton)"""
        return self.distance_robot_devant
    
    def get_distance_securite(self):
        """Retourne la distance de sécurité à maintenir"""
        return self.distance_securite
    
    def signaler_sortie(self):
        """Signale la sortie de la zone de conflit"""
        self.send_msg("SORTIE")
