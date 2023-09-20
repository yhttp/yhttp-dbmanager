from yhttp.ext.dbmanager import PostgresqlManager


DBNAME = 'yhttp-postgesql-testing'


def test_dbmanager():
    # TODO: execute
    # TODO: create
    # TODO: drop
    # TODO: dropifexist
    # TODO: exists
    # TODO: DB cleanup fixture to remover db

    # Instance with postgres identity framework.
    dbm = PostgresqlManager()

    assert dbm.exists('postgres')
    assert not dbm.exists(DBNAME)
