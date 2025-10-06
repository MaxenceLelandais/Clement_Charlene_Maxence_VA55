from src.configuration.Configuration import Configuration

class SystemeService:
    
    def __init__(self):
        
        self.ku, self.tu, self.kp, self.ki, self.kd, self.vitesse = Configuration().getSysteme()
        
    def getKu(self):
        return self.ku
    
    def getTu(self):
        return self.tu
    
    def getKp(self):
        return self.kp
    
    def getKi(self):
        return self.ki
    
    def getKd(self):
        return self.kd
    
    def getVitesse(self):
        return self.vitesse
        