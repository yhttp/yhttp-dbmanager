import os

import pytest
from yhttp.ext.dbmanager import PostgresqlManager


CICD = 'CI' in os.environ \
    and os.environ['CI'] \
    and 'GITHUB_RUN_ID' in os.environ


@pytest.fixture
def cicd():
    return CICD


@pytest.fixture
def dbmanager(cicd):
    host = CICD and 'localhost' or None
    user = CICD and 'postgres' or None
    pass_ = CICD and 'postgres' or None
    return PostgresqlManager(
        host=os.environ.get('YHTTP_DB_DEFAULT_HOST', host),
        user=os.environ.get('YHTTP_DB_DEFAULT_ADMINUSER', user),
        password=os.environ.get('YHTTP_DB_DEFAULT_ADMINPASS', pass_),
    )
