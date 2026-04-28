import os

from bddcli import Given, Application as CLIApplication, status, stderr, \
    when, stdout
import easycli
from yhttp.core import Application

from yhttp.ext.dbmanager import install


app = Application('0.1.0', 'foo')
app.settings.merge('''
db:
  url: postgres://:@/foo
''')
install(app)


def test_applicationcli(cicd):
    cliapp = CLIApplication('example', f'{__name__}:app.climain')
    env = os.environ.copy()
    if cicd:
        env.setdefault('YHTTP_DB_DEFAULT_HOST', 'localhost')
        env.setdefault('YHTTP_DB_DEFAULT_USER', 'postgres')
        env.setdefault('YHTTP_DB_DEFAULT_PASS', 'postgres')

    with Given(cliapp, 'db migration', environ=env):
        assert stderr == ''
        assert status == 0

        when('db migration new foo')
        assert stderr == ''
        assert status == 0
