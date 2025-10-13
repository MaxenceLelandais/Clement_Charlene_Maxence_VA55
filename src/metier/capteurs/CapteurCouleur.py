from pybricks.ev3devices import ColorSensor

class CapteurCouleur():
    def __init__(self, modelCapteur):
        
        self.capteurModel = modelCapteur
        self.port = modelCapteur.getPort()
        
        self.capteur = ColorSensor(self.port)
    
    def getColor(self):
        return self.capteur.color()

    def getReflexion(self):
        return self.capteur.reflection()
    
