# models.py — All Peewee model definitions
#
# Copy this file to models.py and define your own database tables.
# Each class maps to one table. Use these as templates for your data sources.
#
# models.py is gitignored because it reflects your specific database schema.

import peewee
from core.db_connection import db


# ---------------------------------------------------------------------------
# Example: a simple time-series table
# ---------------------------------------------------------------------------

class SensorReading(peewee.Model):
    record_time = peewee.DateTimeField(primary_key=True)
    sensor_name = peewee.TextField()
    value = peewee.FloatField()

    class Meta:
        database = db
        table_name = "sensor_readings"


# ---------------------------------------------------------------------------
# Example: a table with no single primary key (use primary_key = False)
# ---------------------------------------------------------------------------

class Event(peewee.Model):
    record_time = peewee.DateTimeField()
    event_type = peewee.TextField()
    description = peewee.TextField(null=True)

    class Meta:
        database = db
        table_name = "events"
        primary_key = False


# ---------------------------------------------------------------------------
# Example: a table with a composite primary key
# ---------------------------------------------------------------------------

class DailyMetric(peewee.Model):
    user_id = peewee.BigIntegerField()
    date = peewee.DateField()
    metric_name = peewee.TextField()
    value = peewee.FloatField(null=True)

    class Meta:
        database = db
        table_name = "daily_metrics"
        primary_key = peewee.CompositeKey("user_id", "date")
