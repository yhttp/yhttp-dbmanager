import os
import functools
import getpass

from easycli import SubCommand, Argument

from . import dbmanager, migration
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


class CreateDatabaseCommand(DatabaseAdministrativeCommand):
    __command__ = 'create'
    __aliases__ = ['c']

    def __call__(self, args):
        uri = self.getappdbinfo(args)
        self.getdbmanager(args).create(uri.database, owner=uri.user)


class DropDatabaseCommand(DatabaseAdministrativeCommand):
    __command__ = 'drop'
    __aliases__ = ['d']

    def __call__(self, args):
        uri = self.getappdbinfo(args)
        self.getdbmanager(args).drop(uri.database)


class MigrationSubCommand(SubCommand):
    def migrator(self, args):
        app = args.application
        migrator = migration.Migrator(
            app.settings.db.url,
            app.settings.db.migration
        )
        return migrator


class UpgradeCommand(MigrationSubCommand):
    __command__ = 'upgrade'
    __aliases__ = ['u', 'up']
    __arguments__ = [
        Argument(
            'version',
            nargs='?',
            metavar='VERSION',
            type=int,
            help='Upgrade to this version, default: last version'
        )
    ]

    def __call__(self, args):
        with self.migrator(args) as m:
            ver = m.upgrade(args.version)

        print(f'database successfully upgraded to version {ver:04d}.')


class DowngradeCommand(MigrationSubCommand):
    __command__ = 'downgrade'
    __aliases__ = ['d', 'down']
    __arguments__ = [
        Argument(
            'version',
            metavar='VERSION',
            type=int,
            help='Upgrade to this version.'
        )
    ]

    def __call__(self, args):
        with self.migrator(args) as m:
            ver = m.downgrade(args.version)

        print(f'database successfully downgraded to version {ver:04d}.')


class NewVersionCommand(MigrationSubCommand):
    __command__ = 'new'
    __aliases__ = ['n']
    __arguments__ = [
        Argument(
            'name',
            metavar='TITLE',
            help='Creates a new database version file'
        )
    ]

    def __call__(self, args):
        with self.migrator(args) as m:
            ver = m.newversion(args.name)

        print(f'File generated successfully: {ver}.')


class SetVersionCommand(MigrationSubCommand):
    __command__ = 'set'
    __aliases__ = ['s']
    __arguments__ = [
        Argument(
            'version',
            metavar='VERSION',
            type=int,
            help='database version.'
        )
    ]

    def __call__(self, args):
        ver = args.version
        with self.migrator(args) as m:
            m.dbversion_set(ver)

        print(f'database successfully set to version {ver:04d}.')


class MigrationCommand(SubCommand):
    __command__ = 'migration'
    __aliases__ = ['mi']
    __arguments__ = [
        UpgradeCommand,
        DowngradeCommand,
        NewVersionCommand,
        SetVersionCommand
    ]

    def __call__(self, args):
        self._parser.print_help()


class DatabaseCommand(SubCommand):
    __command__ = 'database'
    __aliases__ = ['db']
    __arguments__ = [
        CreateDatabaseCommand,
        DropDatabaseCommand,
        MigrationCommand
    ]
