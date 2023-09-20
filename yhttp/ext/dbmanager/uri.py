import re


URIPATTERN = re.compile(
    r'(?P<provider>.*)://(?P<user>.*):(?P<password>.*)@(?P<host>.*)/'
    r'(?P<dbname>.*)'
)


class DatabaseURI:
    def __init__(self, provider, dbname, host='', user='', password=''):
        assert provider
        assert dbname

        self.provider = provider
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password

    def dumps(self):
        return f'{self.provider}://{self.user}:{self.password}@{self.host}' \
            f'/{self.dbname}'

    @classmethod
    def loads(cls, uri):
        match = URIPATTERN.match(uri)
        if not match:
            raise ValueError(f'Invalid URI: {uri}')

        u = match.groupdict()

        assert u.get('provider')
        assert u.get('dbname')
        return cls(
            u.get('provider'),
            u.get('dbname'),
            u.get('host'),
            u.get('user'),
            u.get('password'),
        )
