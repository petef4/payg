import re


class Grader:
    def __init__(self, grading):
        self.grading = grading

    def grade(self, data):
        """Amend data with scores, keys (for sorting columns) and grades.

        Scores are determined for most columns. Sort keys start with the column
        score but then may draw on other columns so that secondary sorting
        works. Sort keys are effectively alphabetic when scoring does not
        apply.
        """
        operator_scores = dict(
            (name, index) for (index, name) in enumerate(
                sorted(set(r['operator'] for r in data))))
        plan_scores = dict(
            (name, index) for (index, name) in enumerate(
                sorted(set(r['plan'] for r in data))))
        network_scores = dict(
            (name, index) for (index, name) in enumerate(
                sorted(set(r['network'] for r in data))))
        MB_per_day = self.grading['data']['MB / day']
        for row in data:
            operator = operator_scores[row['operator']]
            plan = plan_scores[row['plan']]
            row['operator.key'] = 100 * operator + plan
            row['plan.key'] = 100 * plan + operator
            row['min_same.score'] = same = decipence(row['min_same'])
            row['min_other.score'] = other = decipence(row['min_other'])
            row['min_land.score'] = land = decipence(row['min_land'])
            row['min_same.key'] = 1000000 * same + 1000 * other + land
            row['min_other.key'] = 1000000 * other + 1000 * land + same
            row['min_land.key'] = 1000000 * land + 1000 * other + same
            row['charge_min.key'] = row['charge_min.score'] = (
                max((same, other, land))
                if row['charge_min'] == '[1 min]'
                else decipence(row['charge_min']))
            row['bill_per.key'] = row['bill_per.score'] = bill_per_score(
                row['bill_per'])
            row['sms_same.score'] = same = decipence(row['sms_same'])
            row['sms_other.score'] = other = decipence(row['sms_other'])
            row['sms_same.key'] = 1000 * same + other
            row['sms_other.key'] = 1000 * other + same
            row['voicemail.key'] = row['voicemail.score'] = voicemail_score(
                row['voicemail'])
            row['08x.key'] = row['08x.score'] = decipence(row['08x'])
            row['mms.key'] = row['mms.score'] = decipence(row['mms'])
            row['4G.key'] = row['4G.score'] = yes_no_score(row['4G'])
            row['tether.key'] = row['tether.score'] = yes_no_score(
                row['tether'])
            row['data.key'] = row['data.score'] = data_score(MB_per_day,
                                                             row['data'])
            network = network_scores[row['network']]
            row['network.key'] = 10000 * network + 100 * operator + plan
            row['checked.key'] = (
                10000 * int(row['checked'].replace('-', '')) + 100 * operator +
                plan)
            grades = {}
            for col_score, score in row.items():
                if not col_score.endswith('.score'):
                    continue
                col = col_score[:-6]
                if row[col] in ('?', 'n/a') or (
                        col == 'data' and (row[col].startswith('Add-ons') or
                                           row[col].startswith('Bundles'))):
                    grades[col + '.grade'] = 'na'
                else:
                    for g in self.grading:
                        if col.startswith(g):
                            break
                    else:
                        g = None
                    if g:
                        for grade in ['good', 'okay', 'poor']:
                            if score <= self.grading[g][grade]:
                                grades[col + '.grade'] = grade
                                break
                        else:
                            grades[col + '.grade'] = 'bad'
            row.update(grades)


def decipence(pence):
    """Convert pence or pounds into decipence, taking note of special values.

    Decipence are ints.
    """
    if isinstance(pence, str):
        if pence.endswith('p'):
            pence = float(pence[:-1])
        elif pence.startswith('£'):
            pence = float(pence[1:]) * 100
        elif pence == 'Free':
            pence = 0
        elif pence in ('?', 'n/a'):
            pence = 99.9
        else:
            raise ValueError('String format not handled: ' + pence)
    return int(pence * 10 + 0.5)


def bill_per_score(bill_per):
    if bill_per == 'sec':
        return 100
    elif bill_per in ('min', '[min]'):
        return 200
    else:
        raise ValueError('String format not handled: ' + bill_per)


def voicemail_score(voicemail):
    try:
        pence = voicemail.split('/')[0].rstrip()  # discard ' / per call'
    except AttributeError:  # voicemail is an int
        pence = voicemail
    return decipence(pence)

YES_NO = {
    'Yes': 100,
    'Soon': 150,
    'No': 200,
    '[No]': 200,
    'n/a': None,
    '?': None}


def yes_no_score(yes_no):
    try:
        return YES_NO[yes_no]
    except KeyError:
        raise ValueError('String format not handled: ' + yes_no)

_FLT = r'\d+\.?\d*'
FLOAT = '(' + _FLT + ')'
MONEY = '(' + _FLT + 'p|£' + _FLT + ')'
DAY_PER_MONTH = 30  # month tends to be shorthand for 30 days, not calendar
N_MB = '(' + _FLT + ')MB'

def dip_per_MB(MB_per_day, data):
    match = re.match(MONEY + ' / MB', data)
    if match:
        return MB_per_day * decipence(match.group(1))
    return None


def dip_per_nMB(MB_per_day, data):
    match = re.match(MONEY + ' / ' + N_MB, data)
    if match:
        return MB_per_day * decipence(match.group(1)) / float(match.group(2))
    return None


def dip_per_day(MB_per_day, data):
    match = re.match(
        MONEY + ' / day for ' + FLOAT + ' MB then ' + MONEY + ' / MB',
        data)
    if match:
        chunk = 1
    else:
        match = re.match(
            MONEY + ' / day for ' + FLOAT + ' MB then ' + MONEY + ' / ' +
            FLOAT + ' MB',
            data)
        if match:
            chunk = float(match.group(4))
        else:
            return None
    price = decipence(match.group(1))
    allowance = float(match.group(2))
    if MB_per_day == 0:
        return 0
    elif MB_per_day <= allowance:
        return price
    extra, part = divmod(MB_per_day - allowance, chunk)
    if part > 0:
        extra += 1
    return price + extra * decipence(match.group(3))


def dip_per_MB_some_free_per_day(MB_per_day, data):
    match = re.match(FLOAT + ' MB / day free then ' + MONEY + ' / MB', data)
    if not match:
        return None
    free = float(match.group(1))
    if MB_per_day < free:
        return 0
    return (MB_per_day - free) * decipence(match.group(2))


def dip_per_MB_some_free_per_month(MB_per_day, data):
    match = re.match(FLOAT + ' MB / month free then ' + MONEY + ' / MB', data)
    if not match:
        return None
    free = float(match.group(1)) / DAY_PER_MONTH
    if MB_per_day < free:
        return 0
    return (MB_per_day - free) * decipence(match.group(2))


def dip_per_MB_capped(MB_per_day, data):
    match = re.match(MONEY + ' / MB capped at ' + MONEY + ' / day', data)
    if not match:
        return None
    price = MB_per_day * decipence(match.group(1))
    return min(price, decipence(match.group(2)))


def dip_addons_only(MB_per_day, data):
    match = re.match(
        '(?:Add-on|Bundle)s start from ' + MONEY + ' / ' + FLOAT + ' MB', data)
    if match:
        if MB_per_day == 0:
            return 0
        else:
            return decipence(match.group(1))
    return None

data_scorers = [
    dip_per_MB_some_free_per_day,
    dip_per_MB_some_free_per_month,
    dip_per_MB_capped,
    dip_per_MB,  # must come later than dip_per_MB_capped
    dip_per_nMB,
    dip_per_day,
    dip_addons_only]


def data_score(MB_per_day, data):
    for fn in data_scorers:
        score = fn(MB_per_day, data)
        if score is not None:
            return score
    raise ValueError('String format not handled: ' + data)
