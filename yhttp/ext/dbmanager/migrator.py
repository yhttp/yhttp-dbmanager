import os
import glob


class Migrator:
    defaultsettings = '''
    '''

    def __init__(self, settings):
        self._settings = settings

    def version_new(self, title):
        vdir = self._settings.directory
        if not os.path.exists(vdir):
            os.mkdir(vdir)

        versions = glob.glob(f'{vdir}/*.py')
