from pybricks.ev3devices import ColorSensor
from src.metier.capteurs.Capteurs import Capteurs

class CapteurCouleur(Capteurs):
    def __init__(self, modelCapteur):
        
        super.__init__(modelCapteur)
        
        self.capteur = ColorSensor(self.port)
    
    def getColor(self):
        return self.capteur.color()

    def getReflexion(self):
        return self.capteur.reflection()
    
