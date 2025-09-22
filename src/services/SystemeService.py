from src.metier.systeme.Systeme import Systeme
from configuration.Configuration import Configuration

class SystemeService:
    
    def __init__(self):
        
        self.systeme = Systeme(Configuration().getSysteme())
        
    def getKu(self):
        return self.systeme.getKu()
    
    def getTu(self):
        return self.systeme.getTu()