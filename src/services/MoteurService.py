from src.metier.moteurs.Moteur import Moteur
from src.configuration.Configuration import Configuration

class MoteurService:
    
    def __init__(self):
        
        self.moteur_droit = Moteur(Configuration().getMoteurDroit())
        self.moteur_gauche = Moteur(Configuration().getMoteurGauche())

    
    def avancer(self, vitesseDroite, vitesseGauche):
        
        self.moteur_droit.forward(vitesseDroite)
        self.moteur_gauche.forward(vitesseGauche)
        
    def stop_all(self):
        self.moteur_droit.stop()
        self.moteur_gauche.stop()
        
    def get_distance_traveled(self):
        gauche_angle = self.moteur_gauche.getAngle()
        droite_angle = self.moteur_droit.getAngle()
        wheel_circumference = 3.14159 * 56
        left_distance = (gauche_angle / 360) * wheel_circumference
        right_distance = (droite_angle / 360) * wheel_circumference
        return (left_distance + right_distance) / 2

    def status(self):
        return {
            "droit": self.moteur_droit.status(),
            "gauche": self.moteur_gauche.status()
        }