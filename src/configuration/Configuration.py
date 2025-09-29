from src.configuration.ConfigService import ConfigService

from src.models.CapteurModel import CapteurModel
from src.models.CapteurUltrasonModel import CapteurUltrasonModel
from src.models.MoteurModel import MoteurModel
from src.models.SystemeModel import SystemeModel

class Configuration:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return  # avoid reinitialization
        self._initialized = True

        self.configService = ConfigService()
        self.capteurCouleur = CapteurModel(self.configService["capteur"]["couleur"])
        self.capteurUltrason = CapteurUltrasonModel(self.configService["capteur"]["ultrason"])
        self.moteur_droit = MoteurModel(self.configService["moteur"]["droit"])
        self.moteur_gauche = MoteurModel(self.configService["moteur"]["gauche"])
        self.systeme = SystemeModel(self.configService["system"])

    def getCapteurCouleur(self):
        return self.capteurCouleur
    
    def getCapteurUltrason(self):
        return self.capteurUltrason
    
    def getMoteurDroit(self):
        return self.moteur_droit
    
    def getMoteurGauche(self):
        return self.moteur_gauche
    
    def getSysteme(self):
        return self.systeme