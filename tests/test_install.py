import pytest
from yhttp.core import Application

from yhttp.ext.dbmanager import install


app = Application()


def test_install():
    install(app)
    with pytest.raises(ValueError):
        app.ready()
