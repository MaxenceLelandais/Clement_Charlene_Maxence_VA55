from src.configuration.ConfigService import ConfigService

from src.metier.enums.PortEnum import PortEnum
from src.metier.enums.StopEnum import StopEnum

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

    def getDataCapteurCouleur(self):
        return PortEnum.from_str(self.configService["capteur"]["couleur"]["port"])
    
    def getDataCapteurUltrason(self):
        data = self.configService["capteur"]["ultrason"]
        port = PortEnum.from_str(data["port"])
        distanceDetection = data["distance"]
        return port, distanceDetection
    
    def getDataCapteurGyro(self):
        return PortEnum.from_str(self.configService["capteur"]["gyro"]["port"])
    
    def getMoteurDroit(self):
        data = self.configService["moteur"]["droit"]
        port = PortEnum.from_str(data["port"])
        vitesse= data["vitesse"]
        stop= StopEnum.from_str(data["stop"])
        return port,vitesse,stop
    
    def getMoteurGauche(self):
        data = self.configService["moteur"]["gauche"]
        port = PortEnum.from_str(data["port"])
        vitesse= data["vitesse"]
        stop= StopEnum.from_str(data["stop"])
        return port,vitesse,stop
    
    def getSysteme(self):
        data = self.configService["system"]
        facteurs = data["facteurs"]
        
        ku = facteurs["ku"]
        tu = facteurs["tu"]
        kp = facteurs["kp"]
        ki = facteurs["ki"]
        kd = facteurs["kd"]
        vitesse = facteurs["vitesse"]
        return ku, tu, kp, ki, kd, vitesse