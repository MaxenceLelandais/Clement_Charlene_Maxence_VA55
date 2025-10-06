from pybricks.ev3devices import UltrasonicSensor

class CapteurUltrason():
    def __init__(self, port, distanceDetection):
        self.sensor = UltrasonicSensor(port)
        self.distance_detect = distanceDetection
    
    def distance(self):
        return self.sensor.distance()

    def detection(self):
        return self.distance()<=self.distance_detect