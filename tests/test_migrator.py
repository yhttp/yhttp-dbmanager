import pytest


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


bar_content = '''
def upgrade(db):
    db.execute("""
    CREATE TABLE bar (
        id SERIAL PRIMARY KEY,
        title VARCHAR(50) NOT NULL
    );
    """)


def downgrade(db):
    db.execute("DROP TABLE bar")
'''


def test_migrator_upgrade_downgrade(migrator, mktmptree):
    root = mktmptree({
        '0001-foo.py': foo_content,
        '0002-bar.py': bar_content,
    })
    migrator.settings.directory = root

    assert migrator.dbversion() == 0
    assert migrator.lastversion == 2

    assert 2 == migrator.upgrade()
    assert migrator.db.table_exists('foo')
    assert migrator.db.table_exists('bar')

    assert 0 == migrator.downgrade()
    assert not migrator.db.table_exists('foo')
    assert not migrator.db.table_exists('bar')

    with pytest.raises(FileNotFoundError):
        migrator.upgrade(3)

    migrator.dbversion_set(3)
    with pytest.raises(FileNotFoundError):
        migrator.downgrade(2)


def test_migrator_newversion(migrator, tmpdir):
    migrator.settings.directory = f'{tmpdir}/versions'

    assert f'{tmpdir}/versions/0001-foo.py' == migrator.newversion('foo')
    assert f'{tmpdir}/versions/0002-bar.py' == migrator.newversion('bar')
