from pybricks.parameters import Port


class PortEnum:
    A = Port.A
    B = Port.B
    C = Port.C
    D = Port.D
    S1 = Port.S1
    S2 = Port.S2
    S3 = Port.S3
    S4 = Port.S4

    _map = {
        "A": A,
        "B": B,
        "C": C,
        "D": D,
        "S1": S1,
        "S2": S2,
        "S3": S3,
        "S4": S4,
    }

    @staticmethod
    def from_str(name):
        """Convertit une string ('A', 'B', ...) en Port pybricks."""
        try:
            return PortEnum._map[name]
        except KeyError:
            raise ValueError("Port inconnu: {}".format(name))
