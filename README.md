# yhttp-dbmanager

A `yhttp` extension to create and remove database(s) using command line and
API.


## Quickstart

### Dependencies
Install `postgresql` brefore use of this project.
```bash
apt install postgresql
```

### Prepare

Create and grant the `postgresql` role with `createdb` permission to 
authenticate the current `unix` user within `postgresql` using the peer 
authentication.
```bash
echo "CREATE USER ${USER} WITH CREATEDB" | sudo -u postgres psql
# Or
echo "ALTER USER ${USER} CREATEDB" | sudo -u postgres psql
```

### Usage

Import and install the extension inside the `roolup.py`:

```python
# foo/version.py
__version__ = '0.1.'
```


```python
# foo/rollup.py
from yhttp.core import Application
from yhttp.ext import dbmanager

from .version import __version__


app = Application(__version__, 'foo')


# builtin settings
app.settings.merge('''
db:
  url: postgres://:@/ticketing
```)


# install extensions
dbmanager.install(app)


# http handlers
from . import handlers
```


```python
# foo/__init__.py
from .version import __version__
from .rollup import app
```


```python
# setup.py
import re
from os.path import join, dirname

from setuptools import setup, find_packages


# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'foo/version.py')) as v_file:
    package_version = re.compile('.*__version__ = \'(.*?)\'', re.S).\
        match(v_file.read()).group(1)


dependencies = [
    'yhttp >= 7.0.1, < 8'
    'yhttp-dbmanager >= 5.0.1, < 6'
]


setup(
    name='foo',
    version=package_version,
    install_requires=dependencies,
    packages=find_packages(
        where='.',
        exclude=['tests']
    ),
    entry_points={
        'console_scripts': [
            'foo = foo:app.climain'
        ]
    },
)

```

After installing the extension these command line interfaces will be available
as as subcommand of your application command line interface:
```bash
foo db --help
```


## Contribution

### Dependencies
Install `postgresql` brefore use of this project.
```bash
apt install postgresql
```

### Prepare

Create and grant the `postgresql` role with `createdb` permission to 
authenticate the current `unix` user within `postgresql` using the peer 
authentication.
```bash
echo "CREATE USER ${USER} WITH CREATEDB" | sudo -u postgres psql
# Or
echo "ALTER USER ${USER} CREATEDB" | sudo -u postgres psql
```

### Virtualenv

Create virtual environment:
```bash
make venv
```

Delete virtual environment:
```bash
make venv-delete
```

Activate the virtual environment:
```bash
source ./activate.sh
```


### Install (editable mode)
Install this project as editable mode and all other development dependencies:
```bash
make env
```


### Tests
Execute all tests:
```bash
make test
```

Execute specific test(s) using wildcard:
```bash
make test F=tests/test_db*
make test F=tests/test_form.py::test_querystringform
```

*refer to* [pytest documentation](https://docs.pytest.org/en/7.1.x/how-to/usage.html#how-to-invoke-pytest)
*for more info about invoking tests.*

Execute tests and report coverage result:
```bash
make cover
make cover F=tests/test_static.py
make cover-html
```


# Lint
```bash
make lint
```


### Distribution
Execute these commands to create `Python`'s standard distribution packages
at `dist` directory:
```bash
make sdist
make wheel
```

Or 
```bash
make dist
```
to create both `sdidst` and `wheel` packages.


### Clean build directory
Execute: 
```bash
make clean
```
to clean-up previous `dist/*` and `build/*` directories.


### PyPI

> **_WARNING:_** Do not do this if you'r not responsible as author and 
> or maintainer of this project.

Execute
```bash
make clean
make pypi
```
to upload `sdists` and `wheel` packages on [PyPI](https://pypi.org).
