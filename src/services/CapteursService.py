from src.metier.capteurs.CapteurCouleur import CapteurCouleur
from src.metier.capteurs.CapteurUltrason import CapteurUltrason
from src.metier.capteurs.CapteurGyroscopique import CapteurGyroscopique
from src.configuration.Configuration import Configuration

class CapteursService:
    
    def __init__(self):
        
        self.capteur_couleur = CapteurCouleur(Configuration().getCapteurCouleur())
        self.capteur_ultrason = CapteurUltrason(Configuration().getCapteurUltrason())
        self.capteur_gyro = CapteurGyroscopique(Configuration().getCapteurGyro())

    def status(self):
        return {
            "capteur_couleur": self.capteur_couleur.status()
        }
        
    def get_reflexion(self):
        return self.capteur_couleur.getReflexion()
    
    
    def get_detection(self):
        return self.capteur_ultrason.detection()
    
    def get_angle(self):
        return self.capteur_gyro.angle()
    

    def get_speed(self):
        return self.capteur_gyro.speed()