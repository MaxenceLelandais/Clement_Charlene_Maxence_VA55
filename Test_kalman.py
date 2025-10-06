import numpy as np
import matplotlib.pyplot as plt

# --- Données fournies ---
t = 0.5  # intervalle de temps
distance_mesuree = np.array([0, 6, 12, 14, 20, 24])
vitesse_mesuree = np.array([9, 11, 12, 8, 10, 9])

erreur_mesure_distance = 2
erreur_mesure_vitesse = 1

n = len(distance_mesuree)

# --- Initialisation du filtre de Kalman ---
# État [position, vitesse]
x_est = np.array([0.0, 0.0])
P = np.eye(2) * 1.0

# Matrices du modèle
A = np.array([[1, t],
              [0, 1]])  # transition
H = np.eye(2)  # mesure sur position et vitesse

Q = np.array([[1e-4, 0],
              [0, 1e-4]])  # bruit du processus
R = np.array([[erreur_mesure_distance**2, 0],
              [0, erreur_mesure_vitesse**2]])  # bruit des mesures

estimation = []

# --- Filtrage de Kalman ---
for i in range(n):
    z = np.array([distance_mesuree[i], vitesse_mesuree[i]])

    # 1) Prédiction
    x_pred = A @ x_est
    P_pred = A @ P @ A.T + Q

    # 2) Correction
    K = P_pred @ H.T @ np.linalg.inv(H @ P_pred @ H.T + R)
    x_est = x_pred + K @ (z - H @ x_pred)
    P = (np.eye(2) - K @ H) @ P_pred

    estimation.append(x_est.copy())

# --- Visualisation ---
estimation = np.array(estimation)
temps = np.arange(0, n*t, t)

plt.figure(figsize=(10,5))
plt.plot(temps, distance_mesuree, 'ro', label='Position mesurée')
plt.plot(temps, estimation[:,0], 'b-', label='Position estimée (Kalman)')
plt.xlabel('Temps (s)')
plt.ylabel('Position')
plt.title('Filtre de Kalman - Position')
plt.legend()
plt.show()

plt.figure(figsize=(10,5))
plt.plot(temps, vitesse_mesuree, 'ro', label='Vitesse mesurée')
plt.plot(temps, estimation[:,1], 'b-', label='Vitesse estimée (Kalman)')
plt.xlabel('Temps (s)')
plt.ylabel('Vitesse')
plt.title('Filtre de Kalman - Vitesse')
plt.legend()
plt.show()
