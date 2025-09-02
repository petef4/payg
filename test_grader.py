import grader as G

import pytest

# all decipence tests use f-strings to ensure they are int.

def test_pence():
    assert f"{G.decipence(5)}" == "50"
    assert f"{G.decipence('5.7p')}" == "57"
    assert f"{G.decipence(5.7)}" == "57"
    assert f"{G.decipence(5.67)}" == "57"
    assert f"{G.decipence(5.64)}" == "56"
    assert G.decipence(1.25) in (12, 13)
    assert f"{G.decipence('£1')}" == "1000"
    assert f"{G.decipence('£1.50')}" == "1500"
    assert f"{G.decipence('Free')}" == "0"
    assert f"{G.decipence('?')}" == "999"
    assert f"{G.decipence('n/a')}" == "999"
    with pytest.raises(ValueError) as excinfo:
        G.decipence('foo')
    assert str(excinfo.value) == 'String format not handled: foo'


def test_bill_per_score():
    assert f"{G.bill_per_score('sec')}" == "100"
    assert f"{G.bill_per_score('min')}" == "200"
    assert f"{G.bill_per_score('[min]')}" == "200"
    with pytest.raises(ValueError) as excinfo:
        G.bill_per_score('foo')
    assert str(excinfo.value) == 'String format not handled: foo'


def test_voicemail_score():
    assert f"{G.voicemail_score('Free')}" == "0"
    assert f"{G.voicemail_score(15)}" == "150"
    assert f"{G.voicemail_score('15p')}" == "150"
    assert f"{G.voicemail_score('8p / call')}" == "80"
    with pytest.raises(ValueError) as excinfo:
        G.voicemail_score('foo')
    assert str(excinfo.value) == 'String format not handled: foo'


def test_yes_no_score():
    assert f"{G.yes_no_score('Yes')}" == "100"
    assert f"{G.yes_no_score('Soon')}" == "150"
    assert f"{G.yes_no_score('No')}" == "200"
    assert f"{G.yes_no_score('[No]')}" == "200"
    with pytest.raises(ValueError) as excinfo:
        G.yes_no_score('foo')
    assert str(excinfo.value) == 'String format not handled: foo'


def test_dip_per_MB():
    assert f"{G.dip_per_MB(10, '2p / MB')}" == "200"
    assert f"{G.dip_per_MB(10, '2.5p / MB')}" == "250"
    assert f"{G.dip_per_MB(1, '2p / MB')}" == "20"
    assert f"{G.dip_per_MB(1, '2.5p / MB')}" == "25"
    assert f"{G.dip_per_MB(0, '2p / MB')}" == "0"
    assert f"{G.dip_per_MB(0, '2.5p / MB')}" == "0"
    for other in ('25p / day',
                  '£2 / day for 50 MB then 10p / MB',
                  '1 MB / day free then 19p / MB',
                  # '£3 / MB capped at £1 / day',
                  'Add-ons start from £1 / 100 MB'):
        assert G.dip_per_MB(10, other) is None


def test_dip_per_nMB():
    assert f"{G.dip_per_nMB(10, '20p / 5MB')}" == "400"
    assert f"{G.dip_per_nMB(1, '2p / 5MB')}" == "4"
    assert f"{G.dip_per_nMB(0, '20p / 5MB')}" == "0"
    assert f"{G.dip_per_nMB(0, '2p / 5MB')}" == "0"


def test_dip_per_day():
    assert f"{G.dip_per_day(10, '25p / day for 25 MB then 10p / MB')}" == "250"
    assert f"{G.dip_per_day(10, '£2 / day for 50 MB then 10p / MB')}" == "2000"
    assert f"{G.dip_per_day(10, '£1 / day for 100 MB then £1 / 100 MB')}" == "1000"
    assert f"{G.dip_per_day(1, '25p / day for 25 MB then 10p / MB')}" == "250"
    assert f"{G.dip_per_day(1, '£2 / day for 50 MB then 10p / MB')}" == "2000"
    assert f"{G.dip_per_day(1, '£1 / day for 100 MB then £1 / 100 MB')}" == "1000"
    assert f"{G.dip_per_day(0, '25p / day for 25 MB then 10p / MB')}" == "0"
    assert f"{G.dip_per_day(0, '£2 / day for 50 MB then 10p / MB')}" == "0"
    assert f"{G.dip_per_day(0, '£1 / day for 100 MB then £1 / 100 MB')}" == "0"
    assert f"{G.dip_per_day(30, '25p / day for 25 MB then 10p / MB')}" == "750"
    assert f"{G.dip_per_day(60, '£2 / day for 50 MB then 10p / MB')}" == "3000"
    assert f"{G.dip_per_day(120, '£1 / day for 100 MB then £1 / 100 MB')}" == "2000"
    assert f"{G.dip_per_day(220, '£1 / day for 100 MB then £1 / 100 MB')}" == "3000"
    assert f"{G.dip_per_day(50, '£2 / day includes 50 MB then £1 / 50 MB')}" == "2000"
    for other in ('2p / MB', '2.5p / MB',
                  '1 MB / day free then 19p / MB',
                  '£3 / MB capped at £1 / day',
                  'Add-ons start from £1 / 100 MB'):
        assert G.dip_per_day(10, other) is None


def test_dip_per_MB_some_free_per_day():
    assert f"{G.dip_per_MB_some_free_per_day(10, '1 MB / day free then 19p / MB')}" == "1710"
    assert f"{G.dip_per_MB_some_free_per_day(0, '1 MB / day free then 19p / MB')}" == "0"
    assert f"{G.dip_per_MB_some_free_per_day(1, '1 MB / day free then 19p / MB')}" == "0"
    for other in ('2p / MB', '2.5p / MB', '25p / day',
                  '£2 / day for 50 MB then 10p / MB',
                  '£3 / MB capped at £1 / day',
                  'Add-ons start from £1 / 100 MB'):
        assert G.dip_per_MB_some_free_per_day(10, other) is None


def test_dip_per_MB_some_free_per_month():
    assert f"{G.dip_per_MB_some_free_per_month(10, '200 MB / month free then 1p / MB')}" == "33"
    assert f"{G.dip_per_MB_some_free_per_month(0, '200 MB / month free then 1p / MB')}" == "0"
    assert f"{G.dip_per_MB_some_free_per_month(1, '200 MB / month free then 1p / MB')}" == "0"
    for other in ('2p / MB', '2.5p / MB', '25p / day',
                  '£2 / day for 50 MB then 10p / MB',
                  '£3 / MB capped at £1 / day',
                  'Add-ons start from £1 / 100 MB'):
        assert G.dip_per_MB_some_free_per_month(10, other) is None


def test_dip_per_MB_capped():
    assert f"{G.dip_per_MB_capped(10, '£3 / MB capped at £1 / day')}" == "1000"
    assert f"{G.dip_per_MB_capped(0, '£3 / MB capped at £1 / day')}" == "0"
    assert f"{G.dip_per_MB_capped(1, '£3 / MB capped at £1 / day')}" == "1000"
    for other in ('2p / MB', '2.5p / MB', '25p / day',
                  '£2 / day for 50 MB then 10p / MB',
                  'Add-ons start from £1 / 100 MB'):
        assert G.dip_per_MB_capped(10, other) is None


def test_dip_addons_only():
    assert f"{G.dip_addons_only(10, 'Add-ons start from £1 / 100 MB')}" == "100"
    assert f"{G.dip_addons_only(1, 'Add-ons start from £1 / 100 MB')}" == "10"
    assert f"{G.dip_addons_only(0, 'Add-ons start from £1 / 100 MB')}" == "0"
    assert G.dip_addons_only(10, 'Add-ons start from £10 / 8 GB') in (12, 13)
    assert f"{G.dip_addons_only(10, 'Add-ons start from £3 / 1.5 GB')}" == "20"
    assert f"{G.dip_addons_only(10, 'Bundles start from £1 / 100 MB')}" == "100"
    for other in ('2p / MB', '2.5p / MB', '25p / day',
                  '£2 / day for 50 MB then 10p / MB',
                  '1 MB / day free then 19p / MB',
                  '£3 / MB capped at £1 / day'):
        assert G.dip_addons_only(10, other) is None


def test_data_score():
    assert f"{G.data_score(10, '2p / MB')}" == "200"
    assert f"{G.data_score(10, '2.5p / MB')}" == "250"
    assert f"{G.data_score(10, '25p / day for 25 MB then 10p / MB')}" == "250"
    assert f"{G.data_score(10, '£2 / day for 50 MB then 10p / MB')}" == "2000"
    assert f"{G.data_score(10, '£1 / day for 100 MB then £1 / 100 MB')}" == "1000"
    assert f"{G.data_score(10, '1 MB / day free then 19p / MB')}" == "1710"
    assert f"{G.data_score(10, '£3 / MB capped at £1 / day')}" == "1000"
    assert f"{G.data_score(10, 'Add-ons start from £1 / 100 MB')}" == "100"
    with pytest.raises(ValueError) as excinfo:
        G.data_score(10, 'foo')
    assert str(excinfo.value) == 'String format not handled: foo'
