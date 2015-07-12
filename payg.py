#!/usr/bin/env python
from bs4 import BeautifulSoup

# The following shell command was run to generate the input files:
# for n in {1..85}; do hg cat -r $n -o "%s.~$n~" payg.html

def get_operator(rev):
    filename = 'payg.html.~{}~'.format(rev) if rev else 'payg.html'
    with open(filename) as f:
        soup = BeautifulSoup(f)
    td_op = [r.td for r in soup.html.body.table.tbody.find_all('tr') if r.td]
    i, td_compact = 0, []
    while i < len(td_op):
        td_compact.append(td_op[i])
        i += int(td_op[i].get('rowspan', '1'))
    return set(d.a.text for d in td_compact if d.a)

