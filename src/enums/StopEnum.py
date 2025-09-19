from enum import Enum
from pybricks.parameters import Stop


class StopEnum(Enum):
    COAST = Stop.COAST
    BRAKE = Stop.BRAKE
    HOLD = Stop.HOLD

    @staticmethod
    def from_str(name: str) -> Stop:
        """Convertit une string ('A', 'B', ...) en Stop pybricks."""
        try:
            return StopEnum[name].value
        except KeyError:
            raise ValueError(f"Enum inconnu: {name}")
