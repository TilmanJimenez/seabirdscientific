import abc
from typing import Self

import numpy


class AbstractSensor(abc.ABC):
    """An abstract general sensor."""

    name_short: str | None = None
    name_long: str | None = None
    length: int = 0

    # This is for converting to .cnv format replicating Seasoft v2
    significant_digits: int = 3

    @abc.abstractmethod
    def __init__(self, *args, index: int, **kwargs):
        self.set_name(index)

    def __str__(self) -> str:
        if self.name_short is None:
            return "Unnamed Sensor"
        return self.name_short

    def __repr__(self):
        return str(self)

    @abc.abstractmethod
    def set_name(self, index=0) -> None:
        self.name_short = f"AbsS{index}"
        self.name_long = f"Abstract Sensor {index}" if index else "Abstract Sensor"

    @classmethod
    def from_xmlcon(
        cls, xml, translation_dictionary: dict[str, str] | None = None, index: int = 0
    ) -> Self:
        """
        Reads the configuration values for the sensor from the corresponding XML fragment
        :param xml: A XML fragment with the contents of the corresponding `<Sensor>` tag
        :param translation_dictionary: A dictionary that describes how the XML maps to the sensor
        :param index: The index of the sensor. Sensors of the same time should have increasing indexes
        :return:
        """
        if translation_dictionary is None:
            translation_dictionary = {}
        kwargs: dict[str, float | int] = {}
        for child in xml.iter():
            tag = translation_dictionary.get(child.tag, child.tag)
            if not hasattr(cls, "__static_attributes__"):
                raise Warning(f"{cls} could not be read in, as it has no __static__attributes__")
            else:
                if tag in cls.__static_attributes__:  # type: ignore[attr-defined]
                    kwargs[tag] = float(child.text)
        return cls(index=index, **kwargs)

    @abc.abstractmethod
    def engineering_units_from_hex(self, data, *args, **kwargs) -> numpy.typing.ArrayLike:
        """
        Converts the data from hex to the engineering unit using the sensor's configuration.
        :param data: A `list` or `numpy.array` containing hexadecimal strings.
        :return:
        """
        pass

    @abc.abstractmethod
    def post_hex_processing(self, data, *args, **kwargs) -> numpy.typing.ArrayLike:
        """
        If any postprocessing should be done on this sensor, this is where it happens.
        :param data: A `list` or `numpy.array` containing hexadecimal strings.
        :return:
        """
        pass
