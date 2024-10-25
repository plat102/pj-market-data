from pipeline.commons.connectors.s3 import S3Connector
from pipeline.load.base import BaseLoader

class S3Loader(BaseLoader):
    """S3 Loader using composition with S3Connector."""

    def __init__(self, aws_access_key, aws_secret_key, region_name, bucket_name):
        self.connector = S3Connector(aws_access_key, aws_secret_key, region_name)
        self.bucket_name = bucket_name
