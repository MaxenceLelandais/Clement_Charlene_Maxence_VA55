from src.services.MoteurService import MoteurService
from src.services.CapteursService import CapteursService
from src.services.SystemeService import SystemeService

from src.calculs.BangBang import BangBang
from src.calculs.PID import PID
from src.calculs.PI import PI
from src.calculs.P import P

from src.utils.Log import Log
import time
import math

class MoteursControlleur:

    def __init__(self):
        self.moteursService = MoteurService()
        self.capteursService = CapteursService()
        self.systemeService = SystemeService()
        
        self.logger = Log()
        
        self.ralentissement_en_pourcentage = 0.8
        self.facteur = 1
      
        self.vitesse_base = self.systemeService.getVitesse()
        
        self.pourPID()
        
        self.start = time.time()

        # Initialisation de la position
        self.post_x, self.post_y = 0.0, 0.0
        self.temps_precedent = time.time()
        self.distance_left = 0.0
        self.distance_right = 0.0

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
        
        if self.capteursService.get_detection():
            self.facteur *= self.ralentissement_en_pourcentage
            
            if self.facteur<0.1:
                self.facteur = 0
                self.pid.restart()
        else:
            self.facteur = 1
        
        reflexion = self.capteursService.get_reflexion()
        correction = self.pid.compute(50, reflexion)
        
        

        v_droit = max(0, self.vitesse_base - correction)*self.facteur
        v_gauche = max(0, self.vitesse_base + correction)*self.facteur

        # Calculer la position avant d'envoyer la commande
        self.calculer_position()

        # Afficher et logger la position
        print(self.post_x, self.post_y)
        self.logger.log(time.time()-self.start, self.post_x, self.post_y)
        
        self.moteursService.avancer(v_droit, v_gauche)


    def calculer_position(self):
        """
        Calcule la position (x, y) du robot en utilisant l'odométrie
        avec l'angle du gyroscope et la vitesse moyenne des roues
        """
        # Calculer le temps écoulé depuis la dernière mise à jour
        temps_actuel = time.time()
        delta_temps = temps_actuel - self.temps_precedent
        self.temps_precedent = temps_actuel
        
        # Récupérer l'angle du gyroscope (en degrés)
        theta_deg = self.capteursService.get_angle()
        
        # Convertir l'angle en radians pour les calculs trigonométriques
        theta_rad = math.radians(theta_deg)
        
        # Calculer la distance parcourue par chaque roue
        new_distance_left, new_distance_right = self.moteursService.get_distance_roue()
        
       
        
        
        # Vitesse linéaire moyenne du robot (mm/s)
        vitesse_moyenne = ((self.distance_right - new_distance_right) / (2 * delta_temps) if delta_temps > 0 else 0)
        
        # Calculer le déplacement en x et y
        deplacement_x = vitesse_moyenne * math.cos(theta_rad) * delta_temps
        deplacement_y = vitesse_moyenne * math.sin(theta_rad) * delta_temps
        
        self.distance_left = new_distance_left
        new_distance_right -= self.distance_right
        
        # Mettre à jour la position
        self.post_x += deplacement_x
        self.post_y += deplacement_y



        


        
        
        
        