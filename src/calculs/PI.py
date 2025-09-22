import time

class PI:
    
    def __init__(self, kp, ki, max_histoire = 5):
        self.kp = kp
        self.ki = ki

        self.max_histoire = max_histoire
        self.errors = []
        self.derniere_erreur = 0.0
        self.dernier_temps = time.time()

    def restart(self):
        
        self.errors = []
        self.derniere_erreur = 0.0
        self.dernier_temps = time.time()

    def compute(self, pointInit, mesure):

        error = pointInit - mesure

        start = time.time()
        self.dernier_temps = start

        e_kp = self.kp * error

        if len(self.errors) >= self.max_histoire:
            self.errors.pop(0)
        self.errors.append(error)
        e_ki = self.ki * sum(self.errors)

        self.derniere_erreur = error

        return e_kp + e_ki
