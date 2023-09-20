from yhttp.ext.dbmanager import DatabaseURI

import pytest


def test_dburi():
    uristr = 'foo://bar:baz@qux/quux.thud'
    uri = DatabaseURI.loads(uristr)

    assert uri.provider == 'foo'
    assert uri.user == 'bar'
    assert uri.password == 'baz'
    assert uri.host == 'qux'
    assert uri.dbname == 'quux.thud'
    assert uri.dumps() == uristr


    # Invalid uri
    uristr = 'baduri'
    with pytest.raises(ValueError):
        DatabaseURI.loads(uristr)
