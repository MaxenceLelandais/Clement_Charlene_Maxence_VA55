import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fichier_csv = "LOG-06-10-2025_16-23-48.csv"

temps = []
pos_x = []
pos_y = []

with open(fichier_csv, newline='') as csvfile:
    lecteur = csv.reader(csvfile, delimiter=',')  # ajuster le séparateur si nécessaire
    next(lecteur)  # sauter l'en-tête si elle existe
    for ligne in lecteur:
        if len(ligne) < 3:
            continue
        t, x, y = map(lambda s: float(s.replace(',', '.')), ligne)
        temps.append(t)
        pos_x.append(x)
        pos_y.append(y)

fig, ax = plt.subplots()
ax.set_xlabel("Position X")
ax.set_ylabel("Position Y")
ax.set_title("Trajet animé")
line, = ax.plot([], [], 'b-', lw=2)
point, = ax.plot([], [], 'ro')

ax.set_xlim(min(pos_x) - 1, max(pos_x) + 1)
ax.set_ylim(min(pos_y) - 1, max(pos_y) + 1)

def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point

def update(frame):
    line.set_data(pos_x[:frame+1], pos_y[:frame+1])
    point.set_data([pos_x[frame]], [pos_y[frame]])
    return line, point

ani = FuncAnimation(fig, update, frames=len(temps), init_func=init, blit=True, interval=1)

plt.show()
