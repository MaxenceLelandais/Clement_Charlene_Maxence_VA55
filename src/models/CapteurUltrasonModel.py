from src.metier.enums.PortEnum import PortEnum

class CapteurUltrasonModel():
    
    def __init__(self, data):
        
        self.nom = data["nom"]
        self.port = PortEnum.from_str(data["port"])
        self.distanceDetection = data["distance"]
        
    def getNom(self):
        return self.nom
    
    def getPort(self):
        return self.port
    
    def getDistance(self):
        return self.distanceDetection