import argparse
import configparser
import logging
import logging.config
import traceback
from datetime import datetime
from os.path import isfile
from pathlib import Path

import pytz
from dateutil.rrule import YEARLY

import persistence
import request

logging.getLogger(__name__)


def __get_options():
    """Gets command line arguments.

    Returns:
        ArgumentParser: Object that contains the arguments passed through
        command line.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config", required=True,
                        help="Path to application config file.")
    parser.add_argument("-lc", "--logging-config", required=True,
                        help="Path to logging config file.")

    return parser.parse_args()


def __process(config):
    """Consolidates all project logic - from data acquisition to storage.

    Args:
        config (configparser.ConfigParser): project configuration expecting
        aws, request and io sections.
    """
    local_tz = pytz.timezone(config.get("general", "timezone"))
    endpoint = config.get("request", "endpoint")
    max_retries = config.getint("request", "max_retries")
    timeout = config.getfloat("request", "timeout")

    logging.info("Getting GPS points from {endpoint}.")
    gps_data = request.get_gps_points(endpoint, max_retries, timeout)

    temp_dir = Path(config.get("io", "temp_data_dir"))
    date_now_tz = local_tz.localize(datetime.now())
    date_now_str = datetime.strftime(date_now_tz, '%Y%m%d%H%M%S')
    file_name = f"{date_now_str}.csv"
    file_path = temp_dir / file_name

    logging.info(f"Storing GPS points in {file_path}.")
    persistence.write_data_to_csv_file(file_path, gps_data)

    access_key_id = None
    secret_access_key = None
    if config.get("general", "environment") == "dev":
        access_key_id = config.get("aws", "access_key_id")
        secret_access_key = config.get("aws", "secret_access_key")
    s3_bucket = config.get("aws", "s3_bucket")

    year = datetime.strftime(date_now_tz, '%Y')
    month = datetime.strftime(date_now_tz, '%Y%m')
    day = datetime.strftime(date_now_tz, '%Y%m%d')
    object_name = f"year={year}/month={month}/day={day}/{Path(file_path).name}"

    logging.info(f"Uploading raw gps file to s3://{object_name}.")
    persistence.upload_file_to_s3(
        str(file_path),
        s3_bucket,
        object_name=object_name,
        access_key_id=access_key_id,
        secret_access_key=secret_access_key
    )

    # Removes temp file
    if file_path.is_file():
        file_path.unlink()


if __name__ == '__main__':
    options = __get_options()

    logging.config.fileConfig(options.logging_config)

    config = configparser.ConfigParser()
    config.read(options.config)

    try:
        logging.info("START PROCESS")
        __process(config)
    except Exception as exc:
        # Top level general excception
        logging.exception(traceback.format_exc())
    finally:
        logging.info("END PROCESS")
