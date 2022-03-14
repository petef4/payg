import pytest

import flask_app


@pytest.fixture
def app():
    app = flask_app.app
    return app
