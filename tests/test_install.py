import pytest
from yhttp.core import Application

from yhttp.ext.dbmanager import install


app = Application('0.1.0', 'foo')


def test_install():
    install(app)
    with pytest.raises(ValueError):
        app.ready()
