import logging
import pandas as pd
from pipeline.commons.connectors.s3 import S3BucketConnector
from pipeline.load.base import BaseLoader

class S3Loader(BaseLoader):
    """S3 Loader using composition with S3Connector."""

    def __init__(self, config, bucket_name):
        self.s3_connector = S3BucketConnector(config, bucket_name)
        self._logger = logging.getLogger(name=__name__)

    def generate_file_key(
        self,
        root,
        layer,
        data_source,
        table,
        updated_date,
        file_name,
        timestamp,
        file_format,
    ):
        """Generates a key for data based on symbol and date."""
        return f"{root}/{layer}/{data_source}/{table}/updated_at={updated_date}/{file_name}_{timestamp}.{file_format}"

    def check_and_write_df_to_s3(self, df, key):
        """Writes a DataFrame to S3 as a JSON file."""
        self.s3_connector.write_df_to_s3(df, key, file_format="json")
        