import numpy as np

class Kalman:

    def __init__(self):
        self.Ri = 400                # variance de mesure
        self.Pi_i_moins_1 = 625      # incertitude initiale
        self.Xi_i_moins_1 = 2025     # estimation initiale

    def appliquer(self, angle_mesure):
        """
        Applique un filtre de Kalman 1D à une mesure d'angle.
        Retourne l'angle filtré.
        """
        Zi = angle_mesure

        # Gain de Kalman
        Ki = self.Pi_i_moins_1 / (self.Pi_i_moins_1 + self.Ri)

        # Nouvelle estimation
        Xi_i = (1 - Ki) * self.Xi_i_moins_1 + Ki * Zi

        # Mise à jour de l’incertitude
        Pi_i = (1 - Ki) * self.Pi_i_moins_1

        # Préparer la prochaine itération
        self.Pi_i_moins_1 = Pi_i
        self.Xi_i_moins_1 = Xi_i

        # Retourner l'estimation courante
        return Xi_i


if __name__ == "__main__":
    # Exemple d'utilisation
    kalman = Kalman()

    mesures = [2010, 2102, 1999, 2037, 2081, 1976, 2018, 2010]
    estimations = []

    for m in mesures:
        estimations.append(kalman.appliquer(m))

    print("Estimations :", np.round(estimations, 2))
