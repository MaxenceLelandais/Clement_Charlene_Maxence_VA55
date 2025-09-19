from pybricks.ev3devices import ColorSensor
from src.controlleurs.capteurs.Capteurs import Capteurs
import time

class CapteurCouleur(Capteurs):
    def __init__(self, modelCapteurCouleur):
        
        super.__init__(modelCapteurCouleur)
        
        self.capteur = ColorSensor(modelCapteurCouleur.getPort())
        self.d_erreur = (50-self.getReflexion())

        self.list = []
        self.list.append(self.d_erreur)
        self.nbr = 5
        self.start = time.time()
    
    def getColor(self):
        return self.capteur.color()

    def getReflexion(self):
        return self.capteur.reflection()
    

    def getProportionnel(self):

        ku = 2
        tu = 2
        kp = 0.6*ku
        ki = 1.2*ku/tu
        kd = 3*ku*tu/40
        vitesse = 300


        erreur = (50-self.getReflexion())
        if len(self.list)>=self.nbr:
            del self.list[0]
        self.list.append(erreur)

        diff_temps = time.time()-self.start

        e_kp = erreur*kp
        somme = 0
        for i in self.list:
            somme+=i
        e_ki = somme*ki
        e_kd = ((erreur - self.d_erreur)/diff_temps)*kd

        self.d_erreur = erreur
        self.start = time.time()

        corr = e_kp+e_ki+e_kd
        

        speedMoteurDroit = max(0,vitesse + corr)
        speedMoteurGauche = max(0,vitesse - corr)


        return speedMoteurGauche, speedMoteurDroit