# tests/test_vs2000.py


def test_get_vs2000_returns_list():
    from tools.vs2000 import get_vs2000
    result = get_vs2000()
    assert isinstance(result, list)


def test_get_bikes_not_exported():
    import tools.vs2000 as vs2000_module
    assert not hasattr(vs2000_module, "get_bikes"), (
        "get_bikes should be removed — rename to get_vs2000"
    )
