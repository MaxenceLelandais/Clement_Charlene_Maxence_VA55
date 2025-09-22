class Systeme:

    def __init__(self, systemeModel):
        self.systemeModel = systemeModel
        
    def getKu(self):
        return self.systemeModel.getKu()
    
    def getTu(self):
        return self.systemeModel.getTu()
    
    def getKp(self):
        return self.systemeModel.getKp()
    
    def getKi(self):
        return self.systemeModel.getKi()
    
    def getVitesse(self):
        return self.systemeModel.getVitesse()