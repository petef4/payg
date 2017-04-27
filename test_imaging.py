import imaging


def test_load():
    img = imaging.Imaging()
    assert img.logo[0] == '1pmobile_16.png'
    assert img.logo[1] == '3_16.png'
    assert img.logo[2] == 'aether_16.png'
    assert img.logo[-1] == 'white_16.png'


def test_add_logo_pos():
    data = [
        {'operator': '1pMobile', 'operator.logo': '1pmobile_16.png'},
        {'operator': '3', 'operator.logo': '3_16.png'}]
    img = imaging.Imaging()
    img.add_logo_pos(data)
    assert data[0]['operator.logo_pos'] == -4
    assert data[1]['operator.logo_pos'] == -28
