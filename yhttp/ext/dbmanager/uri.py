import re


URIPATTERN = re.compile(
    r'(?P<provider>.*)://(?P<user>.*):(?P<password>.*)@(?P<host>.*)/'
    r'(?P<database>.*)'
)


class DatabaseURI:
    def __init__(self, provider, database, host='', user='', password=''):
        assert provider
        assert database

        self.provider = provider
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def dumps(self):
        return f'{self.provider}://{self.user}:{self.password}@{self.host}' \
            f'/{self.database}'

    @classmethod
    def loads(cls, uri):
        match = URIPATTERN.match(uri)
        if not match:
            raise ValueError(f'Invalid URI: {uri}')

        u = match.groupdict()

        assert u.get('provider')
        assert u.get('database')
        return cls(
            u.get('provider'),
            u.get('database'),
            u.get('host'),
            u.get('user'),
            u.get('password'),
        )

    def todict(self):
        return dict(
            provider=self.provider,
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database
        )
