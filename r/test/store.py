from unittest.mock import patch
import nose.tools
import r.store

@r.store.cached()
def cached_fn(value):
    uncached_fn(value)
    return value

def uncached_fn(value):
    return value

@r.store.cached(wildcard=['bar'])
def wildcard_fn(foo, bar=0):
    uncached_fn(foo)
    return foo + bar

def setup():
    r.store.configure()
    r.store._flush_I_KNOW_WHAT_IM_DOING()

def teardown():
    r.store._flush_I_KNOW_WHAT_IM_DOING()

@nose.tools.with_setup(setup, teardown)
def test_cached():
    with patch('r.test.store.uncached_fn') as mock_uncached_fn:
        value = 5
        assert cached_fn(value) == value
        assert mock_uncached_fn.called

        mock_uncached_fn.reset_mock()
        assert cached_fn(value) == value
        assert not mock_uncached_fn.called

@nose.tools.with_setup(setup, teardown)
def test_delete():
    key = 'foo'
    value = 'bar'
    r.store.set(key, value)
    assert r.store.get(key) == value
    r.store.delete(key)
    assert not r.store.get(key)

@nose.tools.with_setup(setup, teardown)
def test_dirty():
    with patch('r.test.store.uncached_fn') as mock_uncached_fn:
        value = 5
        assert cached_fn(value) == value
        assert mock_uncached_fn.called

        mock_uncached_fn.reset_mock()
        assert cached_fn(value) == value
        assert not mock_uncached_fn.called

        mock_uncached_fn.reset_mock()
        cached_fn.dirty(value)
        assert cached_fn(value) == value
        assert mock_uncached_fn.called

@nose.tools.with_setup(setup, teardown)
def test_exclude():
    with patch('r.test.store.uncached_fn') as mock_uncached_fn:
        one = 1
        two = 2
        three = 3

        mock_uncached_fn.reset_mock()
        assert wildcard_fn(one, two) == one + two
        assert mock_uncached_fn.called

        mock_uncached_fn.reset_mock()
        assert wildcard_fn(one, three) == one + three
        assert mock_uncached_fn.called

        mock_uncached_fn.reset_mock()
        assert wildcard_fn(two, three) == two + three
        assert mock_uncached_fn.called

        mock_uncached_fn.reset_mock()
        assert wildcard_fn(one, two) == one + two
        assert not mock_uncached_fn.called

        mock_uncached_fn.reset_mock()
        assert wildcard_fn(one, three) == one + three
        assert not mock_uncached_fn.called

        mock_uncached_fn.reset_mock()
        assert wildcard_fn(two, three) == two + three
        assert not mock_uncached_fn.called

        wildcard_fn.dirty(one)

        mock_uncached_fn.reset_mock()
        assert wildcard_fn(one, two) == one + two
        assert mock_uncached_fn.called

        mock_uncached_fn.reset_mock()
        assert wildcard_fn(one, three) == one + three
        assert mock_uncached_fn.called

        mock_uncached_fn.reset_mock()
        assert wildcard_fn(two, three) == two + three
        assert not mock_uncached_fn.called

@nose.tools.with_setup(setup, teardown)
def test_multi():
    string = {
        'string1': 'bar',
        'string2': 'qux'
    }
    r.store.set_multi(string)
    assert r.store.get_multi(list(string.keys())) == string

    lst = {
        'list1': [1, 2, 3],
        'list2': [4, 5, 6]
    }
    r.store.set_multi(lst)
    assert r.store.get_multi(list(lst.keys())) == lst

    dictionary = {
        'dictionary1': {'a': 5},
        'dictionary2': {'b': 'str'}
    }
    r.store.set_multi(dictionary)
    assert r.store.get_multi(list(dictionary.keys())) == dictionary

@nose.tools.with_setup(setup, teardown)
def test_single():
    string = 'bar'
    r.store.set('string', string)
    assert r.store.get('string') == string

    list = [1, 2, 3]
    r.store.set('list', list)
    assert r.store.get('list') == list

    dictionary = {'a': 5, 'b': 6}
    r.store.set('dictionary', dictionary)
    assert r.store.get('dictionary') == dictionary
