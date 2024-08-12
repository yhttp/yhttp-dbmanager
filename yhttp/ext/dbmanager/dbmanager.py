import abc

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DatabaseManager(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def execute(self, query):  # pragma: no cover
        pass

    @abc.abstractmethod
    def create(self, name, owner=None, dropifexists=False):  # pragma: no cover
        pass

    @abc.abstractmethod
    def drop(self, name):  # pragma: no cover
        pass

    @abc.abstractmethod
    def exists(self, name):  # pragma: no cover
        pass

    @abc.abstractmethod
    def dropifexists(self, name):  # pragma: no cover
        pass


class PostgresqlManager(DatabaseManager):

    def __init__(self, host=None, database='postgres', user=None,
                 password=None):
        self.connection = psycopg2.connect(
            host=host,
            dbname=database,
            user=user,
            password=password
        )
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    def execute(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
        finally:
            cursor.close()

    def exists(self, name):
        query = f'SELECT 1 FROM pg_database WHERE datname=\'{name}\''

        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            r = cursor.fetchone()
            if r:
                return r[0] == 1
            else:
                return False
        finally:
            cursor.close()

    def create(self, name, owner=None, dropifexists=False):
        if dropifexists:
            self.dropifexists(name)

        query = f'CREATE DATABASE "{name}"' + \
            (f' WITH OWNER {owner}' if owner else '')

        self.execute(query)

    def drop(self, name):
        self.execute(f'DROP DATABASE "{name}"')

    def dropifexists(self, name):
        self.execute(f'DROP DATABASE IF EXISTS "{name}"')
