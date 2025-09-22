from src.metier.moteurs.Moteur import Moteur
from src.configuration.Configuration import Configuration

class MoteurService:
    
    def __init__(self):
        
        self.moteur_droit = Moteur(Configuration().getMoteurDroit())
        self.moteur_gauche = Moteur(Configuration().getMoteurGauche())
    """
        def start_all(self):
        self.moteur_droit.start()
        self.moteur_gauche.start()
    """
    
    def avancer(self, vitesseDroite, vitesseGauche):
        
        self.moteur_droit.forward(vitesseDroite)
        self.moteur_gauche.forward(vitesseGauche)
        
    def stop_all(self):
        self.moteur_droit.stop()
        self.moteur_gauche.stop()

    def status(self):
        return {
            "droit": self.moteur_droit.status(),
            "gauche": self.moteur_gauche.status()
        }