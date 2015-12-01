import pytest

import flaskapp


@pytest.fixture
def app():
    app = flaskapp.app
    return app
