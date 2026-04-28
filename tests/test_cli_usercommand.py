from bddcli import Given, Application as CLIApplication, status, stderr, \
    stdout
import easycli
from yhttp.core import Application

from yhttp.ext.dbmanager import install


class Bar(easycli.SubCommand):
    __command__ = 'bar'

    def __call__(self, args):
        print('bar')


app = Application('0.1.0', 'foo')
app.settings.merge('''
db:
  url: postgres://:@/foo
''')
install(app, cliarguments=[Bar])


def test_applicationcli():
    cliapp = CLIApplication('example', f'{__name__}:app.climain')

    with Given(cliapp, 'db bar'):
        assert status == 0
        assert stderr == ''
        assert stdout == 'bar\n'
