import os

import pytest
from pymlconf import Meld
from yhttp.ext.dbmanager import PostgresqlManager
from yhttp.dev.fixtures import freshdb

from yhttp.ext.dbmanager import Migrator


@pytest.fixture
def dbmanager(cicd):
    host = cicd and 'localhost' or None
    user = cicd and 'postgres' or None
    pass_ = cicd and 'postgres' or None
    return PostgresqlManager(
        host=os.environ.get('YHTTP_DB_DEFAULT_HOST', host),
        user=os.environ.get('YHTTP_DB_DEFAULT_ADMINUSER', user),
        password=os.environ.get('YHTTP_DB_DEFAULT_ADMINPASS', pass_),
    )


@pytest.fixture
def migrator(freshdb):
    m = Migrator(freshdb, Meld(Migrator.default_settings))
    yield m
    m.close()
