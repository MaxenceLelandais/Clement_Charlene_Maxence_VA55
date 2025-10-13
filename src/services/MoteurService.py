from src.metier.moteurs.Moteur import Moteur
from src.configuration.Configuration import Configuration

class MoteurService:
    
    def __init__(self):
        portd,vitessed,stopd = Configuration().getMoteurDroit()
        portg,vitesseg,stopg = Configuration().getMoteurGauche()
        self.moteur_droit = Moteur(portd,vitessed,stopd)
        self.moteur_gauche = Moteur(portg,vitesseg,stopg)

    
    def avancer(self, vitesseDroite, vitesseGauche):
        
        self.moteur_droit.forward(vitesseDroite)
        self.moteur_gauche.forward(vitesseGauche)
        
    def stop_all(self):
        self.moteur_droit.stop()
        self.moteur_gauche.stop()
        
    def get_distance_traveled(self):
        left_distance, right_distance = self.get_distance_roue()
        return (left_distance + right_distance) / 2
    
    def get_distance_roue(self):
        gauche_angle = self.moteur_gauche.getAngle()
        droite_angle = self.moteur_droit.getAngle()
        left_distance = (gauche_angle / 360) * self.getCirconferenceWheel()
        right_distance = (droite_angle / 360) * self.getCirconferenceWheel()
        return left_distance, right_distance
    
    def getCirconferenceWheel(self):
        return 3.14159 * 56

    def status(self):
        return {
            "droit": self.moteur_droit.status(),
            "gauche": self.moteur_gauche.status()
        }