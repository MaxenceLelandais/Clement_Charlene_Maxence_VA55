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
        
        self.ralentissement_en_pourcentage = 0.8
        self.facteur = 1

        self.obstacle = False
      
        self.vitesse_base = self.systemeService.getVitesse()
        
        self.pourPID()
        
        self.start = time.time()
        self.stopwatch = StopWatch()

        # Initialisation de la position
        self.post_x, self.post_y = 0.0, 0.0
        self.temps_precedent = self.stopwatch.time()
        self.distance_left = 0.0
        self.distance_right = 0.0
        self.couleur_avant = ""
        
        # Gestion des zones pour MQTT
        self.dans_zone_stockage = False
        self.dans_zone_conflit = False
        self.couleur_sortie = "Vert"  # Couleur qui indique la sortie
        
        # Distance depuis l'entrée en zone de stockage (pour le peloton/coopératif)
        self.distance_entree_stockage = 0.0  # Distance totale parcourue à l'entrée
        self.distance_depuis_entree = 0.0    # Distance depuis l'entrée

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

    def envoieCommandeMoteurs(self):

        self.temps_precedent = time.time()
        
        # 1. Vérifier les ordres du contrôleur Node-RED
        ordre = self.mqtt.get_ordre()
        print("Ordre actuel:", ordre, "Zone stockage:", self.dans_zone_stockage, "Zone conflit:", self.dans_zone_conflit)
        
        # 2. Gestion obstacle (priorité absolue)
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

        # 3. Lecture capteurs
        reflexion = self.capteursService.get_reflexion()
        couleur = self.capteursService.get_couleur()
        
        # Calculer la distance totale parcourue
        distance_totale = self.moteursService.get_distance_traveled()
        
        print(couleur, reflexion, "| Ordre:", ordre)

        # 4. Détection des zones et signalement MQTT
        if self.couleur_avant != couleur:
            
            if couleur == "Rouge":
                # Entrée zone stockage voie GAUCHE
                self.dans_zone_stockage = True
                self.dans_zone_conflit = False
                self.distance_entree_stockage = distance_totale
                self.mqtt.signaler_entree("GAUCHE", 0)  # Distance 0 = à l'entrée
                
            elif couleur == "Bleu":
                # Entrée zone stockage voie DROITE
                self.dans_zone_stockage = True
                self.dans_zone_conflit = False
                self.distance_entree_stockage = distance_totale
                self.mqtt.signaler_entree("DROITE", 0)
                
            elif couleur == "Vert":
                # Sortie de la zone de conflit
                self.dans_zone_stockage = False
                self.dans_zone_conflit = False
                self.mqtt.signaler_sortie()
            
            self.couleur_avant = couleur
        
        # 4b. Envoyer régulièrement la distance depuis l'entrée (pour coopératif et peloton)
        if self.dans_zone_stockage or self.dans_zone_conflit:
            self.distance_depuis_entree = distance_totale - self.distance_entree_stockage
            self.mqtt.envoyer_distance(self.distance_depuis_entree)

        # 5. Appliquer l'ordre du contrôleur
        if ordre == "STOP":
            print(">>> ARRET COMMANDE PAR NODE-RED <<<")
            self.moteursService.avancer(0, 0)
            self.pid.restart()
            return
        
        elif ordre == "FOLLOW":
            # Mode peloton : maintenir la distance de sécurité avec le robot devant
            distance_robot_devant = self.mqtt.get_distance_robot_devant()
            
            if distance_robot_devant is not None:
                # Calculer l'écart avec la distance de sécurité
                distance_securite = self.mqtt.get_distance_securite()
                
                # La distance réelle entre nous = distance du robot devant - notre distance
                # On veut maintenir distance_securite (200mm)
                ecart = distance_robot_devant - self.distance_depuis_entree
                erreur = ecart - distance_securite
                
                if erreur > 50:  # Trop loin du robot devant, accélérer
                    self.facteur = min(1.5, 1.0 + erreur / 200)
                    print("PELOTON: Trop loin ({:.0f}mm), accélère".format(ecart))
                elif erreur < -50:  # Trop proche du robot devant, ralentir
                    self.facteur = max(0.3, 1.0 + erreur / 200)
                    print("PELOTON: Trop proche ({:.0f}mm), ralentit".format(ecart))
                else:  # Distance OK
                    self.facteur = 1.0
                    print("PELOTON: Distance OK ({:.0f}mm)".format(ecart))
            else:
                print("PELOTON: En attente info robot devant...")
                self.facteur = 0.8  # Avancer doucement

        # 6. Calcul PID et commande moteurs (seulement si GO ou FOLLOW)
        correction = self.pid.compute(50, reflexion)
        

        v_droit = max(0, self.vitesse_base - correction) * self.facteur
        v_gauche = max(0, self.vitesse_base + correction) * self.facteur

        # 7. Calculer la position avant d'envoyer la commande
        self.calculer_position()

        # 8. Logging
        temps_actuel = self.stopwatch.time()
        delta_temps = temps_actuel - self.temps_precedent
        self.temps_precedent = temps_actuel

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
