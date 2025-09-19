class SystemModel():
    
    def __init__(self, data):
        
        facteurs = data["facteurs"]
        
        self.ku = facteurs["ku"]
        self.tu = facteurs["tu"]
        
    def getKu(self):
        return self.ku
    
    def getTu(self):
        return self.tu