import os
import glob
import importlib
from functools import cached_property
from contextlib import contextmanager

import psycopg2


VERSIONFILE_TEMPLATE = '''\
def upgrade(db):
    raise NotImplementedError()


def downgrade(db):
    raise NotImplementedError()
'''


class Database:
    def __init__(self, url):
        self.url = url

    @cached_property
    def connection(self):
        return psycopg2.connect(self.url)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def execute(self, query):
        with self.connection.cursor() as c:
            c.execute(query)

    @contextmanager
    def select(self, query):
        with self.connection.cursor() as c:
            c.execute(query)
            yield c

    def exists(self, query):
        query = f'SELECT EXISTS ({query});'

        with self.connection.cursor() as c:
            c.execute(query)
            r = c.fetchone()
            return r[0]

    def table_exists(self, name):
        return self.exists(f'''
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = '{name}'
        ''')


class Migrator:
    default_settings = '''
      versiontable: yhttp_version
    '''

    def __init__(self, url, settings):
        self.url = url
        self.settings = settings

    def __enter__(self):
        self.db
        return self

    def __exit__(self, exctype, excvalue, traceback):
        self.close()

    @cached_property
    def db(self):
        return Database(self.url)

    def close(self):
        self.db.close()

    @cached_property
    def vtable(self):
        return self.settings.versiontable

    def ensure_versiontable(self):
        if self.db.table_exists(self.vtable):
            return

        self.db.execute(f'''
            CREATE TABLE {self.vtable} (
                version INTEGER NOT NULL
            );
        ''')

        self.db.execute(f'''
            INSERT INTO {self.vtable} (version) VALUES (0);
        ''')
        self.db.commit()

    def dbversion(self):
        self.ensure_versiontable()
        with self.db.select(f'SELECT version from {self.vtable}') as c:
            return c.fetchone()[0]

    def dbversion_set(self, ver):
        self.db.execute(f'UPDATE {self.vtable} SET version={ver}')
        self.db.commit()

    @cached_property
    def versions_directory(self):
        try:
            vdir = self.settings.directory
        except AttributeError:
            raise ValueError(
                'Please provide db.migration.directory configuration entry.'
            )

        if not os.path.exists(vdir):
            os.mkdir(vdir)

        return vdir

    @property
    def lastversion(self):
        files = glob.glob(f'{self.versions_directory}/*-*.py')
        if not files:
            return 0

        lastfile = sorted(files)[-1]
        ver = os.path.basename(lastfile).split('-', 1)[0]
        return int(ver)

    def newversion(self, name):
        ver = self.lastversion + 1
        filename = f'{ver:04d}-{name}.py'
        filepath = os.path.join(self.versions_directory, filename)
        with open(filepath, 'w') as f:
            f.write(VERSIONFILE_TEMPLATE)

        return filepath

    def loadmodule(self, ver):
        files = glob.glob(f'{self.versions_directory}/{ver:04d}-*.py')
        if not files:
            return None

        modfile = files[0]
        modname = os.path.splitext(os.path.basename(modfile))[0]
        spec = importlib.util.spec_from_file_location(modname, modfile)
        mod = importlib.util.module_from_spec(spec)
        # sys.modules[module_name] = module
        spec.loader.exec_module(mod)
        return mod

    def filenotfound(self, ver):
        return FileNotFoundError(
            f'script {ver:04d}_*.py not found within directory: '
            f'{self.versions_directory}.'
        )

    def upgrade(self, targetver=None):
        dbver = self.dbversion()
        if targetver is None:
            targetver = self.lastversion

        while dbver < targetver:
            cver = dbver + 1
            mod = self.loadmodule(cver)
            if mod is None:
                raise self.filenotfound(cver)

            mod.upgrade(self.db)
            self.dbversion_set(cver)
            dbver = cver

        return targetver

    def downgrade(self, targetver=0):
        dbver = self.dbversion()
        while dbver > targetver:
            mod = self.loadmodule(dbver)
            if mod is None:
                raise self.filenotfound(dbver)

            mod.downgrade(self.db)
            dbver -= 1
            self.dbversion_set(dbver)

        return targetver
