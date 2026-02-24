import numpy

from seabirdscientific.sensors.abstract_sensor import AbstractSensor
from seabirdscientific.sensors.utils import hex_to_freq


class TemperatureSensor(AbstractSensor):
    def __init__(
        self,
        *args,
        F0: float,
        A: float,
        B: float,
        C: float,
        D: float,
        G: float,
        H: float,
        I: float,
        J: float,
        slope: float = 1,
        offset: float = 0,
        index: int = 0,
        **kwargs,
    ):
        super().__init__(*args, index=index, **kwargs)
        self.length = 6
        self.significant_digits = 4
        self.F0 = F0
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.G = G
        self.H = H
        self.I = I
        self.J = J
        self.slope = slope
        self.offset = offset

    def set_name(self, index=0):
        self.name_short = f"t{index}90C"
        self.name_long = (
            f"Temperature, {index} [ITS-90, deg C]"
            if index != 0
            else "Temperature [ITS-90, deg C]"
        )

    def engineering_units_from_hex(self, data, *args, **kwargs):
        log = numpy.log(self.F0 / hex_to_freq(data))
        return 1.0 / (self.G + log * (self.H + log * (self.I + log * self.J))) - 273.15

    def post_hex_processing(self, data, *args, **kwargs) -> numpy.typing.ArrayLike:
        return data
