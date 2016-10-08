from numbers import Number


def add_effective_per_min(data, maximum_call):
    """Update data to add eff_min elements.

    data is modified.
    """
    #if True: return
    for row in data:
        per_minute = max_minute(row)
        charge_min = per_minute if row['charge_min'] == '[1 min]' else pence(
            row['charge_min'])
        minimum = charge_min / per_minute
        row['eff_min'] = smart_mean_per_minute(
            maximum_call, minimum, per_minute, charge_interval(row['bill_per']))


def max_minute(row):
    """Return the largest of the per minute charges as pence (float).
    """
    max = 0.0
    valid = False
    for m in ('same', 'other', 'land'):
        p = pence(row['min_' + m])
        if isinstance(p, Number) and p >= max:
            max = p
            valid = True
    if not valid:
        raise ValueError('Per minute charges not found')
    return max


def pence(charge):
    if not isinstance(charge, str):
        return charge
    elif charge.endswith('p'):
        return float(charge[:-1])
    elif charge.startswith('£'):
        return float(charge[1:]) * 100
    elif charge == 'Free':
        return 0
    elif charge in ('?', 'n/a'):
        return charge
    else:
        raise ValueError('String format not handled: ' + charge)


def charge_interval(bill_per):
    if bill_per == 'sec':
        return 1
    elif bill_per in ('min', '[min]'):
        return 60
    else:
        raise ValueError('String format not handled: ' + bill_per)


def smart_mean_per_minute(
        maximum, minimum, per_minute, charge_interval, connection=0):
    """Returns the mean charge for a minute.

    Args:
        maximum (seconds): maximum length of call to average (the minimum is 1)
        minimum (seconds): calls are effectively at least this long
        per_minute: charge for a call of one minute
        charge_interval (seconds): call length rounded up to a multiple of this
        connection: charge for connecting call
    """
    whole_intervals, last_seconds = divmod(maximum, charge_interval)
    first_intervals, inexact = divmod(minimum, charge_interval)
    if inexact != 0:
        pass #raise ValueError('minimum must be a multiple of charge interval')
    middle_intervals = whole_intervals - first_intervals
    per_second = per_minute / 60.0
    if middle_intervals < 0:
        return (per_second * minimum + connection) * 60.0 / maximum
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
        ) * 60.0 / maximum**2
