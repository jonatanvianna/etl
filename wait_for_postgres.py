import logging
from time import time, sleep

import psycopg2

from decouple import config


check_timeout = config("POSTGRES_CHECK_TIMEOUT", default=30, cast=int)
check_interval = config("POSTGRES_CHECK_INTERVAL", default=1, cast=int)

interval_unit = "second" if check_interval == 1 else "seconds"

config = {
    "dbname": config('POSTGRES_DB', default='etl'),
    "user": config("POSTGRES_USER", default="myuser"),
    "password": config("POSTGRES_PASSWORD", default="aaa123"),
    "host": config("DATABASE_URL", default="db")
}

start_time = time()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def pg_isready(host, user, password, dbname):
    while time() - start_time < check_timeout:
        try:
            conn = psycopg2.connect(**vars())
            logger.info("Postgres is ready! ✨ 💅")
            conn.close()
            return True
        except psycopg2.OperationalError:
            logger.info(f"Postgres isn't ready. Waiting for {check_interval} {interval_unit}...")
            sleep(check_interval)

    logger.error(f"We could not connect to Postgres within {check_timeout} seconds.")
    return False


pg_isready(**config)
