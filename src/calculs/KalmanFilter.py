import math

class KalmanFilter:
    """
    Filtre de Kalman pour la fusion de l'angle du gyroscope et de l'odométrie.
    
    Le modèle utilisé :
    - État : angle du robot (theta)
    - Mesure 1 : angle du gyroscope (mesure directe)
    - Mesure 2 : angle calculé par odométrie (à partir de la différence de distance des roues)
    
    Équations du filtre de Kalman :
    1. Prédiction :
       - x_pred = A * x + B * u
       - P_pred = A * P * A^T + Q
    
    2. Correction :
       - K = P_pred * H^T * (H * P_pred * H^T + R)^-1
       - x = x_pred + K * (z - H * x_pred)
       - P = (I - K * H) * P_pred
    
    Pour l'angle :
    - A = 1 (modèle constant)
    - H = 1 (mesure directe de l'angle)
    - Q = bruit du processus (incertitude du modèle)
    - R = bruit de mesure (incertitude des capteurs)
    """
    
    def __init__(self, process_variance=0.01, measurement_variance_gyro=0.5, measurement_variance_odom=2.0):
        """
        Initialise le filtre de Kalman
        
        Args:
            process_variance: Variance du bruit du processus (Q) - incertitude du modèle
            measurement_variance_gyro: Variance du bruit de mesure du gyroscope (R1)
            measurement_variance_odom: Variance du bruit de mesure de l'odométrie (R2)
        """
        # État initial (angle)
        self.x = 0.0  # angle estimé
        
        # Matrice de covariance de l'erreur
        self.P = 1.0  # incertitude initiale
        
        # Bruit du processus (Q)
        self.Q = process_variance
        
        # Bruit de mesure (R)
        self.R_gyro = measurement_variance_gyro
        self.R_odom = measurement_variance_odom
        
        # Pour le calcul de l'angle par odométrie
        self.previous_left_distance = 0.0
        self.previous_right_distance = 0.0
        self.wheel_base = 118.0  # Distance entre les roues en mm (à calibrer)
        
    def predict(self):
        """
        Étape de prédiction du filtre de Kalman
        Pour un modèle constant : x_pred = x (pas de changement attendu)
        """
        # x_pred = x (modèle constant)
        # P_pred = P + Q
        self.P = self.P + self.Q
        
    def update_with_gyro(self, angle_gyro):
        """
        Étape de correction avec la mesure du gyroscope
        
        Args:
            angle_gyro: Angle mesuré par le gyroscope (en degrés)
        """
        # Calcul du gain de Kalman : K = P / (P + R)
        K = self.P / (self.P + self.R_gyro)
        
        # Correction de l'état : x = x + K * (z - x)
        innovation = angle_gyro - self.x
        self.x = self.x + K * innovation
        
        # Mise à jour de la covariance : P = (1 - K) * P
        self.P = (1 - K) * self.P
        
    def update_with_odometry(self, left_distance, right_distance):
        """
        Étape de correction avec l'angle calculé par odométrie
        
        Args:
            left_distance: Distance parcourue par la roue gauche (en mm)
            right_distance: Distance parcourue par la roue droite (en mm)
        """
        # Calculer la différence de distance depuis la dernière mesure
        delta_left = left_distance - self.previous_left_distance
        delta_right = right_distance - self.previous_right_distance
        
        # Mettre à jour les distances précédentes
        self.previous_left_distance = left_distance
        self.previous_right_distance = right_distance
        
        # Calculer le changement d'angle à partir de l'odométrie
        # delta_theta = (delta_right - delta_left) / wheel_base
        delta_theta_rad = (delta_right - delta_left) / self.wheel_base
        delta_theta_deg = math.degrees(delta_theta_rad)
        
        # L'angle prédit par odométrie
        angle_odom = self.x + delta_theta_deg
        
        # Calcul du gain de Kalman pour l'odométrie
        K = self.P / (self.P + self.R_odom)
        
        # Correction de l'état
        innovation = angle_odom - self.x
        self.x = self.x + K * innovation
        
        # Mise à jour de la covariance
        self.P = (1 - K) * self.P
        
    def update_fusion(self, angle_gyro, left_distance, right_distance):
        """
        Fusion des deux mesures (gyroscope et odométrie)
        
        Args:
            angle_gyro: Angle mesuré par le gyroscope (en degrés)
            left_distance: Distance parcourue par la roue gauche (en mm)
            right_distance: Distance parcourue par la roue droite (en mm)
        
        Returns:
            float: Angle estimé fusionné (en degrés)
        """
        # Étape de prédiction
        self.predict()
        
        # Calculer l'angle par odométrie
        delta_left = left_distance - self.previous_left_distance
        delta_right = right_distance - self.previous_right_distance
        
        # Mettre à jour les distances précédentes
        self.previous_left_distance = left_distance
        self.previous_right_distance = right_distance
        
        # Calculer le changement d'angle à partir de l'odométrie
        delta_theta_rad = (delta_right - delta_left) / self.wheel_base
        delta_theta_deg = math.degrees(delta_theta_rad)
        
        # L'angle prédit par odométrie (angle précédent + delta)
        angle_odom = self.x + delta_theta_deg
        
        # Fusion des deux mesures avec pondération par la covariance
        # Méthode de fusion optimale
        w_gyro = 1.0 / self.R_gyro
        w_odom = 1.0 / self.R_odom
        
        angle_fused = (w_gyro * angle_gyro + w_odom * angle_odom) / (w_gyro + w_odom)
        
        # Calcul du gain de Kalman combiné
        R_combined = 1.0 / (w_gyro + w_odom)
        K = self.P / (self.P + R_combined)
        
        # Correction de l'état avec la mesure fusionnée
        self.x = self.x + K * (angle_fused - self.x)
        
        # Mise à jour de la covariance
        self.P = (1 - K) * self.P
        
        return self.x
        
    def get_angle(self):
        """
        Retourne l'angle estimé actuel
        
        Returns:
            float: Angle estimé (en degrés)
        """
        return self.x
        
    def reset(self, angle=0.0):
        """
        Réinitialise le filtre
        
        Args:
            angle: Angle initial (en degrés)
        """
        self.x = angle
        self.P = 1.0
        self.previous_left_distance = 0.0
        self.previous_right_distance = 0.0
        
    def set_wheel_base(self, wheel_base):
        """
        Définit la distance entre les roues (voie)
        
        Args:
            wheel_base: Distance entre les roues en mm
        """
        self.wheel_base = wheel_base
