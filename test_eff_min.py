TOL = 6  # tolerance, compare to this number of decimal places


def test__charge_per_call():
    assert round(20 - charge_per_call(1, 0, 20, 60), TOL) == 0
    assert round(20 - charge_per_call(60, 0, 20, 60), TOL) == 0
    assert round(40 - charge_per_call(90, 0, 20, 60), TOL) == 0
    assert round(40 - charge_per_call(120, 0, 20, 60), TOL) == 0
    assert round(60 - charge_per_call(121, 0, 20, 60), TOL) == 0

    assert round(2 - charge_per_call(1, 0, 20, 6), TOL) == 0
    assert round(2 - charge_per_call(6, 0, 20, 6), TOL) == 0
    assert round(4 - charge_per_call(7, 0, 20, 6), TOL) == 0
    assert round(4 - charge_per_call(12, 0, 20, 6), TOL) == 0

    assert round(10 - charge_per_call(1, 60, 0, 600, 10), TOL) == 0
    assert round(10 - charge_per_call(6, 60, 0, 600, 10), TOL) == 0
    assert round(10 - charge_per_call(7, 60, 0, 600, 10), TOL) == 0
    assert round(10 - charge_per_call(12, 60, 0, 600, 10), TOL) == 0


def test__mean_per_call():
    assert round(20 - mean_per_call(30, 60, 20, 60), TOL) == 0
    assert round(20 - mean_per_call(60, 60, 20, 60), TOL) == 0
    assert round(30 - mean_per_call(120, 60, 20, 60), TOL) == 0
    assert round(40 - mean_per_call(180, 60, 20, 60), TOL) == 0

    assert round(20 - mean_per_call(30, 60, 20, 1), TOL) == 0
    assert round(20 - mean_per_call(60, 60, 20, 1), TOL) == 0
    assert round(25 + 1. / 12 - mean_per_call(120, 60, 20, 1), TOL) == 0
    assert round(33 + 4. / 9 - mean_per_call(180, 60, 20, 1), TOL) == 0

    assert round(5 + 1. / 6 - mean_per_call(30, 1, 20, 1), TOL) == 0
    assert round(10 + 1. / 6 - mean_per_call(60, 1, 20, 1), TOL) == 0
    assert round(20 + 1. / 6 - mean_per_call(120, 1, 20, 1), TOL) == 0
    assert round(30 + 1. / 6 - mean_per_call(180, 1, 20, 1), TOL) == 0

    # these tests are not appropriate for real world parameters, the minimum
    # ought to be a multiple of charge_interval
    assert round(6 - mean_per_call(30, 1, 20, 6), TOL) == 0
    assert round(11 - mean_per_call(60, 1, 20, 6), TOL) == 0
    assert round(21 - mean_per_call(120, 1, 20, 6), TOL) == 0
    assert round(31 - mean_per_call(180, 1, 20, 6), TOL) == 0

    assert round(6 - mean_per_call(30, 6, 20, 6), TOL) == 0
    assert round(11 - mean_per_call(60, 6, 20, 6), TOL) == 0
    assert round(21 - mean_per_call(120, 6, 20, 6), TOL) == 0
    assert round(31 - mean_per_call(180, 6, 20, 6), TOL) == 0

    # again the minimum ought to be a multiple of charge_interval
    assert round(10 - mean_per_call(30, 60, 0, 600, 10), TOL) == 0
    assert round(10 - mean_per_call(60, 60, 0, 600, 10), TOL) == 0
    assert round(10 - mean_per_call(120, 60, 0, 600, 10), TOL) == 0
    assert round(10 - mean_per_call(180, 60, 0, 600, 10), TOL) == 0

    assert round(10 - mean_per_call(30, 0, 0, 600, 10), TOL) == 0
    assert round(10 - mean_per_call(60, 0, 0, 600, 10), TOL) == 0
    assert round(10 - mean_per_call(120, 0, 0, 600, 10), TOL) == 0
    assert round(10 - mean_per_call(180, 0, 0, 600, 10), TOL) == 0

    assert round(10 - mean_per_call(30, 600, 0, 600, 10), TOL) == 0
    assert round(10 - mean_per_call(60, 600, 0, 600, 10), TOL) == 0
    assert round(10 - mean_per_call(120, 600, 0, 600, 10), TOL) == 0
    assert round(10 - mean_per_call(180, 600, 0, 600, 10), TOL) == 0


MEAN_PER_CALL_DATA = (
    # (maximum, minimum, per_minute, charge_interval, connection=0)
    (30, 60, 20, 60), (60, 60, 20, 60),
    (120, 60, 20, 60), (180, 60, 20, 60),
    (30, 60, 20, 1), (60, 60, 20, 1),
    (120, 60, 20, 1), (180, 60, 20, 1),
    (30, 1, 20, 1), (60, 1, 20, 1),
    (120, 1, 20, 1), (180, 1, 20, 1),
    (30, 6, 20, 6), (60, 6, 20, 6),
    (120, 6, 20, 6), (180, 6, 20, 6),
    (30, 0, 0, 600, 10), (60, 0, 0, 600, 10),
    (120, 0, 0, 600, 10), (180, 0, 0, 600, 10),
    (30, 600, 0, 600, 10), (60, 600, 0, 600, 10),
    (120, 600, 0, 600, 10), (180, 600, 0, 600, 10))


def test__excel_mean_per_call():
    for args in MEAN_PER_CALL_DATA:
        assert round(excel_mean_per_call(*args) - mean_per_call(*args), TOL) == 0


def test__smart_mean_per_call():
    for args in MEAN_PER_CALL_DATA:
        assert round(smart_mean_per_call(*args) - mean_per_call(*args), TOL) == 0


def excel_mean_per_call(
        maximum, minimum, per_minute, charge_interval, connection=0):
    """Returns the mean charge for a call.

    Args:
        maximum (seconds): maximum length of call
        minimum (seconds): calls are effectively at least this long
        per_minute: charge for a call of one minute
        charge_interval (seconds): call length rounded up to a multiple of this
        connection: charge for connecting call
    """
    C5 = 60   # m  minimum length of call, seconds
    C6 = 20   # c  charge per minute, pence/min
    C7 = 1    # i  chargeable interval
    C8 = 0    # f  flat rate connection charge
    C9 = 180  # u  upper bound (length of call), seconds
    C9 = maximum
    C5 = minimum
    C6 = per_minute
    C7 = charge_interval
    C8 = connection
    C11 = int(C9 / C7)   # I  max number of intervals
    C12 = C9 - C11 * C7  # r  remaining seconds
    C14 = C5 / C7        # m/i
    C15 = C11 - C5 / C7  # I - m/i
    C17 = C5 * C6 / 60.0 + C8
    C19 = (C5 * (C5 * C6 / 60.0 + C8) + C12 * (C6 * C7 * (C11 + 1) / 60.0 + C8)) / C9
    # C23=((C7^2)*C6/60)*(C11*(C11+1)/2 - (C14)*(C14+1)/2)+C7*(C11 - C14)*C8
    C23 = ((C7**2) * C6 / 60.0) * (C11 * (C11 + 1) / 2.0 - (C14) * (C14 + 1) / 2.0) + C7 * (C11 - C14) * C8
    C21 = (C5 * (C5 * C6 / 60.0 + C8) + C12 * (C6 * C7 * (C11 + 1) / 60.0 + C8) + C23) / C9
    # F6=IF(C15<0,C17,IF(C15=0,C19,C21))
    if C15 < 0:     # I < m/i
        F6 = C17
    elif C15 == 0:  # I = m/i
        F6 = C19
    else:           # I > m/i
        F6 = C21
    return F6


def smart_mean_per_call(
        maximum, minimum, per_minute, charge_interval, connection=0):
    """Returns the mean charge for a call.

    Args:
        maximum (seconds): maximum length of call
        minimum (seconds): calls are effectively at least this long
        per_minute: charge for a call of one minute
        charge_interval (seconds): call length rounded up to a multiple of this
        connection: charge for connecting call
    """
    whole_intervals, last_seconds = divmod(maximum, charge_interval)
    first_intervals, inexact = divmod(minimum, charge_interval)
    if inexact != 0:
        raise ValueError('minimum must be a multiple of charge interval')
    middle_intervals = whole_intervals - first_intervals
    per_second = per_minute / 60.0
    if middle_intervals < 0:
        return per_second * minimum + connection
    else:
        return (
            per_second * (
                charge_interval**2 * (
                    middle_intervals * (middle_intervals + 1) / 2 +
                    first_intervals * middle_intervals) +
                charge_interval * (first_intervals +
                                   middle_intervals + 1) * last_seconds +
                minimum**2
            ) +
            connection * (charge_interval * middle_intervals + minimum +
                          last_seconds)
        ) / maximum


def mean_per_call(maximum, minimum, per_minute, charge_interval, connection=0):
    """Returns the mean charge for a call.

    Calculates call charges for calls ranging from 1 second up to maximum
    (inclusive) and then returns the mean.

    This is a reference implementation that explicitly calculates the charge
    for each call. It can be used to validate algorithms which use a smarter
    formula.

    Args:
        maximum (seconds): maximum length of call
        minimum (seconds): calls are effectively at least this long
        per_minute: charge for a call of one minute
        charge_interval (seconds): call length rounded up to a multiple of this
        connection: charge for connecting call
    """
    total = sum(charge_per_call(
        s, minimum, per_minute, charge_interval, connection)
                for s in range(1, maximum + 1))
    return total / maximum


def charge_per_call(
        seconds, minimum, per_minute, charge_interval, connection=0):
    """Returns the charge for a call.

    Args:
        seconds: length of call
        minimum (seconds): calls are effectively at least this long
        per_minute: charge for a call of one minute
        charge_interval (seconds): call length rounded up to a multiple of this
        connection: charge for connecting call
    """
    per_interval = charge_interval * per_minute / 60.0
    q, r = divmod(max(seconds, minimum), charge_interval)
    if r > 0:
        q += 1
    return q * per_interval + connection
