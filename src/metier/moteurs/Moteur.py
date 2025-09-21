from pybricks.ev3devices import Motor

class Moteur:

    def __init__(self, moteurModel):
        self.moteurModel = moteurModel
        self.moteur = Motor(moteurModel.getPort())
        
    def action(self,percentage):
        self.moteur.duty(percentage)

    def forward(self,speed):
        self.moteur.run(speed)

    def rotate(self,angle, aSpeed):
        self.moteur.run_target(aSpeed, angle)

    def stop(self):
        self.moteur.stop(self.moteurModel.getStop())

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