import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Lecture du fichier CSV ---
fichier_csv = "LOG-06-10-2025_16-23-48.csv"  # Remplacer par le chemin de ton fichier

temps = []
pos_x = []
pos_y = []

with open(fichier_csv, newline='') as csvfile:
    lecteur = csv.reader(csvfile)
    for ligne in lecteur:
        if len(ligne) < 3:
            continue  # ignorer les lignes incomplètes
        t, x, y = map(float, ligne)
        temps.append(t)
        pos_x.append(x)
        pos_y.append(y)

# --- Création de la figure ---
fig, ax = plt.subplots()
ax.set_xlabel("Position X")
ax.set_ylabel("Position Y")
ax.set_title("Trajet animé")
line, = ax.plot([], [], 'b-', lw=2)
point, = ax.plot([], [], 'ro')  # point qui se déplace

# Ajuster les limites de l'axe
ax.set_xlim(min(pos_x) - 1, max(pos_x) + 1)
ax.set_ylim(min(pos_y) - 1, max(pos_y) + 1)

# --- Fonction d'initialisation ---
def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point

# --- Fonction d'animation ---
def update(frame):
    line.set_data(pos_x[:frame+1], pos_y[:frame+1])
    point.set_data(pos_x[frame], pos_y[frame])
    return line, point

# --- Création de l'animation ---
ani = FuncAnimation(fig, update, frames=len(temps), init_func=init, blit=True, interval=1)

plt.show()
