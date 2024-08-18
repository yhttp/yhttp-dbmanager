import os

import pytest
from yhttp.dev.fixtures import cicd
from yhttp.ext.dbmanager import PostgresqlManager


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
