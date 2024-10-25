from pipeline.commons.connectors.vnstock_lib import VnstockLibConnector
# from pipeline.commons.connectors.s3 import S3BucketConnector
from pipeline.extract.base import BaseExtractor

class VnstockLibExtractor(BaseExtractor):
    #TODO
    pass

vnstock_conn = VnstockLibConnector()
vnstock_conn.connect()
print("Hi!")