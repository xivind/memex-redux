# core/db_connection.py — Peewee initialisation and connection management
import json
from pathlib import Path

from peewee import MySQLDatabase
from pydantic import BaseModel


class Config(BaseModel):
    mariadb_host: str | None = None
    mariadb_database: str | None = None
    mariadb_user: str | None = None
    mariadb_password: str | None = None
    mariadb_port: int = 3306
    api_domains: dict[str, str] = {}
    server_port: int = 8002
    yr_api_key: str | None = None


def _load_config() -> Config:
    path = Path(__file__).parent.parent / "config.json"
    with open(path) as f:
        return Config(**json.load(f))


config = _load_config()

db: MySQLDatabase | None = (
    MySQLDatabase(
        config.mariadb_database,
        host=config.mariadb_host,
        port=config.mariadb_port,
        user=config.mariadb_user,
        password=config.mariadb_password,
    )
    if config.mariadb_host
    else None
)


def check_db_connection() -> bool:
    if db is None:
        return False
    try:
        db.connect(reuse_if_open=True)
        db.execute_sql("SELECT 1")
        return True
    except Exception:
        return False
