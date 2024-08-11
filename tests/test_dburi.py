from yhttp.ext.dbmanager import DatabaseURI

import pytest


def test_dburi():
    uristr = 'foo://bar:baz@qux/quux.thud'
    uri = DatabaseURI.loads(uristr)

    assert uri.provider == 'foo'
    assert uri.user == 'bar'
    assert uri.password == 'baz'
    assert uri.host == 'qux'
    assert uri.database == 'quux.thud'
    assert uri.dumps() == uristr

    # Invalid uri
    uristr = 'baduri'
    with pytest.raises(ValueError):
        DatabaseURI.loads(uristr)

    # Without password
    uristr = 'foo://bar:@qux/quux.thud'
    uri = DatabaseURI.loads(uristr)
    assert uri.provider == 'foo'
    assert uri.user == 'bar'
    assert uri.password == ''
    assert uri.host == 'qux'
    assert uri.database == 'quux.thud'
    assert uri.dumps() == uristr

    # Without username and password
    uristr = 'foo://:@qux/quux.thud'
    uri = DatabaseURI.loads(uristr)
    assert uri.provider == 'foo'
    assert uri.user == ''
    assert uri.password == ''
    assert uri.host == 'qux'
    assert uri.database == 'quux.thud'
    assert uri.dumps() == uristr

    # Without username, password and host
    uristr = 'foo://:@/quux.thud'
    uri = DatabaseURI.loads(uristr)
    assert uri.provider == 'foo'
    assert uri.user == ''
    assert uri.password == ''
    assert uri.host == ''
    assert uri.database == 'quux.thud'
    assert uri.dumps() == uristr


def test_dburi_todict():
    uristr = 'foo://bar:baz@qux/quux.thud'
    uri = DatabaseURI.loads(uristr)

    assert uri.todict() == dict(
        provider='foo',
        user='bar',
        password='baz',
        host='qux',
        database='quux.thud'
    )
