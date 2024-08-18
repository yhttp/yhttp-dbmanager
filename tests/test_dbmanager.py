DBNAME = 'yhttp-postgesql-testing'


def test_dbmanager(dbmanager):
    # Cleanup
    dbmanager.dropifexists(DBNAME)

    assert dbmanager.exists('postgres')
    assert not dbmanager.exists(DBNAME)

    dbmanager.create(DBNAME)
    assert dbmanager.exists(DBNAME)

    dbmanager.create(DBNAME, dropifexists=True)
    assert dbmanager.exists(DBNAME)

    dbmanager.drop(DBNAME)
    assert not dbmanager.exists(DBNAME)

    dbmanager.create(DBNAME)
    dbmanager.dropifexists(DBNAME)
    assert not dbmanager.exists(DBNAME)
