# flake8: noqa
from .cli import DatabaseCommand
from .install import install
from .dbmanager import PostgresqlManager
from .uri import DatabaseURI
from .migration import Migrator


__version__ = '8.1.1'
