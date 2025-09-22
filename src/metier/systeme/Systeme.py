class Systeme:

    def __init__(self, systemeModel):
        self.systemeModel = systemeModel
        
    def getKu(self):
        return self.systemeModel.getKu()
    
    def getTu(self):
        return self.systemeModel.getTu()