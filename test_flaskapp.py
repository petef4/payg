from flask import url_for


def test_home(client):
    assert client.get(url_for('home')).status_code == 200


def test_payg(client):
    assert client.get(url_for('payg')).status_code == 200


def test_links(client):
    assert client.get(url_for('links')).status_code == 200


def test_shopping(client):
    assert client.get(url_for('shopping')).status_code == 200


def test_times(client):
    assert client.get(url_for('times')).status_code == 200


def test_test(client):
    assert client.get(url_for('test')).status_code == 200
