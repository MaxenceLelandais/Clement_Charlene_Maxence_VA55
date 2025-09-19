from enum import Enum
from pybricks.parameters import Port


class PortEnum(Enum):
    A = Port.A
    B = Port.B
    C = Port.C
    D = Port.D
    S2 = Port.S2

    @staticmethod
    def from_str(name: str) -> Port:
        """Convertit une string ('A', 'B', ...) en Port pybricks."""
        try:
            return PortEnum[name].value
        except KeyError:
            raise ValueError(f"Port inconnu: {name}")
