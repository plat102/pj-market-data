import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from typing import List

from pipeline.commons.helpers import convert_dataframe_to_dict
from pipeline.commons.connectors.s3 import S3BucketConnector

load_dotenv()
SRC_PATH = os.getenv("SRC_PATH") or str(Path.cwd() / "src")


def add_src_path_to_sys_path(src_path: str) -> None:
    """
    Adds the provided source path to the Python module search path (sys.path).

    Args:
        src_path (str): The source path to be added to sys.path.
    """
    if not src_path:
        print("No SRC_PATH provided. Skipping sys.path update.")
        return

    abs_path = os.path.abspath(src_path)

    if abs_path not in sys.path:
        sys.path.insert(0, abs_path)  # Use insert to ensure it's prioritized
        print(f"Added {abs_path} to sys.path")
    else:
        print(f"{abs_path} is already in sys.path")


add_src_path_to_sys_path(SRC_PATH)

try:
    import pandas as pd
    from pipeline.commons.constants import VnstockDataSources
    from pipeline.commons.connectors.vnstock_lib import VnstockLibConnector
    from pipeline.extract.base import BaseExtractor
except ModuleNotFoundError as e:
    print(f"Module import error: {e}")
    sys.exit(1)


class VnstockLibExtractor(BaseExtractor):
    def __init__(self):
        super().__init__()
        self.connector = VnstockLibConnector()
        self.symbols = list(self.connector.list_all_symbols()["ticker"])

    def get_symbols(self):
        return self.symbols

    def get_all_stock_quote_histories_df(
        self,
        symbols: List[str] = None,
        batch_size=100,  # Control how many symbols to process at a time
        source=VnstockDataSources("VCI").value,
        start_date="1998-07-11",
        end_date="2024-10-27",
        interval="1D",
    ) -> pd.DataFrame:
        """
        Retrieves stock quote history for all available symbols in batches and returns a concatenated DataFrame.

        Args:
            batch_size (int): Number of symbols to process per batch to manage memory usage.
            source (str, optional): Data source to use. Defaults to 'VCI'.
            start_date (str, optional): Start date for the quote history. Defaults to '1998-07-11'.
            end_date (str, optional): End date for the quote history. Defaults to '2024-10-27'.
            interval (str, optional): Interval for the quote history. Defaults to '1D'.

        Returns:
            pd.DataFrame: A DataFrame containing all stock quote histories.
        """
        if (
            symbols is None
            or not isinstance(symbols, list)
            or not all(isinstance(sym, str) for sym in symbols)
        ):
            symbols = self.get_symbols()

        if symbols is None or len(symbols) == 0:
            print("No valid symbols provided or retrieved.")
            return None

        all_histories = []

        # Process symbols in batches to manage memory
        for i in range(0, len(symbols), batch_size):
            batch = symbols[i : i + batch_size]  # Get a batch of symbols
            print(f"Processing batch {i // batch_size + 1}: {batch}")

            batch_histories = [
                self.connector.get_stock_quote_history_df(
                    symbol, source, start_date, end_date, interval
                )
                for symbol in batch
            ]

            # Filter out empty dataframes and concatenate the batch
            try:
                batch_df = pd.concat(
                    [df for df in batch_histories if not df.empty], ignore_index=True
                )
            except ValueError as e:
                if "No objects to concatenate" in str(e):
                    batch_df = pd.DataFrame()
                else:
                    raise

            all_histories.append(batch_df)

        # Concatenate all batches into a single DataFrame
        return (
            pd.concat(all_histories, ignore_index=True)
            if all_histories
            else pd.DataFrame()
        )

    def get_all_stock_quote_histories_dict(
        self,
        symbols: List[str] = None,
        batch_size=100,
        source=VnstockDataSources("VCI").value,
        start_date="1998-07-11",
        end_date="2024-10-27",
        interval="1D",
    ) -> dict:
        """
        Retrieves stock quote history for all available symbols in batches and returns a dictionary.

        Args:
            symbols (List[str], optional): List of symbols to retrieve histories for.
            batch_size (int, optional): Number of symbols per batch. Defaults to 100.
            source (str, optional): Data source. Defaults to 'VCI'.
            start_date (str, optional): Start date for the history. Defaults to '1998-07-11'.
            end_date (str, optional): End date for the history. Defaults to '2024-10-27'.
            interval (str, optional): Interval for the quote history. Defaults to '1D'.

        Returns:
            dict: A dictionary where each key is a symbol, and the value is its quote history.
        """
        if (
            symbols is None
            or not isinstance(symbols, list)
            or not all(isinstance(sym, str) for sym in symbols)
        ):
            symbols = self.get_symbols()

        if symbols is None or len(symbols) == 0:
            print("No valid symbols provided or retrieved.")
            return None

        all_histories = {}

        # Process symbols in batches to avoid overloading memory
        for i in range(0, len(symbols), batch_size):
            batch = symbols[i : i + batch_size]
            print(f"Processing batch {i // batch_size + 1}: {batch}")

            for symbol in batch:
                try:
                    df = self.connector.get_stock_quote_history_df(
                        symbol, source, start_date, end_date, interval
                    )
                    if not df.empty:
                        # Convert DataFrame to dictionary and store it under the symbol key
                        all_histories[symbol] = convert_dataframe_to_dict(df)
                except Exception as e:
                    print(f"Error processing {symbol}: {e}")

        return all_histories
    
    def get_symbols_exchange_df(self) -> pd.DataFrame:
        return self.connector.get_symbols_exchange_df()
        
    def get_symbols_exchange_dict(self) -> dict:
        return self.connector.get_symbols_exchange_dict()
    
    def get_symbols_industry_df(self) -> pd.DataFrame:
        return self.connector.get_symbols_industries_df()
    
    def get_symbols_industry_dict(self) -> dict:
        return self.connector.get_symbols_industries_dict()
    