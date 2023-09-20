from yhttp import Application
from yhttp.ext.dbmanager import install

import pytest


app = Application()


def test_install():
    install(app)
    with pytest.raises(ValueError):
        app.ready()
