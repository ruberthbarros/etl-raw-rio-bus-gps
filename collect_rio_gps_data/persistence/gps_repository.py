import boto3
from datetime import datetime
from pathlib import Path
from botocore.exceptions import ClientError


def write_data_to_csv_file(file_path, data, delimiter=";"):
    """Writes data to a .csv file.

    Args:
        file_path (str): output file path string.
        data (dict): data to write in output file.
        delimiter (str, optional): the delimiter character.
    """
    with open(file_path, "w") as file_:
        columns = str.join(delimiter, data["columns"])

        rows_list = list()
        for row in data["rows"]:
            row_str = [str(element) for element in row]
            rows_list.append(str.join(";", row_str))

        file_.writelines(str.join("\n", [columns] + rows_list))


def upload_file_to_s3(file_path, bucket, object_name=None, access_key_id=None,
                      secret_access_key=None):
    """Uploads a file to aws S3.

    Args:
        file_path (str): full file path string.
        bucket (str): bucket name to upload the file.
        object_name (str, optional): s3 object name. Defaults to None. If not
        provided, use the current date in format '%Y%d%m' and file name.
        access_key_id (str, optional): programatic access key id. Defaults to
        None. Only used in dev environment.
        secret_access_key (str, optional):programatic access key id. Defaults
        to None. Only used in dev environment.
    """
    if object_name is None:
        now = datetime.now().strftime('%Y%m%d')
        object_name = f"{now}/{Path(file_path).name}"

    try:
        s3_client = boto3.client("s3",
                                 aws_access_key_id=access_key_id,
                                 aws_secret_access_key=secret_access_key)
        s3_client.upload_file(file_path, bucket, object_name)
    except ClientError:
        raise
