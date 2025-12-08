#!/usr/bin/env pybricks-micropython

from src.services.MoteurService import MoteurService
from src.services.CapteursService import CapteursService
from src.services.SystemeService import SystemeService

from src.calculs.BangBang import BangBang
from src.calculs.KalmanAngle import KalmanAngle
from src.calculs.PID import PID
from src.calculs.PI import PI
from src.calculs.P import P
from src.calculs.KalmanFilter import KalmanFilter

from pybricks.tools import wait
from pybricks import ev3brick as brick

from src.utils.Log import Log
import time
import math
from src.MQTT.MQTT import MQTT

from pybricks.tools import StopWatch

class MoteursControlleur:

    def __init__(self):
        self.moteursService = MoteurService()
        self.capteursService = CapteursService()
        self.systemeService = SystemeService()

        # Passer l'ID du robot ici (changer pour robot2, robot3, etc.)
        self.mqtt = MQTT('robot1')
        
        self.logger = Log()
        self.stopwatch = StopWatch()
        
        self.ralentissement_en_pourcentage = 0.8
        self.facteur = 1

        self.obstacle = False
      
        self.vitesse_base = self.systemeService.getVitesse()
        
        self.pourPID()

        # Initialisation de la position
        self.post_x, self.post_y = 0.0, 0.0
        self.temps_precedent = time.time()
        self.distance_left = 0.0
        self.distance_right = 0.0
        self.couleur_avant = ""
        
        # Gestion des zones pour MQTT
        self.dans_zone_stockage = True  # TEMPORAIRE: forcer à True pour tester
        self.dans_zone_conflit = False
        self.couleur_sortie = "Vert"  # Couleur qui indique la sortie
        
        # Signaler l'entrée dès le départ (pour tester)
        self.mqtt.signaler_entree("GAUCHE")

        # Initialisation du filtre de Kalman
        # Paramètres à ajuster selon les performances :
        # - process_variance : incertitude du modèle (faible = modèle fiable)
        # - measurement_variance_gyro : bruit du gyroscope (ajuster selon la qualité du capteur)
        # - measurement_variance_odom : bruit de l'odométrie (plus élevé car dérive des roues)
        self.kalman_filter = KalmanFilter(
            process_variance=0.01,        # Modèle relativement fiable
            measurement_variance_gyro=0.5, # Gyroscope assez précis
            measurement_variance_odom=2.0  # Odométrie moins précise (glissement des roues)
        )
        
        # Paramètres de calibration (à ajuster selon votre robot)
        self.wheel_diameter = 56.0  # Diamètre des roues en mm
        self.wheel_base = 118.0      # Distance entre les roues en mm
        self.kalman_filter.set_wheel_base(self.wheel_base)

        self.nbr_passage = 0
        self.niveau_passage = ["DROITE","GAUCHE"]

    def pourBangBang(self):
        
        
        self.bangBang = BangBang()
        
        
    def pourP(self):
        
        kp = self.systemeService.getKp()
        
        self.p = P(kp)
        
    def pourPI(self):
        
        kp = self.systemeService.getKp()
        ki = self.systemeService.getKi()
        
        self.pi = PI(kp, ki)
        
    def pourPID(self):
        
        
        kp = self.systemeService.getKp()
        ki = self.systemeService.getKi()
        kd = self.systemeService.getKd()
        """
        ku = self.systemeService.getKu()
        tu = self.systemeService.getTu()

        kp = 0.6 * ku
        ki = 1.2 * ku / tu
        """
        tu = self.systemeService.getTu()
        kd = (3 * kp * tu) / 40
        
        self.pid = PID(kp, ki, kd)

    def detection_entree_sortie_intersection(self, couleur):

        if self.couleur_avant!=couleur:

            if couleur == "Rouge":

                endroit = self.niveau_passage[self.nbr_passage%2]
                brick.sound.beep()
                self.mqtt.send_msg(endroit)
                self.nbr_passage+=1
                wait(200)

            self.couleur_avant = couleur

    def detection_obstacle(self):

        if self.capteursService.get_detection():

            if not self.obstacle:
                self.mqtt.send_msg("OBSTACLE DETECTE")

            self.obstacle = True

            self.facteur *= self.ralentissement_en_pourcentage
            
            if self.facteur < 0.1:
                self.facteur = 0
                self.pid.restart()
            self.moteursService.avancer(0, 0)
            return  # Sortir immédiatement
            
        else:
            self.facteur = 1
            self.obstacle = False

        
    def envoieCommandeMoteurs(self):

        self.temps_precedent = time.time()
        
        # 1. Vérifier les ordres du contrôleur Node-RED
        ordre = self.mqtt.get_ordre()
        print("Ordre actuel:", ordre, "Zone stockage:", self.dans_zone_stockage, "Zone conflit:", self.dans_zone_conflit)
        
        # 2. Gestion obstacle (priorité absolue)
        
        self.detection_obstacle()

        # 3. Lecture capteurs
        reflexion = self.capteursService.get_reflexion()

        couleur = self.capteursService.get_couleur()


        self.detection_entree_sortie_intersection(couleur)

        print(couleur, reflexion, "| Ordre:", ordre)

        # 5. Appliquer l'ordre du contrôleur - SIMPLE: STOP = arrêt, GO = avance
        if ordre == "STOP":
            print(">>> ARRET COMMANDE PAR NODE-RED <<<")
            self.moteursService.avancer(0, 0)
            self.pid.restart()
            return

        # 6. Calcul PID et commande moteurs (seulement si GO)
        correction = self.pid.compute(50, reflexion)
        

        v_droit = max(0, self.vitesse_base - correction) * self.facteur
        v_gauche = max(0, self.vitesse_base + correction) * self.facteur

        # 7. Calculer la position avant d'envoyer la commande
        self.calculer_position()

        # 8. Logging
        temps_actuel = self.stopwatch.time()
        delta_temps = temps_actuel - self.temps_precedent
        self.temps_precedent = temps_actuel

        #print(delta_temps, v_droit, v_gauche )

        angle_gyro = self.capteursService.get_angle()

        self.logger.log(delta_temps, v_droit, v_gauche, angle_gyro)
        
        # 9. Envoyer commandes moteurs
        self.moteursService.avancer(v_droit, v_gauche)


    def calculer_position(self):
        """
        Calcule la position (x, y) du robot en utilisant l'odométrie
        avec l'angle corrigé par le filtre de Kalman
        """
        # Calculer le temps écoulé depuis la dernière mise à jour
        #temps_actuel = time.time()f
        #temps_actuel = self.stopwatch.time()
        #delta_temps = temps_actuel - self.temps_precedent
        #self.temps_precedent = temps_actuel
        
        # Récupérer l'angle du gyroscope (en degrés)
        angle_gyro = self.capteursService.get_angle()
        
        # Calculer la distance parcourue par chaque roue
        distance_left, distance_right = self.moteursService.get_distance_roue()
        
        # Appliquer le filtre de Kalman pour fusionner gyroscope et odométrie
        theta_deg = self.kalman_filter.update_fusion(angle_gyro, distance_left, distance_right)
        
        # Convertir l'angle corrigé en radians pour les calculs trigonométriques
        theta_rad = math.radians(theta_deg)

        
        
        # Calculer le déplacement depuis la dernière itération
        if self.distance_left != 0.0 or self.distance_right != 0.0:
            # Changement de distance pour chaque roue
            delta_left = distance_left - self.distance_left
            delta_right = distance_right - self.distance_right
            
            # Distance moyenne parcourue par le robot
            distance_moyenne = (delta_left + delta_right) / 2.0
            
            # Calculer le déplacement en x et y avec l'angle corrigé
            deplacement_x = distance_moyenne * math.cos(theta_rad)
            deplacement_y = distance_moyenne * math.sin(theta_rad)
            
            # Mettre à jour la position
            self.post_x += deplacement_x
            self.post_y += deplacement_y
        
        # Sauvegarder les distances actuelles pour la prochaine itération
        self.distance_left = distance_left
        self.distance_right = distance_right


        self.temps_precedent = time.time()
