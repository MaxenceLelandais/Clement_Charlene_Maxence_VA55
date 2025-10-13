from pybricks.ev3devices import UltrasonicSensor as EV3Ultrasonic

class CapteurUltrason():
    def __init__(self, capteurUltrasonModel):
        self.sensor = EV3Ultrasonic(capteurUltrasonModel.getPort())
        self.distance_detect = capteurUltrasonModel.getDistance()
    
    def distance(self):
        return self.sensor.distance()

    def detection(self):
        return self.distance()<=self.distance_detect