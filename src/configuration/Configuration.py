from src.metaclasses.Singleton import SingletonMeta
from configuration.ConfigService import ConfigService

from src.models.CapteurModel import CapteurModel
from src.models.MoteurModel import MoteurModel
from models.SystemeModel import SystemeModel

class Configuration(metaclass=SingletonMeta):
    value: str = None

    def __init__(self) -> None:
        self.configService = ConfigService()
        
        self.capteurCouleur = CapteurModel(self.configService["capteur"]["couleur"])
        self.moteur_droit = MoteurModel(self.configService["moteur"]["droit"])
        self.moteur_gauche = MoteurModel(self.configService["moteur"]["gauche"])
        self.systeme = SystemeModel(self.configService["system"])

    def getCapteurCouleur(self):
        return self.capteurCouleur
    
    def getMoteurDroit(self):
        return self.moteur_droit
    
    def getMoteurGauche(self):
        return self.moteur_gauche
    
    def getSysteme(self):
        return self.systeme