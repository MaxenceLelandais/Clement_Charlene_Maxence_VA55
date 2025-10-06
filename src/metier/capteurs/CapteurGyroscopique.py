from pybricks.ev3devices import GyroSensor


class CapteurGyroscopique:

    def __init__(self, port):
        self.sensor = GyroSensor(port)


    def speed(self):
        return self.sensor.speed()
    
    def angle(self):
        return self.sensor.angle()
    
    def reset_angle(self):
        return self.sensor.reset_angle()
    