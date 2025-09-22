from src.metier.systeme.Systeme import Systeme
from src.configuration.Configuration import Configuration

class SystemeService:
    
    def __init__(self):
        
        self.systeme = Systeme(Configuration().getSysteme())
        
    def getKu(self):
        return self.systeme.getKu()
    
    def getTu(self):
        return self.systeme.getTu()
    
    def getKp(self):
        return self.systeme.getKp()
    
    def getKi(self):
        return self.systeme.getKi()
    
    def getVitesse(self):
        return self.systeme.getVitesse()
        