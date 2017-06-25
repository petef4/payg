from json import load
import os

from grader import Grader

with open('payg.json', encoding='UTF-8') as f:
    data = load(f)

with open('grading.json', encoding='UTF-8') as f:
    grading = load(f)
grader = Grader(grading)
grader.grade(data)

preamble = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head profile="http://gmpg.org/xfn/11">
    <title>Compare PAYG mobile networks - Mobile Network Comparison</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <style>
        table {
            border-collapse: collapse;
        }
        tr, td, th {
            border: 0.1em solid black;
        }
    </style>
</head>
<body>
'''
postamble = '''</body>
</html>
'''


class MncData:
    def __init__(self, pathname=None):
        if pathname is None:
            pathname = os.path.expanduser(
                '~/Downloads/PAYG/MNC/text-replace 003.txt')
        self.primary(pathname)
        self.secondary()

    def primary(self, pathname):
        """Parse pathname contents to populate primary attributes: plans, all.
        """
        self.plans = []
        self.all = {}
        with open(pathname) as f:
            for line in f.readlines():
                kv = line.rstrip().split(' => ')
                if len(kv) == 2:
                    key, value = kv
                    if not (key.startswith(':') and key.endswith(':')):
                        raise ValueError('cannot parse {}', line.rstrip())
                    self.all[key] = value
                    if key.endswith('calls:') and key != ':calls:':
                        self.plans.append(key[1:-6])

    def secondary(self):
        """Populate secondary attributes: calls, texts, sims, coverage, other.
        """
        self.call = {}
        self.text = {}
        self.review = {}
        self.sim = {}
        self.coverage = {}
        self.other = {}
        for key, value in self.all.items():
            if key.endswith('calls:') and key != ':calls:':
                self.call[key[1:-6]] = value
            elif key.endswith('texts:') and key != ':texts:':
                self.text[key[1:-6]] = value
            elif key[1:-1] in self.plans:
                self.review[key[1:-1]] = value
            elif key.endswith('sim:') and key != ':sim:':
                self.sim[key[1:-4]] = value
            elif key.endswith('coverages:') and key != ':coverage:':
                self.call[key[1:-6]] = value
            else:
                self.other[key[1:-1]] = value

    def populate(self, table_in=None, table_out=None):
        """Substitute :references: and ((comments))."""
        if table_in is None:
            table_in = os.path.expanduser(
                '~/Downloads/PAYG/MNC/comparison table 002.html')
        if table_out is None:
            table_out = os.path.expanduser(
                '~/Downloads/PAYG/MNC/comparison table filled.html')
        with open(table_in, 'r') as i, open(table_out, 'w') as o:
            o.write(preamble)
            for line in i.readlines():
                for k, v in self.all.items():
                    line = line.replace(k, v)
                if line.count(':') > 1:
                    raise ValueError('unresolved reference in {}'.format(line))
                o.write(line)
            o.write(postamble)


class Map:
    def __init__(self, pathname=None):
        if pathname is None:
            pathname = os.path.expanduser('~/Downloads/PAYG/MNC/map.json')
        with open(pathname, encoding='UTF-8') as f:
            self.mnc2payg = load(f)
        self.payg_index = {}
        for i, entry in enumerate(data):
            self.payg_index[(entry['operator'], entry['plan'])] = i
        self.active_mnc2payg = {}
        self.defunct = []
        for k, v in self.mnc2payg.items():
            if v is None:
                self.defunct.append(k)
            else:
                self.active_mnc2payg[k] = self.payg_index[tuple(v)]
