from pymlconf import Meld

from .cli import DatabaseCommand
from .migration import Migrator


def install(app, cliarguments=None):
    app.cliarguments.append(DatabaseCommand)
    if cliarguments:
        DatabaseCommand.__arguments__.extend(cliarguments)

    app.settings |= Meld(
        Meld(Migrator.default_settings, root='migration'),
        root='db'
    )

    @app.when
    def ready(app):
        if 'url' not in app.settings.db:
            raise ValueError(
                'Please provide db.url configuration entry, for example: '
                'postgres://:@/dbname'
            )
