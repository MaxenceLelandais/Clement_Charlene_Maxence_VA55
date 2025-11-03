from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Color

class CapteurCouleur:
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

        self.couleur = ""
        self.reflexion = 0
        self.delay = 0

    def getColor(self):
        if self.delay%3==0 or self.couleur == "":
            self.couleur = self.color_names.get(self.capteur.color(), "Inconnu")
        self.delay +=1
        return self.couleur

    def getReflexion(self):
        return self.capteur.reflection()

