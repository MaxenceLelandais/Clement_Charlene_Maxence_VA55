from src.services.ConfigService import ConfigService
from src.controlleurs.capteurs.CapteurCouleur import CapteurCouleur
from src.models.CapteurModel import CapteurModel


class CapteursService:
    
    def __init__(self):
        
        config = ConfigService()
        
        self.capteur_couleur = CapteurCouleur(CapteurModel(config["capteur"]["couleur"]))

    def status(self):
        return {
            "capteur_couleur": self.capteur_couleur.status()
        }