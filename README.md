# Dependencies
install `postgreslq` brefore use of this project.


## Contribution

### Prepare

Create and grant `postgres` role with `createdb` permission:
```bash
echo "CREATE USER ${USER} WITH CREATEDB" | sudo -u postgres psql
# Or
echo "ALTER USER ${USER} CREATEDB" | sudo -u postgres psql
```

Create virtual environment:
```bash
make venv
```

Install this project as editable mode and all other development dependencies:
```bash
make env
```

### Tests
Execute all tests:
```bash
make test
```

Execute all tests and report coverage result:
```bash
make cover
```

### Virtualenv
```bash
source ./activate.sh
```
