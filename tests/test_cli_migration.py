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


def test_cli_migration(cicd):
    cliapp = CLIApplication('foo', f'{__name__}:app.climain')
    env = os.environ.copy()
    if cicd:
        env.setdefault('YHTTP_DB_DEFAULT_HOST', 'localhost')
        env.setdefault('YHTTP_DB_DEFAULT_ADMINUSER', 'postgres')
        env.setdefault('YHTTP_DB_DEFAULT_ADMINPASS', 'postgres')

    with Given(cliapp, 'db migration', enviiron=env):
        when('db drop')
        when('db create')
        assert status == 0

        when('db migration upgrade 1')
        assert stdout == 'database successfully upgraded to version 0001.\n'
        assert stderr == ''
        assert status == 0

        when('db migration downgrade 0')
        assert stderr == ''
        assert stdout == 'database successfully downgraded to version 0000.\n'
        assert status == 0

        when('db migration upgrade')
        assert stdout == 'database successfully upgraded to version 0001.\n'
        assert stderr == ''
        assert status == 0

        when('db migration new bar')
        assert stderr == ''
        assert stdout.endswith('/0002-bar.py.\n')
        assert status == 0

        when('db drop')
        assert status == 0
