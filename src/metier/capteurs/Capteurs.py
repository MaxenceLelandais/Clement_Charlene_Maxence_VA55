class Capteurs:

    def __init__(self, capteurModel):
        self.capteurModel = capteurModel
        self.port = capteurModel.getPort()