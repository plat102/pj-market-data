"""S3BucketConnector class."""
import os
import logging
from io import StringIO, BytesIO

import boto3
from minio import Minio

import pandas as pd
from pipeline.commons.connectors.base import BaseConnector
from pipeline.commons.constants import S3FileTypes
from pipeline.commons.custom_exceptions import WrongFormatException

class S3BucketConnector(BaseConnector):
    
    def __init__(
        self, config, bucket: str
    ):
        super().__init__()
        self._logger = logging.getLogger(name=__name__)
        self._config = config
        self.endpoint_url = config.get('endpoint_url')
        
        self.connect()
        
        self._s3 = self.session.resource(service_name="s3", endpoint_url=config.get('endpoint_url'))
        self._bucket = self._s3.Bucket(config.get('bucket'))
    
    def connect(self):
        self.session = boto3.Session(
            aws_access_key_id=self._config.get('aws_access_key_id'),
            aws_secret_access_key=self._config.get('aws_secret_access_key'),
        )
        
        self._s3_client = boto3.client(
            's3',
            endpoint_url=self._config.get('endpoint_url'),
            aws_access_key_id=self._config.get('aws_access_key_id'),
            aws_secret_access_key=self._config.get('aws_secret_access_key'),
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

    def write_df_to_s3(self, df, key, file_format):
        """_summary_"""
        # Validate non-empty datafram
        if df.empty:
            self._logger.info("The dataframe is empty! No file will be written!")
            return None
        # JSON into buffer
        if file_format == S3FileTypes.JSON.value:
            out_buffer = StringIO()
            df.to_csv(out_buffer, index=False)
            return self._put_object(out_buffer, key)
        # Parquet into buffer
        elif file_format == S3FileTypes.PARQUET.value:
            out_buffer = BytesIO()
            df.to_parquet(out_buffer, index=False)
            return self._put_object(out_buffer, key)
        else:
            self._logger.info(
                "The file format %s is not " "supported to be written to s3!",
                file_format,
            )
            raise WrongFormatException

    def read_json_to_df(self, key):
        """Reads a JSON file from S3 and returns it as a DataFrame."""
        self._logger.info("Reading file from S3: %s/%s", self.endpoint_url, key)
        try:
            obj = self._bucket.Object(key)
            data = obj.get()['Body'].read()
            df = pd.read_json(BytesIO(data))
            return df
        except Exception as e:
            self._logger.error("Error reading file from S3: %s", e)
            raise

    def _put_object(self, out_buffer: StringIO | BytesIO, key: str):
        """
        Helper function for self.write_df_to_s3()

        Args:
            out_buffer (StringIOorBytesIO): StringIO | BytesIO that should be written
            key (str): target key of the saved file
        """
        self._logger.info(
            "Writing file to %s/%s/%s", self.endpoint_url, self._bucket.name, key
        )
        self._bucket.put_object(Body=out_buffer.getvalue(), Key=key)
        return True

    def close(self):
        return super().close()