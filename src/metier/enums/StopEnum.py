from pybricks.parameters import Stop


class StopEnum:
    COAST = Stop.COAST
    BRAKE = Stop.BRAKE
    HOLD = Stop.HOLD

    _map = {
        "COAST": COAST,
        "BRAKE": BRAKE,
        "HOLD": HOLD,
    }

    @staticmethod
    def from_str(name):
        try:
            return StopEnum._map[name]
        except KeyError:
            raise ValueError("Enum inconnu: {}".format(name))
