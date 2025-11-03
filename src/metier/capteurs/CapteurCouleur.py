from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Color
class CapteurCouleur():
    def __init__(self, modelCapteur):
        
        self.capteurModel = modelCapteur
        self.port = modelCapteur.getPort()
        
        self.capteur = ColorSensor(self.port)

        self.color_names = {
            Color.BLACK: "Noir",
            Color.BLUE: "Bleu",
            Color.GREEN: "Vert",
            Color.YELLOW: "Jaune",
            Color.RED: "Rouge",
            Color.WHITE: "Blanc",
            Color.BROWN: "Marron"
        }

    def getColor(self):
        color = self.capteur.color()
        return self.color_names.get(color, "Inconnu")

    def getReflexion(self):
        return self.capteur.reflection()
    
