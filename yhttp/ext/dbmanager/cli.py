import os
import functools
import getpass

from easycli import SubCommand, Argument

from . import dbmanager
from .uri import DatabaseURI


getdbpass = functools.partial(getpass.getpass, 'Enter db password: ')


DEFAULT_DBUSER = os.environ['USER']


class DatabaseAdministrativeCommand(SubCommand):
    __arguments__ = [
        Argument(
            '-H',
            '--host',
            default=os.environ.get('YHTTP_DB_DEFAULT_HOST', ''),
            help='DB hostname, default: empty.'
        ),
        Argument('-d', '--database', default='postgres', help='DB name'),
        Argument(
            '-u',
            '--user',
            default=os.environ.get(
                'YHTTP_DB_DEFAULT_ADMINUSER',
                DEFAULT_DBUSER
            ),
            help=f'DB administrator username, default: ${DEFAULT_DBUSER}'
        ),
        Argument(
            '-p', '--password',
            nargs='?',
            default=os.environ.get(
                'YHTTP_DB_DEFAULT_ADMINPASS',
                'postgres'
            ),
            help='DB administrator password'
        ),
    ]

    def getdbmanager(self, args):
        password = args.password or getdbpass()

        return dbmanager.PostgresqlManager(
            user=args.user,
            password=password,
            host=args.host,
            database=args.database
        )

    def getappdbinfo(self, args):
        dbsettings = args.application.settings.db
        url = DatabaseURI.loads(dbsettings.url)
        return url


class CreateDatabase(DatabaseAdministrativeCommand):
    __command__ = 'create'
    __aliases__ = ['c']

    def __call__(self, args):
        uri = self.getappdbinfo(args)
        self.getdbmanager(args).create(uri.database, owner=uri.user)


class DropDatabase(DatabaseAdministrativeCommand):
    __command__ = 'drop'
    __aliases__ = ['d']

    def __call__(self, args):
        uri = self.getappdbinfo(args)
        self.getdbmanager(args).drop(uri.database)


class DatabaseCommand(SubCommand):
    __command__ = 'database'
    __aliases__ = ['db']
    __arguments__ = [
        CreateDatabase,
        DropDatabase
    ]
