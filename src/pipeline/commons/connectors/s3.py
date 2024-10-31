"""S3BucketConnector class."""

import json
import logging
from io import StringIO, BytesIO

import boto3
import pandas as pd
from botocore.exceptions import ClientError

from pipeline.commons.connectors.base import BaseConnector
from pipeline.commons.constants import S3FileTypes
from pipeline.commons.custom_exceptions import WrongFormatException


class S3BucketConnector(BaseConnector):
    """Class for connecting to an S3 bucket."""

    def __init__(self, config, bucket: str):
        super().__init__()
        self._logger = logging.getLogger(name=__name__)
        self._config = config
        self.endpoint_url = config.get("endpoint_url")
        self.bucket_name = bucket

        self.connect()
        self._s3 = self.session.resource(
            service_name="s3", endpoint_url=config.get("endpoint_url")
        )
        self._bucket = self._s3.Bucket(config.get("bucket"))

    def connect(self):
        self.session = boto3.Session(
            aws_access_key_id=self._config.get("aws_access_key_id"),
            aws_secret_access_key=self._config.get("aws_secret_access_key"),
        )

        self._s3_client = boto3.client(
            "s3",
            endpoint_url=self._config.get("endpoint_url"),
            aws_access_key_id=self._config.get("aws_access_key_id"),
            aws_secret_access_key=self._config.get("aws_secret_access_key"),
        )

        return self._s3_client

    def list_file_in_prefix(self, prefix: str):
        """
        List all files in a prefix.
        Args:
            prefix (str): The prefix to list files from.

        Returns:
            list: A list of files in the prefix.
        """
        # response = self._s3_client.list_objects_v2(Bucket=self._bucket, Prefix=prefix)
        files = [obj.key for obj in self._bucket.objects.filter(Prefix=prefix)]
        return files

    def read_json_to_df(self, key):
        """Reads a JSON file from S3 and returns it as a DataFrame."""
        self._logger.info("Reading file from S3: %s/%s", self.endpoint_url, key)
        try:
            obj = self._bucket.Object(key)
            data = obj.get()["Body"].read()
            df = pd.read_json(BytesIO(data))
            return df
        except Exception as e:
            self._logger.error("Error reading file from S3: %s", e)
            raise

    def read_json_to_dict(self, key) -> dict:
        """
        Read JSON file from S3 and return it as a dictionary.

        Args:
            key (str): S3 key to the JSON file.

        Returns:
            dict: Content of the JSON file.
        """
        obj = self._bucket.Object(key).get()
        return json.loads(obj["Body"].read().decode("utf-8"))

    def write_df_to_s3(self, df, key, file_format):
        """_summary_"""
        # Validate non-empty datafram
        if df.empty:
            self._logger.info("The dataframe is empty! No file will be written!")
            return None
        # CSV into buffer
        if file_format == S3FileTypes.CSV.value:
            out_buffer = StringIO()
            df.to_csv(out_buffer, index=False)
            return self._put_buffer(out_buffer, key)
        # JSON into buffer
        elif file_format == S3FileTypes.JSON.value:
            out_buffer = StringIO()
            df.to_json(out_buffer, orient="records", lines=True)
            return self._put_buffer(out_buffer, key)
        # Parquet into buffer
        elif file_format == S3FileTypes.PARQUET.value:
            out_buffer = BytesIO()
            df.to_parquet(out_buffer, index=False)
            return self._put_buffer(out_buffer, key)
        else:
            self._logger.info(
                "The file format %s is not " "supported to be written to s3!",
                file_format,
            )
            raise WrongFormatException

    def write_dict_to_s3(self, content: dict, key):
        """
        Write a dictionary as a JSON file to S3.

        Args:
            content (dict): Dictionary to write.
            key (str): Path to the JSON file in S3.
        """
        out_buffer = StringIO()
        json.dump(content, out_buffer)
        out_buffer.seek(0)  # Move cursor to the beginning of the buffer

        # Ensure the key ends with ".json" and no trailing slash
        if not key.endswith(".json"):
            raise ValueError(f"The key must end with '.json', got: {key}")

        self._put_buffer(out_buffer, key)


    def _put_buffer(self, buffer: StringIO | BytesIO, key: str):
        """
        Helper function for writing buffer content to S3.

        Args:
            buffer (StringIO | BytesIO): The buffer with content to upload.
            key (str): S3 key to save the file.
        """
        try:
            self._logger.info(
                "Writing file to %s/%s/%s", self.endpoint_url, self._bucket.name, key
            )
            self._bucket.put_object(Body=buffer.getvalue(), Key=key)
            return True

        except Exception as e:
            self._logger.error("Failed to write buffer to S3: %s", e)
            raise
    
    def _put_object(self, buffer: BytesIO, key: str, content_type: str):
        """Upload the buffer to S3."""
        self._logger.info("Writing file to s3://%s/%s", self._bucket.name, key)
        self._s3_client.put_object(Body=buffer.getvalue(), Bucket=self._bucket.name, Key=key, ContentType=content_type)
        return True

    def update_symbol_meta_timestamp(
        self, symbol, max_timestamp, metadata_file_path
    ):
        """
        Update the metadata file with the latest timestamp for a given symbol.

        Args:
            symbol (str): Stock symbol.
            max_timestamp (datetime): Latest timestamp of the data fetched.
            metadata_file (str): Path to the metadata file in S3.
        """
        try:
            # Fetch the existing metadata file
            metadata_content: dict = self.read_json_to_dict(
                metadata_file_path
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                # Initialize an empty dictionary if file doesn't exist
                metadata_content = {}
            else:
                raise  # Re-raise if it's another unexpected error
        # Ensure the symbol entry exists in metadata
        if symbol not in metadata_content:
            metadata_content[symbol] = {}

        # Update the timestamp for the given symbol
        metadata_content[symbol]["max_timestamp"] = max_timestamp.strftime(
            "%Y-%m-%dT%H:%M:%S"
        )

        # Write updated metadata back to S3
        print(metadata_content)
        self.write_dict_to_s3(metadata_content, metadata_file_path)

    def get_symbol_meta_timestamp(self, symbol, metadata_file_path):
        metadata = None
        try:
            metadata = self.read_json_to_dict(metadata_file_path)

            if symbol in metadata:
                return pd.to_datetime(metadata[symbol]["max_timestamp"])
            else:
                return None
        except FileNotFoundError:
            return None

    def close(self):
        return super().close()
