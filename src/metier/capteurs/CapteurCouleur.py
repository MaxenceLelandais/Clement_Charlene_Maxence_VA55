from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Color
from pybricks.tools import wait
import _thread

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

        self.couleur = "Inconnu"
        self.reflexion = 0
        self.running = True
        self._lock = _thread.allocate_lock()

        _thread.start_new_thread(self._getColor, ())

    def _getColor(self):
        while self.running:
            color = self.capteur.color()
            with self._lock:
                self.couleur = self.color_names.get(color, "Inconnu")
            wait(200)

    def getColor(self):
        with self._lock:
            return self.couleur

    def getReflexion(self):
        return self.capteur.reflection()

    def stop(self):
        self.running = False
