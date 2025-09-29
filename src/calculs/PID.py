import time

class PID:
    
    def __init__(self, kp, ki, kd, max_histoire = 500):
        self.kp = kp
        self.ki = ki
        self.kd = kd

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
        dt = start - self.dernier_temps if self.dernier_temps else 1e-6
        self.dernier_temps = start

        e_kp = self.kp * error

        if len(self.errors) >= self.max_histoire:
            self.errors.pop(0)
        self.errors.append(error)
        e_ki = self.ki * sum(self.errors)*dt

        e_kd = self.kd * (error - self.derniere_erreur) / dt if dt > 0 else 0.0

        self.derniere_erreur = error

        return e_kp + e_ki + e_kd
