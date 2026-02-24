import numpy


def hex_to_volt(voltage_word: numpy.typing.ArrayLike) -> numpy.typing.ArrayLike:
    """
    Converts the hexadecimal value to a voltage, assuming the formula:
    V = 5 ( 1 - h / 4095 )
    :param voltage_word: A numpy array with integers between 0 and 4095
    :return: A numpy array containing voltages between 0V and 5V
    """
    voltages = numpy.bitwise_xor(voltage_word, 0xFFF)
    return numpy.divide(voltages, 819)


def hex_to_freq(frequency_word: numpy.typing.ArrayLike) -> numpy.typing.ArrayLike:
    """
    Converts the hexadecimal value to a frequency, assuming the formula:
    f = h / 256
    :param frequency_word: A numpy array with integers between 0 and 16777215
    :return: A numpy array containing frequencies between 0 Hz and 65536 Hz
    """
    frequency = numpy.divide(frequency_word, 256)
    return frequency
