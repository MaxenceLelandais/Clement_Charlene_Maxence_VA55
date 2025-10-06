from pybricks.ev3devices import ColorSensor

class CapteurCouleur():
    def __init__(self, port):
        
        self.capteur = ColorSensor(port)
    
    def getColor(self):
        return self.capteur.color()

    def getReflexion(self):
        return self.capteur.reflection()
    
