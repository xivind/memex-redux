import json
import pytest
from unittest.mock import patch, mock_open


def _make_config(**overrides):
    base = {
        "mariadb_host": "testhost",
        "mariadb_database": "testdb",
        "mariadb_user": "user",
        "mariadb_password": "pass",
        "mariadb_port": 3306,
        "api_domains": {},
        "server_port": 8002,
    }
    base.update(overrides)
    return json.dumps(base)


def test_config_loads_all_fields():
    with patch("builtins.open", mock_open(read_data=_make_config())):
        from importlib import reload
        import core.db_connection as db_mod
        reload(db_mod)
        assert db_mod.config.mariadb_host == "testhost"
        assert db_mod.config.mariadb_port == 3306


def test_config_no_db_fields_loads_with_none():
    minimal = json.dumps({"server_port": 8002})
    with patch("builtins.open", mock_open(read_data=minimal)):
        from importlib import reload
        import core.db_connection as db_mod
        reload(db_mod)
        assert db_mod.config.mariadb_host is None
        assert db_mod.db is None


def test_check_db_connection_returns_false_when_db_none():
    import core.db_connection as db_mod
    original_db = db_mod.db
    db_mod.db = None
    assert db_mod.check_db_connection() is False
    db_mod.db = original_db


def test_check_db_connection_returns_false_on_error():
    from unittest.mock import MagicMock
    import core.db_connection as db_mod
    if db_mod.db is None:
        pytest.skip("No DB configured")
    db_mod.db.connect = MagicMock(side_effect=Exception("no db"))
    assert db_mod.check_db_connection() is False


def test_config_loads_api_domains():
    cfg_json = json.dumps({
        "mariadb_host": "testhost",
        "mariadb_database": "testdb",
        "mariadb_user": "user",
        "mariadb_password": "pass",
        "mariadb_port": 3306,
        "api_domains": {
            "My Service": "http://api:8003",
            "Another Service": "http://api2:8004",
        },
        "server_port": 8002,
    })
    with patch("builtins.open", mock_open(read_data=cfg_json)):
        from importlib import reload
        import core.db_connection as db_mod
        reload(db_mod)
        assert db_mod.config.api_domains == {
            "My Service": "http://api:8003",
            "Another Service": "http://api2:8004",
        }
