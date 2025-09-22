import time

class P:
    
    def __init__(self, kp):
        self.kp = kp

        self.derniere_erreur = 0.0

    def restart(self):
        
        self.derniere_erreur = 0.0

    def compute(self, pointInit, mesure):

        error = pointInit - mesure

        e_kp = self.kp * error

        return e_kp
