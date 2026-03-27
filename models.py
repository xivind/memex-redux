# models.py — All Peewee model definitions (one per deployment)
import peewee
from core.db_connection import db


# ---------------------------------------------------------------------------
# Finance — ATM provider data
# ---------------------------------------------------------------------------

class Balance(peewee.Model):
    record_time = peewee.DateTimeField(primary_key=True)
    balance = peewee.FloatField()
    account = peewee.TextField()
    card_provider = peewee.TextField()

    class Meta:
        database = db
        table_name = "balance"


class Transaction(peewee.Model):
    unique_id = peewee.TextField()
    record_time = peewee.DateField()
    merchant_name = peewee.TextField()
    merchant_category = peewee.TextField()
    amount = peewee.IntegerField()
    card_provider = peewee.TextField()
    booking_status = peewee.TextField(default="BOOKED")

    class Meta:
        database = db
        table_name = "transactions"
        primary_key = False


# ---------------------------------------------------------------------------
# Finance — Moneybags budgeting system
# ---------------------------------------------------------------------------

class MoneybagCategory(peewee.Model):
    id = peewee.CharField(max_length=10, primary_key=True)
    created_at = peewee.DateTimeField()
    name = peewee.CharField(max_length=255)
    type = peewee.CharField(max_length=10)

    class Meta:
        database = db
        table_name = "moneybags_categories"


class MoneybagPayee(peewee.Model):
    id = peewee.CharField(max_length=10, primary_key=True)
    created_at = peewee.DateTimeField()
    name = peewee.CharField(max_length=255)
    type = peewee.CharField(max_length=10)

    class Meta:
        database = db
        table_name = "moneybags_payees"


class MoneybagBudgetEntry(peewee.Model):
    id = peewee.CharField(max_length=10, primary_key=True)
    created_at = peewee.DateTimeField()
    category = peewee.ForeignKeyField(
        MoneybagCategory, column_name="category_id", backref="budget_entries"
    )
    year = peewee.IntegerField()
    month = peewee.SmallIntegerField()
    amount = peewee.IntegerField()
    updated_at = peewee.DateTimeField()
    comment = peewee.TextField(null=True)

    class Meta:
        database = db
        table_name = "moneybags_budget_entries"


class MoneybagBudgetTemplate(peewee.Model):
    id = peewee.CharField(max_length=10, primary_key=True)
    created_at = peewee.DateTimeField()
    year = peewee.IntegerField()
    category = peewee.ForeignKeyField(
        MoneybagCategory, column_name="category_id", backref="budget_templates"
    )

    class Meta:
        database = db
        table_name = "moneybags_budget_templates"


class MoneybagConfiguration(peewee.Model):
    id = peewee.CharField(max_length=10, primary_key=True)
    created_at = peewee.DateTimeField()
    key = peewee.CharField(max_length=255)
    value = peewee.TextField()
    updated_at = peewee.DateTimeField()

    class Meta:
        database = db
        table_name = "moneybags_configuration"


class MoneybagSupersaverCategory(peewee.Model):
    id = peewee.CharField(max_length=10, primary_key=True)
    name = peewee.CharField(max_length=255)
    created_at = peewee.DateTimeField()
    updated_at = peewee.DateTimeField()

    class Meta:
        database = db
        table_name = "moneybags_supersaver_categories"


class MoneybagSupersaver(peewee.Model):
    id = peewee.CharField(max_length=10, primary_key=True)
    category = peewee.ForeignKeyField(
        MoneybagSupersaverCategory, column_name="category_id", backref="entries"
    )
    amount = peewee.IntegerField()
    date = peewee.DateField()
    comment = peewee.TextField(null=True)
    created_at = peewee.DateTimeField()
    updated_at = peewee.DateTimeField()

    class Meta:
        database = db
        table_name = "moneybags_supersaver"


class MoneybagTransaction(peewee.Model):
    id = peewee.CharField(max_length=10, primary_key=True)
    created_at = peewee.DateTimeField()
    category = peewee.ForeignKeyField(
        MoneybagCategory, column_name="category_id", backref="moneybag_transactions"
    )
    payee = peewee.ForeignKeyField(
        MoneybagPayee, column_name="payee_id", null=True, backref="moneybag_transactions"
    )
    date = peewee.DateField()
    amount = peewee.IntegerField()
    comment = peewee.TextField(null=True)
    updated_at = peewee.DateTimeField()

    class Meta:
        database = db
        table_name = "moneybags_transactions"


# ---------------------------------------------------------------------------
# Health — Fitbit
# ---------------------------------------------------------------------------

class Fitbit(peewee.Model):
    record_time = peewee.DateField(primary_key=True)
    activity_floors = peewee.IntegerField(null=True)
    activity_steps = peewee.IntegerField(null=True)
    calories = peewee.IntegerField(null=True)
    weight_weight = peewee.FloatField(null=True)
    weight_bmi = peewee.FloatField(null=True)
    weight_fat = peewee.FloatField(null=True)
    water = peewee.IntegerField(null=True)
    sleep_total_time_in_bed = peewee.IntegerField(null=True)
    sleep_total_minutes_asleep = peewee.IntegerField(null=True)
    sleep_deep = peewee.IntegerField(null=True)
    sleep_light = peewee.IntegerField(null=True)
    sleep_rem = peewee.IntegerField(null=True)
    sleep_wake = peewee.IntegerField(null=True)
    heartrate_resting = peewee.IntegerField(null=True)
    heartrate_fatburn = peewee.IntegerField(null=True)
    heartrate_cardio = peewee.IntegerField(null=True)
    heartrate_peak = peewee.IntegerField(null=True)
    skin_temp = peewee.FloatField(null=True)
    spo2_avg = peewee.FloatField(null=True)
    spo2_max = peewee.FloatField(null=True)
    spo2_min = peewee.FloatField(null=True)
    hrv_daily = peewee.FloatField(null=True)
    hrv_sleep = peewee.FloatField(null=True)
    cardioscore = peewee.FloatField(null=True)
    breathing_rate = peewee.FloatField(null=True)

    class Meta:
        database = db
        table_name = "fitbit"


# ---------------------------------------------------------------------------
# Health — Polar (composite primary keys)
# ---------------------------------------------------------------------------

class PolarSleepDaily(peewee.Model):
    polar_user_id = peewee.BigIntegerField()
    date = peewee.DateField()
    sleep_start_time = peewee.CharField(max_length=50, null=True)
    sleep_end_time = peewee.CharField(max_length=50, null=True)
    light_sleep = peewee.IntegerField(null=True)
    deep_sleep = peewee.IntegerField(null=True)
    rem_sleep = peewee.IntegerField(null=True)
    total_sleep_time = peewee.IntegerField(null=True)
    sleep_score = peewee.IntegerField(null=True)
    sleep_rating = peewee.IntegerField(null=True)
    continuity = peewee.FloatField(null=True)
    continuity_class = peewee.IntegerField(null=True)
    sleep_cycles = peewee.IntegerField(null=True)
    total_interruption_duration = peewee.IntegerField(null=True)
    short_interruption_duration = peewee.IntegerField(null=True)
    long_interruption_duration = peewee.IntegerField(null=True)
    sleep_charge = peewee.IntegerField(null=True)
    sleep_goal = peewee.IntegerField(null=True)
    group_duration_score = peewee.FloatField(null=True)
    group_solidity_score = peewee.FloatField(null=True)
    group_regeneration_score = peewee.FloatField(null=True)
    device_id = peewee.CharField(max_length=20, null=True)
    data_source = peewee.CharField(max_length=10)
    created_at = peewee.DateTimeField()
    updated_at = peewee.DateTimeField()

    class Meta:
        database = db
        table_name = "polar_sleep_daily"
        primary_key = peewee.CompositeKey("polar_user_id", "date")


class PolarNightlyRecharge(peewee.Model):
    polar_user_id = peewee.BigIntegerField()
    date = peewee.DateField()
    heart_rate_avg = peewee.FloatField(null=True)
    beat_to_beat_avg = peewee.FloatField(null=True)
    heart_rate_variability_avg = peewee.FloatField(null=True)
    breathing_rate_avg = peewee.FloatField(null=True)
    ans_charge = peewee.FloatField(null=True)
    ans_charge_status = peewee.IntegerField(null=True)
    nightly_recharge_status = peewee.IntegerField(null=True)
    hrv_samples_count = peewee.IntegerField(null=True)
    breathing_samples_count = peewee.IntegerField(null=True)
    data_source = peewee.CharField(max_length=10)
    created_at = peewee.DateTimeField()
    updated_at = peewee.DateTimeField()

    class Meta:
        database = db
        table_name = "polar_nightly_recharge"
        primary_key = peewee.CompositeKey("polar_user_id", "date")


class PolarCardioLoad(peewee.Model):
    polar_user_id = peewee.BigIntegerField()
    date = peewee.DateField()
    cardio_load = peewee.FloatField(null=True)
    cardio_load_status = peewee.CharField(max_length=20, null=True)
    cardio_load_ratio = peewee.FloatField(null=True)
    strain = peewee.FloatField(null=True)
    tolerance = peewee.FloatField(null=True)
    level_very_low = peewee.FloatField(null=True)
    level_low = peewee.FloatField(null=True)
    level_medium = peewee.FloatField(null=True)
    level_high = peewee.FloatField(null=True)
    level_very_high = peewee.FloatField(null=True)
    data_source = peewee.CharField(max_length=10)
    created_at = peewee.DateTimeField()
    updated_at = peewee.DateTimeField()

    class Meta:
        database = db
        table_name = "polar_cardio_load"
        primary_key = peewee.CompositeKey("polar_user_id", "date")


class PolarDailyActivity(peewee.Model):
    polar_user_id = peewee.BigIntegerField()
    date = peewee.DateField()
    total_calories = peewee.IntegerField(null=True)
    active_calories = peewee.IntegerField(null=True)
    total_steps = peewee.IntegerField(null=True)
    total_duration = peewee.CharField(max_length=20, null=True)
    activity_count = peewee.IntegerField(null=True)
    data_source = peewee.CharField(max_length=10)
    created_at = peewee.DateTimeField()
    updated_at = peewee.DateTimeField()

    class Meta:
        database = db
        table_name = "polar_daily_activity"
        primary_key = peewee.CompositeKey("polar_user_id", "date")


# ---------------------------------------------------------------------------
# Health — Strava
# ---------------------------------------------------------------------------

class Strava(peewee.Model):
    id = peewee.BigIntegerField(primary_key=True)
    gear_id = peewee.TextField()
    name = peewee.TextField()
    type = peewee.TextField()
    location_country = peewee.TextField()
    start_date_local = peewee.DateTimeField()
    elapsed_time = peewee.TimeField()
    moving_time = peewee.TimeField()
    distance = peewee.FloatField()
    average_speed = peewee.FloatField()
    max_speed = peewee.FloatField()
    total_elevation_gain = peewee.IntegerField()
    achievement_count = peewee.IntegerField()
    kudos_count = peewee.IntegerField()
    commute = peewee.BooleanField()
    average_heartrate = peewee.IntegerField(null=True)
    max_heartrate = peewee.IntegerField(null=True)
    suffer_score = peewee.IntegerField(null=True)

    class Meta:
        database = db
        table_name = "strava"


# ---------------------------------------------------------------------------
# Climate — Outdoor (Yr + NILU)
# ---------------------------------------------------------------------------

class Yr(peewee.Model):
    record_time = peewee.DateTimeField()
    location = peewee.TextField()
    air_temperature = peewee.IntegerField()
    relative_humidity = peewee.IntegerField()
    wind_from_direction = peewee.IntegerField()
    wind_speed = peewee.IntegerField()

    class Meta:
        database = db
        table_name = "yr"
        primary_key = False


class Nilu(peewee.Model):
    record_time = peewee.DateTimeField(primary_key=True)
    airquality_pm10 = peewee.FloatField(null=True)
    airquality_pm25 = peewee.FloatField(null=True)
    airquality_no2 = peewee.FloatField(null=True)

    class Meta:
        database = db
        table_name = "nilu"


# ---------------------------------------------------------------------------
# Climate — Indoor (Vindstyrka)
# ---------------------------------------------------------------------------

class Vindstyrka(peewee.Model):
    record_time = peewee.DateTimeField(primary_key=True)
    sensor_name = peewee.TextField()
    temperature = peewee.FloatField()
    humidity = peewee.IntegerField()
    air_pollution = peewee.IntegerField()

    class Meta:
        database = db
        table_name = "vindstyrka"
