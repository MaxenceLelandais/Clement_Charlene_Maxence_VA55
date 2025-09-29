class SystemeModel():
    
    def __init__(self, data):
        
        facteurs = data["facteurs"]
        
        self.ku = facteurs["ku"]
        self.tu = facteurs["tu"]
        self.kp = facteurs["kp"]
        self.ki = facteurs["ki"]
        self.kd = facteurs["kd"]
        self.vitesse = facteurs["vitesse"]
        
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