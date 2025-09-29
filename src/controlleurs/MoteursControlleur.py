from src.services.MoteurService import MoteurService
from src.services.CapteursService import CapteursService
from src.services.SystemeService import SystemeService

from src.calculs.BangBang import BangBang
from src.calculs.PID import PID
from src.calculs.PI import PI
from src.calculs.P import P

from src.utils.Log import Log
import time

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
        else:
            self.facteur = 1
        
        reflexion = self.capteursService.get_reflexion()
        correction = self.pid.compute(50, reflexion)
        
        
        self.logger.log(time.time()-self.start,reflexion, self.moteursService.get_distance_traveled())

        v_droit = max(0, self.vitesse_base - correction)*self.facteur
        v_gauche = max(0, self.vitesse_base + correction)*self.facteur

        self.moteursService.avancer(v_droit, v_gauche)
        
        
        
        
        