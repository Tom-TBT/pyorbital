"""Unit and time conversion"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_conversion.ipynb.

# %% auto 0
__all__ = ['ASTRO_UNIT', 'LIGHT_YEAR', 'PARSEC', 'SOLAR_DAY', 'SIDERAL_DAY', 'TROPICAL_YEAR', 'SIDERAL_YEAR', 'ANOMALISTIC_YEAR',
           'DRACONIC_YEAR', 'JULIAN_YEAR', 'GALACTIC_YEAR', 'timezone_d', 'dms_to_decimal', 'decimal_to_dms',
           'is_leap_year', 'is_gregorian', 'date_to_julian', 'julian_to_date', 'day_into_year', 'day_into_year_to_date',
           'day_of_week', 'lct_to_ut', 'ut_to_lct', 'gst_to_lst', 'lst_to_gst']

# %% ../nbs/01_conversion.ipynb 2
import math

# %% ../nbs/01_conversion.ipynb 3
ASTRO_UNIT = 149597870700  # Astronomical unit in meter
LIGHT_YEAR = 9.461E+15     # Light-year in meter
PARSEC = 3.086E+16     # Parsec in meter

SOLAR_DAY = 24 # Interval of time for the sun to come back to the meridian. This is an average.
SIDERAL_DAY = 23.9333  # Time for a star to return at the same position
TROPICAL_YEAR = 365.2422  # Time between two vernal equinox (sun crossing equator)
SIDERAL_YEAR = 365.2564  # Star used as reference point 
ANOMALISTIC_YEAR = 365.2596  # Point of when the earth is closest to the sun
DRACONIC_YEAR = 346.6201 # Combined sun and moon motion. To predict eclipses.
JULIAN_YEAR = 365.25  # Average year lenght in Julian calendar 
GALACTIC_YEAR = 2.25E8 * SIDERAL_YEAR  # In days

# %% ../nbs/01_conversion.ipynb 4
def dms_to_decimal(degree, minute, second, sign):
    """
    Conversion from DMS format (e.g. 15°42'9") to decimal format (e.g. 15.7025).
    """
    assert (sign == 1 or sign == -1)
    degree = abs(degree)
    minute += second / 60
    decimal = degree + (minute / 60)
    return decimal * sign

def decimal_to_dms(decimal):
    """
    Conversion from decimal format (e.g. 15.7025) to DMS format (e.g. 15°42'9").
    """
    sign = -1 if decimal < 0 else 1
    decimal = abs(decimal)
    degree = int(decimal)
    frac = math.modf(decimal)[0]
    frac *= 60
    minute = int(frac)
    frac = math.modf(frac)[0]
    second = 60 * frac
    return degree, minute, second, sign

# %% ../nbs/01_conversion.ipynb 6
def is_leap_year(year):
    return (year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0))

def is_gregorian(year, month, day):
    return (year > 1582) or (year == 1582 and ((month > 10) or (month == 10 and day > 14)))

# %% ../nbs/01_conversion.ipynb 8
def date_to_julian(year, month, day):
    """
    Conversion from Calendar date to Julian day (note that the day can be expressed in decimal with `dms_to_decimal`)).
    """
    assert 1 <= month <= 12
    if month <= 2:
        year -= 1
        month += 12
    t = 0.75 if year < 0 else 0
    
    a, b = 0, 0
    if is_gregorian(year, month, day):
        a = int(year/100)
        b = 2 - a + int(a/4)
        
    return b + int(365.25 * year - t) + int(30.6001 * (month + 1)) + day + 1720994.5

def julian_to_date(julian_day):
    """
    Conversion from Julian day to Calendar date.
    """
    julian_day += 0.5
    i = int(julian_day)
    f = math.modf(julian_day)[0]
    b = i
    if i > 2299160:
        a = int((i - 1867216.25)/36524.25)
        b = i + 1 + a - int(a/4)
    c = b + 1524
    d = int((c - 122.1)/365.25)
    e = int(365.25 * d)
    g = int((c - e)/30.6001)
    
    day = c - e + f - int(30.6001 * g)
    month = g - 1 if g < 13.5 else g - 13
    year = d - 4716 if month > 2.5 else d - 4715
    return year, month, day

# %% ../nbs/01_conversion.ipynb 10
def day_into_year(year, month, day):
    t = 1 if is_leap_year(year) else 2
    return int(275 * month / 9) - (t * int((month + 9) / 12)) + day - 30

def day_into_year_to_date(year, days):
    a = 1523 if is_leap_year(year) else 1889
    b = int((days + a - 122.1) / 365.25)
    c = days + a - int(b * 365.25)
    e = int(c / 30.6001)
    month = e - 1 if e < 13.5 else e - 13
    day = c - int(e * 30.6001)
    return year, month, day   

# %% ../nbs/01_conversion.ipynb 12
def day_of_week(year, month, day):
    """
    Gives back which day was the given date. 0: sunday, 1: monday, ...
    """
    day = int(day)
    jd = date_to_julian(year, month, day)
    a = (jd + 1.5) / 7
    b = 7 * math.modf(a)[0]
    return round(b)

# %% ../nbs/01_conversion.ipynb 14
timezone_d = {
    "cet": 1,
    "est": -5,
    "cst": -6,
    "mst": -7,
    "pst": -8
}
def lct_to_ut(hour, minute, second, timezone, daylight_saving_time=False):
    """
    Local civil time to universal time
    """
    dec = dms_to_decimal(hour, minute, second, 1)
    if daylight_saving_time:
        dec -= 1
    dec -= timezone_d[timezone]
    return decimal_to_dms((dec + 24) % 24)

def ut_to_lct(hour, minute, second, timezone, daylight_saving_time=False):
    """
    Universal time to local civil time
    """
    dec = dms_to_decimal(hour, minute, second, 1)
    dec += timezone_d[timezone]
    dec = (dec + 24) % 24
    if daylight_saving_time:
        dec += 1
    return decimal_to_dms((dec + 24) % 24)

# %% ../nbs/01_conversion.ipynb 16
def ut_to_lct(year, month, day, hour, minute, second):
    """
    Universal time to Greenwitch standard time
    """
    jd = date_to_julian(year, month, day)
    jd0 = date_to_julian(year, 1, 0)
    days = jd - jd0
    t = (jd0 - 2415020) / 36525
    r = 6.6460656 + 2400.051262 * t + 0.00002581 ** t 
    b = 24 - r + 24 * (year - 1900)
    t0 = 0.0657098 * days - b
    ut = dms_to_decimal(hour, minute, second, 1)
    gst = t0 + 1.002738 * ut
    return decimal_to_dms((gst + 24) % 24)

def lct_to_ut(year, month, day, hour, minute, second):
    """
    Greenwitch standard time to universal time.
    """
    jd = date_to_julian(year, month, day)
    jd0 = date_to_julian(year, 1, 0)
    days = jd - jd0
    t = (jd0 - 2415020) / 36525
    r = 6.6460656 + 2400.051262 * t + 0.00002581 ** t 
    b = 24 - r + 24 * (year - 1900)
    t0 = 0.0657098 * days - b
    t0 = (t0 + 24) % 24
    gst = dms_to_decimal(hour, minute, second, 1)
    a = gst - t0
    a = (a + 24) % 24
    ut = 0.99727 * a
    return decimal_to_dms((ut + 24) % 24)

# %% ../nbs/01_conversion.ipynb 18
def gst_to_lst(hour, minute, second, longitude):
    """
    longitude: 40E is +40, 40W is -40
    """
    gst = dms_to_decimal(hour, minute, second, 1)
    lst = gst + (longitude / 15)
    return decimal_to_dms((lst + 24) % 24)

def lst_to_gst(hour, minute, second, longitude):
    """
    longitude: 40E is +40, 40W is -40
    """
    lst = dms_to_decimal(hour, minute, second, 1)
    gst = lst - (longitude / 15)
    return decimal_to_dms((gst + 24) % 24)
