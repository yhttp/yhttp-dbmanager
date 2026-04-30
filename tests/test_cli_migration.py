import os
import tempfile

from bddcli import Given, Application as CLIApplication, status, stderr, \
    when, stdout
from yhttp.core import Application

from yhttp.ext.dbmanager import install


vdir = tempfile.mkdtemp()
app = Application('0.1.0', 'foo')
app.settings.merge(f'''
db:
  url: postgres://:@/foo
  migration:
    directory: {vdir}
''')
if os.environ.get('CI') and os.environ.get('GITHUB_RUN_ID'):
    app.settings.db.url = 'postgres://postgres:postgres@localhost/foo'

install(app)


foo_content = '''
def upgrade(db):
    db.execute("""
    CREATE TABLE foo (
        id SERIAL PRIMARY KEY,
        title VARCHAR(50) NOT NULL
    );
    """)


def downgrade(db):
    db.execute("DROP TABLE foo")
'''
with open(f'{vdir}/0001-foo.py', 'w') as f:
    f.write(foo_content)


def test_cli_migration():
    cliapp = CLIApplication('foo', f'{__name__}:app.climain')
    env = os.environ.copy()

    with Given(cliapp, 'db migration', environ=env):
        when('db drop')
        when('db create')
        assert status == 0

        when('db migration upgrade 1')
        assert stderr == ''
        assert status == 0
        assert stdout == 'database successfully upgraded to version 0001.\n'

        when('db migration downgrade 0')
        assert stderr == ''
        assert stdout == 'database successfully downgraded to version 0000.\n'
        assert status == 0

        when('db migration upgrade')
        assert stderr == ''
        assert status == 0
        assert stdout == 'database successfully upgraded to version 0001.\n'

        when('db migration new bar')
        assert stderr == ''
        assert status == 0
        assert stdout.endswith('/0002-bar.py.\n')

        when('db migration set foo')
        assert stderr == 'invalid version: foo\n'
        assert status == 1
        assert stdout == ''

        when('db migration set 0')
        assert stderr == ''
        assert status == 0
        assert stdout == 'database successfully set to version 0000.\n'

        when('db migration get')
        assert stderr == ''
        assert status == 0
        assert stdout == '0\n'

        when('db migration get last')
        assert stderr == ''
        assert status == 0
        assert stdout == '1\n'

        when('db migration set last')
        assert stderr == ''
        assert status == 0
        assert stdout == 'database successfully set to version 0001.\n'

        when('db migration get')
        assert stderr == ''
        assert status == 0
        assert stdout == '1\n'

        when('db drop')
        assert status == 0
