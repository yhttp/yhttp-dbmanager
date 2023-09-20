import yhttp

from .cli import DatabaseCLI


def install(app, cliarguments=None):
    app.cliarguments.append(DatabaseCLI)
    if cliarguments:
        DatabaseCLI.__arguments__.extend(cliarguments)

    @app.when
    def ready(app):
        if 'db' not in app.settings:
            raise ValueError(
                'Please provide db.url configuration entry, for example: '
                'postgres://:@/dbname'
            )

    return app
