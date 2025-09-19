import time

class PID:
    """
    Implémentation d'un contrôleur PID générique.
    """

    def __init__(self, kp: float, ki: float, kd: float, max_history: int = 5):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.max_history = max_history
        self.errors = []
        self.last_error = 0.0
        self.last_time = time.time()

    def reset(self):
        """Réinitialise l'historique des erreurs."""
        self.errors = []
        self.last_error = 0.0
        self.last_time = time.time()

    def compute(self, setpoint: float, measurement: float) -> float:
        """
        Calcule la sortie PID en fonction de la consigne (setpoint)
        et de la mesure actuelle (measurement).
        """
        # Erreur = Consigne - Mesure
        error = setpoint - measurement

        # Temps écoulé
        now = time.time()
        dt = now - self.last_time if self.last_time else 1e-6
        self.last_time = now

        # --- Composantes PID ---
        # Proportionnel
        e_kp = self.kp * error

        # Intégral (somme des erreurs)
        if len(self.errors) >= self.max_history:
            self.errors.pop(0)
        self.errors.append(error)
        e_ki = self.ki * sum(self.errors)

        # Dérivé (variation de l’erreur)
        e_kd = self.kd * (error - self.last_error) / dt if dt > 0 else 0.0

        # Sauvegarde
        self.last_error = error

        # Résultat PID
        return e_kp + e_ki + e_kd
