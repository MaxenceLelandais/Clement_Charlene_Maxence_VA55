from pybricks.ev3devices import Motor

class Moteur:

    def __init__(self, port,vitesse,stop_type):
        print("Creating motor on port:", port)
        self.moteur = Motor(port)
        self.stop_type = stop_type
        self.vitesse = vitesse
        
    def action(self,percentage):
        self.moteur.duty(percentage)

    def forward(self,speed):
        self.moteur.run(speed)

    def rotate(self,angle, aSpeed):
        self.moteur.run_target(aSpeed, angle)

    def stop(self):
        self.moteur.stop(self.stop_type)

    def getAngle(self):
        return self.moteur.angle()

    def resetAngle(self):
        return self.moteur.reset_angle()
    
    def status(self):
        return {
            self.nom:{
                "angle":self.getAngle()
                }
            }