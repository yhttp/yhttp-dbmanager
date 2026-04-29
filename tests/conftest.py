import os

import pytest
from pymlconf import MergableDict
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
    settings = MergableDict('migration: {}')
    settings.migration.merge(Migrator.default_settings)
    m = Migrator(freshdb, settings.migration)
    yield m
    m.close()
