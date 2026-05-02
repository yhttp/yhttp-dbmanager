import os

from bddcli import Given, Application as CLIApplication, status, stderr, \
    when, stdout
from yhttp.core import Application

from yhttp.ext.dbmanager import install


app = Application('0.1.0', 'foo')
app.settings |= '''
db:
  url: postgres://:@/foo
'''
install(app)


def test_applicationcli(cicd):
    cliapp = CLIApplication('example', f'{__name__}:app.climain')
    env = os.environ.copy()
    if cicd:
        env.setdefault('YHTTP_DB_DEFAULT_HOST', 'localhost')
        env.setdefault('YHTTP_DB_DEFAULT_ADMINUSER', 'postgres')
        env.setdefault('YHTTP_DB_DEFAULT_ADMINPASS', 'postgres')

    with Given(cliapp, 'db', environ=env):
        assert stderr == ''
        assert status == 0

        when('db drop')
        when('db create')
        assert stderr == ''
        assert status == 0

        when('db drop')
        assert status == 0
        assert stderr == ''

        when('db c')
        assert status == 0
        assert stderr == ''
        assert stdout == ''
