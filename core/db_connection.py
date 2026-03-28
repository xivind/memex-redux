# core/db_connection.py — Peewee initialisation and connection management
import json
from pathlib import Path

from peewee import MySQLDatabase
from pydantic import BaseModel


class Config(BaseModel):
    mariadb_host: str
    mariadb_database: str
    mariadb_user: str
    mariadb_password: str
    mariadb_port: int = 3306
    velo_supervisor_url: str = ""
    server_port: int = 8002


def _load_config() -> Config:
    path = Path(__file__).parent.parent / "config.json"
    with open(path) as f:
        return Config(**json.load(f))


config = _load_config()

db = MySQLDatabase(
    config.mariadb_database,
    host=config.mariadb_host,
    port=config.mariadb_port,
    user=config.mariadb_user,
    password=config.mariadb_password,
)


def check_db_connection() -> bool:
    try:
        db.connect(reuse_if_open=True)
        db.execute_sql("SELECT 1")
        return True
    except Exception:
        return False
