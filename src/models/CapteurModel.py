from src.metier.enums.PortEnum import PortEnum

class CapteurModel():
    
    def __init__(self, data):
        
        self.nom = data["nom"]
        self.port = PortEnum.from_str(data["port"])
        
    def getNom(self):
        return self.nom
    
    def getPort(self):
        return self.port