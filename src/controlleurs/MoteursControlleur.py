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

        self.angle_actuel = 0
        self.vitesse = 0
        self.post_x, self.post_y = 0,0
                
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

        start = time.time()
        
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


        self.position(time.time()-start)


        print(self.post_x, self.post_y)

        self.logger.log(time.time()-self.start,self.post_x, self.post_y)
        self.moteursService.avancer(v_droit, v_gauche)


    def position(self, temps):

        circonference = self.moteursService.getCirconferenceWheel()

        degret = self.capteursService.get_angle()
        degret_par_seconde = self.capteursService.get_speed()

        vitesse = (circonference/360)*degret_par_seconde
        distance = vitesse * temps
        
        distance_left, distance_right = self.moteursService.get_distance_roue()
        delta_distance = (distance_left + distance_right)/2
        delta_theta = (distance_right - distance_left) / circonference  # in radians

        self.angle_actuel += math.degrees(delta_theta)
        self.post_x += delta_distance * math.cos(math.radians(self.angle_actuel))
        self.post_y += delta_distance * math.sin(math.radians(self.angle_actuel))



        


        
        
        
        