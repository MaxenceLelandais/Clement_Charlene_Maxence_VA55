from src.models.SystemModel import SystemModel
from src.services.MoteurService import MoteurService
from src.services.CapteursService import CapteursService
from src.services.ConfigService import ConfigService

from src.calculs.PID import PID

class MoteursControlleur:
    """
    Contrôleur de moteurs basé sur un régulateur PID
    pour suivre une ligne ou maintenir une consigne.
    """

    def __init__(self):
        self.moteursService = MoteurService()
        self.capteursService = CapteursService()
        self.configService = ConfigService()
        
        # Chargement du modèle système
        systemModel = SystemModel(self.configService["system"])
        # Initialisation PID avec Ku, Tu
        ku = systemModel.getKu()
        tu = systemModel.getTu()

        kp = 0.6 * ku
        ki = 1.2 * ku / tu
        kd = 3 * ku * tu / 40

        self.pid = PID(kp, ki, kd)
        self.vitesse_base = 300

    def envoieCommandeMoteurs(self):
        reflexion = self.capteursService.get_reflexion()
        correction = self.pid.compute(setpoint=50, measurement=reflexion)

        v_droit = max(0, self.vitesse_base + correction)
        v_gauche = max(0, self.vitesse_base - correction)

        self.moteursService.avancer(v_droit, v_gauche)

