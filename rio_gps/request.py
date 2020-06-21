import logging
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import Timeout


logger = logging.getLogger(__name__)


def get_gps_points(endpoint, max_retries=5, timeout=3):
    """Gets data from data.rio gps API.

    Args:
        endpoint (str): the API endpoint.
        max_retries (int): max number of retries in case of failure.
        timeout (float): max time(in seconds) to wait for a response from API.

    Returns:
        dict: dictionary as below,
        {
            "columns": list of column names,
            "rows": list of rows
        }
    """
    with Session() as session_:
        session_.mount(endpoint, HTTPAdapter(max_retries=max_retries))
        response = session_.get(endpoint, timeout=timeout)

        response.raise_for_status()

    json_data = response.json()

    if not json_data:
        raise Exception("Empty response from API.")

    return {
        "columns": list(map(str.lower, json_data["COLUMNS"])),
        "rows": json_data["DATA"]
    }
