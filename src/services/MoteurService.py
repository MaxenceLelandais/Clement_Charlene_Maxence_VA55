from src.services.ConfigService import ConfigService
from src.metier.moteurs.Moteur import Moteur
from src.models.MoteurModel import MoteurModel


class MoteurService:
    
    def __init__(self):
        
        config = ConfigService()
        
        self.moteur_droit = Moteur(MoteurModel(config["moteur"]["droit"]))
        self.moteur_gauche = Moteur(MoteurModel(config["moteur"]["gauche"]))
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