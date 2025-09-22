import time
import os

class Log:
    
    def __init__(self):
        heures = time.localtime()
        val = "{:02d}-{:02d}-{:04d}_{:02d}-{:02d}-{:02d}".format(
            heures[2], heures[1], heures[0], heures[3], heures[4], heures[5]
        )
        
        # Dossier logs
        self.repertoire = "/home/robot/Clement_Charlene_Maxence_VA55/logs"
        
        # Créer le dossier logs s'il n'existe pas
        try:
            os.mkdir(self.repertoire)
        except OSError:
            pass  # le dossier existe déjà
        
        # Nom du fichier CSV
        self.nom = "{}/LOG-{}.csv".format(self.repertoire, val)
        
        
    def log(self, correction, distance, reflexion):
        # Ajouter une ligne dans le CSV
        with open(self.nom, "a") as file:
            line = "{},{},{}\n".format(correction, distance, reflexion)
            file.write(line)
