"""Unit and time conversion"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_conversion.ipynb.

# %% auto 0
__all__ = ['AU_METER', 'LY_METER', 'PS_METER', 'dms_to_decimal', 'decimal_to_dms']

# %% ../nbs/01_conversion.ipynb 2
import math

# %% ../nbs/01_conversion.ipynb 3
AU_METER = 149597870700
LY_METER = 9.461E+15
PS_METER = 3.086E+16

# %% ../nbs/01_conversion.ipynb 4
def dms_to_decimal(degree, minute, second):
    """
    Conversion from DMS format (e.g. 15°42'9") to decimal format (e.g. 15.7025).
    """
    sign = -1 if degree < 0 else 1
    degree = abs(degree)
    minute += second / 60
    decimal = degree + (minute / 60)
    return round(decimal * sign, 4)

#| export
def decimal_to_dms(decimal):
    """
    Conversion from decimal format (e.g. 15.7025) to DMS format (e.g. 15°42'9").
    """
    sign = -1 if decimal < 0 else 1
    decimal = abs(decimal)
    degree = int(decimal)
    frac, _ = math.modf(decimal)
    frac *= 60
    minute = int(frac)
    frac, _ = math.modf(frac)
    second = 60 * frac
    return degree * sign, minute, round(second, 4)
