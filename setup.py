import os.path
import re

from setuptools import setup, find_namespace_packages


# reading package's version (same way sqlalchemy does)
with open(
    os.path.join(
        os.path.dirname(__file__),
        'yhttp/ext/dbmanager/', '__init__.py'
    )
) as v_file:
    package_version = \
        re.compile('.*__version__ = \'(.*?)\'', re.S)\
        .match(v_file.read())\
        .group(1)


dependencies = [
    'yhttp >= 7.0.1, < 8',
    'psycopg2',
]


setup(
    name='yhttp-dbmanager',
    version=package_version,
    author='Vahid Mardani',
    author_email='vahid.mardani@gmail.com',
    url='http://github.com/yhttp/yhttp-dbmanager',
    description='Database manager command line interface and API for yhttp.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # This is important!
    install_requires=dependencies,
    packages=find_namespace_packages(
        where='./',
        include=['yhttp.ext.dbmanager'],
        exclude=['tests']
    ),
    license='MIT',
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Development Status :: 5 - Production/Stable',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
