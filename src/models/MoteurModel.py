from src.enums.PortEnum import PortEnum
from src.enums.StopEnum import StopEnum

class MoteurModel:
    
    def __init__(self, data):
        
        self.nom = data["nom"]
        self.port = PortEnum.from_str(data["port"])
        self.vitesse= data["vitesse"]
        self.stop= StopEnum.from_str(data["stop"])
        
    def getNom(self):
        return self.nom
    
    def getPort(self):
        return self.port
    
    def getVitesse(self):
        return self.vitesse
    
    def getStop(self):
        return self.stop
        