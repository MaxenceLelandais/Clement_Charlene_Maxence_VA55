from src.metier.capteurs.CapteurCouleur import CapteurCouleur
from src.configuration.Configuration import Configuration

class CapteursService:
    
    def __init__(self):
        
        self.capteur_couleur = CapteurCouleur(Configuration().getCapteurCouleur())

    def status(self):
        return {
            "capteur_couleur": self.capteur_couleur.status()
        }
        
    def get_reflexion(self):
        return self.capteur_couleur.getReflexion()