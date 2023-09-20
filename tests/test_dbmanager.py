from yhttp.ext.dbmanager import PostgresqlManager


DBNAME = 'yhttp-postgesql-testing'


def test_dbmanager():
    # Instance with postgres identity framework.
    dbm = PostgresqlManager()

    # Cleanup
    dbm.dropifexists(DBNAME)

    assert dbm.exists('postgres')
    assert not dbm.exists(DBNAME)

    dbm.create(DBNAME)
    assert dbm.exists(DBNAME)

    dbm.create(DBNAME, dropifexists=True)
    assert dbm.exists(DBNAME)

    dbm.drop(DBNAME)
    assert not dbm.exists(DBNAME)

    dbm.create(DBNAME)
    dbm.dropifexists(DBNAME)
    assert not dbm.exists(DBNAME)
