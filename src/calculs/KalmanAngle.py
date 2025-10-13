import math


class KalmanAngle:
    """Simple 1D Kalman filter for angle estimation.

    State is angle in radians. Predict step integrates angular rate (deg/s).
    All inputs from sensors are in degrees or deg/s and are converted
    to radians internally.
    """

    def __init__(self, initial_angle_deg=0.0, p0_deg2=1.0, q_deg2=0.01, r_deg2=1.0):
        # convert variances from deg^2 to rad^2
        deg2rad = math.radians(1.0)
        self.x = math.radians(initial_angle_deg)  # state (rad)
        self.P = (p0_deg2) * (deg2rad ** 2)
        self.Q = (q_deg2) * (deg2rad ** 2)
        self.R = (r_deg2) * (deg2rad ** 2)

    def predict(self, omega_deg_s, dt):
        """Predict step using angular rate omega (deg/s) over dt seconds."""
        omega_rad_s = math.radians(omega_deg_s)
        self.x = self.x + omega_rad_s * dt
        # normalize angle to [-pi, pi] to avoid drift of representation
        self.x = (self.x + math.pi) % (2 * math.pi) - math.pi
        self.P = self.P + self.Q

    def update(self, z_angle_deg):
        """Update step with measured absolute angle (deg)."""
        z = math.radians(z_angle_deg)
        # residual (ensure within [-pi,pi])
        y = z - self.x
        y = (y + math.pi) % (2 * math.pi) - math.pi

        S = self.P + self.R
        K = self.P / S if S != 0 else 0.0

        self.x = self.x + K * y
        self.x = (self.x + math.pi) % (2 * math.pi) - math.pi
        self.P = (1.0 - K) * self.P

    def get_theta(self):
        """Return estimated angle in radians."""
        return self.x

    def get_theta_deg(self):
        return math.degrees(self.x)