from src.services.ConfigService import ConfigService
from src.models.SystemModel import SystemModel


class SystemService:
    
    def __init__(self):
        
        config = ConfigService()
        
        self.systemModel = SystemModel(config["system"])
        
    def getKu(self):
        return self.systemModel.getKu()
    
    def getTu(self):
        return self.systemModel.getTu()