import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open


def _make_config(**overrides):
    base = {
        "mariadb_host": "testhost",
        "mariadb_database": "testdb",
        "mariadb_user": "user",
        "mariadb_password": "pass",
        "mariadb_port": 3306,
        "velo_supervisor_url": "http://vs:8003",
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


def test_config_missing_required_field_raises():
    bad = json.dumps({"mariadb_host": "h"})  # missing required fields
    with patch("builtins.open", mock_open(read_data=bad)):
        from importlib import reload
        import core.db_connection as db_mod
        with pytest.raises(Exception):
            reload(db_mod)


def test_check_db_connection_returns_false_on_error():
    from unittest.mock import MagicMock
    import core.db_connection as db_mod
    db_mod.db.connect = MagicMock(side_effect=Exception("no db"))
    assert db_mod.check_db_connection() is False
