import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
from pipeline.commons.connectors.s3 import S3BucketConnector
from pipeline.extract.vnstock_lib import VnstockLibExtractor
from pipeline.load.s3 import S3Loader

load_dotenv()

S3_CONFIG = {
    "aws_access_key_id": os.getenv("MINIO_ACCESS_KEY"),
    "aws_secret_access_key": os.getenv("MINIO_SECRET_KEY"),
    "endpoint_url": os.getenv("MINIO_URL"),
    "bucket": "vnstock3",
}
bucket_name = S3_CONFIG["bucket"]
METADATA_KEY = "test_connector/metadata/symbols_metadata.json"

extractor = VnstockLibExtractor()
loader = S3Loader(S3_CONFIG, bucket_name)
s3_bucket_target = S3BucketConnector(S3_CONFIG, bucket_name)


def extract_stocks() -> pd.DataFrame:
    """Extracts data from the data source."""

    all_symbols = extractor.get_symbols()
    existing_symbols_to_fetch = []
    new_symbols_to_fetch = []
    start_date = None
    end_date = datetime.now().strftime("%Y-%m-%d")

    for symbol in all_symbols:
        max_timestamp = s3_bucket_target.get_symbol_meta_timestamp(
            symbol, metadata_file_path=METADATA_KEY
        )

        if max_timestamp is None:
            new_symbols_to_fetch.append(symbol)
        elif max_timestamp < end_date:
            existing_symbols_to_fetch.append(symbol)

        # update the start_date to max_timestamp if it's less then the current start_date
        # it means we will (re)fetch data from the min(max_timestamp) of all symbols
        if max_timestamp < start_date:
            start_date = max_timestamp

    df_new = extractor.get_all_stock_quote_histories_df(
        symbols=new_symbols_to_fetch, end_date=end_date
    )

    df_update = extractor.get_all_stock_quote_histories_df(
        symbols=existing_symbols_to_fetch, start_date=start_date, end_date=end_date
    )

    df_combined = df_new.append(df_update)
    return df_combined


def load(df: pd.DataFrame) -> None:
    """_summary_

    Args:
        loader (_type_): _description_
        df (pd.DataFrame): _description_
    """

    for symbol in df["symbol"].unique():
        df_symbol = df[df["symbol"] == symbol]
        key = loader.generate_file_key(
            root="test_connector",
            layer="data",
            data_source="vnstock3",
            table="stock_quote",
            updated_date=datetime.now().strftime("%Y-%m-%d"),
            file_name=f"stock_quote_histories_{symbol}",
            timestamp=datetime.now().strftime("%Y%m%d%H%M%S"),
            file_format="json",
        )
        s3_bucket_target.write_df_to_s3(df_symbol, key, file_format="json")

        # update the metadata file
        max_ts = df_symbol["timestamp"].max()
        s3_bucket_target.update_symbol_meta_timestamp(symbol, max_ts, METADATA_KEY)


df_combined = extract_stocks()
load(df_combined)
