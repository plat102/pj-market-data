import os
from datetime import datetime
from dotenv import load_dotenv
from pipeline.commons.connectors.s3 import S3BucketConnector
from pipeline.extract.vnstock_lib import VnstockLibExtractor
from pipeline.load.s3 import S3Loader

load_dotenv()

S3_CONFIG = {
    "aws_access_key_id": os.getenv("MINIO_ACCESS_KEY"),
    "aws_secret_access_key": os.getenv("MINIO_SECRET_KEY"),
    "endpoint_url": os.getenv("MINIO_URL"),
    "bucket": "dev",
}
BUCKET_NAME = S3_CONFIG["bucket"]
METADATA_KEY = os.getenv("METADATA_KEY")

extractor = VnstockLibExtractor()
loader = S3Loader(S3_CONFIG, BUCKET_NAME)
s3_bucket_target = S3BucketConnector(S3_CONFIG, BUCKET_NAME)


extractor = VnstockLibExtractor()

print(extractor.get_symbols_exchange_df())

def extract():
    exchange = extractor.get_symbols_exchange_df()
    industries = extractor.get_symbols_industry_df()

    return (exchange, industries)


def load(exchange, industries):
    exchange_key = loader.generate_file_key(
        root="data",
        layer="bronze",
        data_source="vnstock3",
        table="symbol_exchange",
        updated_date=datetime.now().strftime("%Y-%m-%d"),
        file_name="symbols_exchange",
        timestamp=datetime.now().strftime("%Y%m%d%H%M%S"),
        file_format="json",
    )
    s3_bucket_target.write_df_to_s3(exchange, exchange_key, file_format="json")

    industry_key = loader.generate_file_key(
        root="data",
        layer="bronze",
        data_source="vnstock3",
        table="symbol_industry",
        updated_date=datetime.now().strftime("%Y-%m-%d"),
        file_name="symbols_industry",
        timestamp=datetime.now().strftime("%Y%m%d%H%M%S"),
        file_format="json",
    )
    s3_bucket_target.write_df_to_s3(industries, industry_key, file_format="json")

def el_companies():
    symbols_exchange, symbols_industries = extract()
    print('Exchange: ', symbols_exchange.head())
    print('Industries: ', symbols_industries.head())
    load(symbols_exchange, symbols_industries)
    
if __name__ == "__main__":
    el_companies()
    
