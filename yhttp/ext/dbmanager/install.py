from .cli import DatabaseCommand


def install(app, cliarguments=None):
    app.cliarguments.append(DatabaseCommand)
    if cliarguments:
        DatabaseCommand.__arguments__.extend(cliarguments)

    app.settings.merge('''
    db:
      migration: {}
    ''')

    @app.when
    def ready(app):
        if 'url' not in app.settings.db or \
                'directory' not in app.settings.db.migration:
            raise ValueError(
                'Please provide db.url configuration entry, for example: '
                'postgres://:@/dbname'
            )
