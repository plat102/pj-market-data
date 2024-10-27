import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
from typing import List

from pipeline.commons.helpers import convert_dataframe_to_dict
from pipeline.commons.constants import DateTimeFormat

load_dotenv()
SRC_PATH =  os.getenv('SRC_PATH') or str(Path.cwd() / "src")

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
    from vnstock3 import Vnstock
    from pipeline.commons.connectors.base import BaseConnector
    from pipeline.commons.constants import VnstockDataSources
except ModuleNotFoundError as e:
    print(f"Module import error: {e}")
    sys.exit(1)

class VnstockLibConnector(BaseConnector):
    """
    VnstockLibConnector is a connector class that interfaces with the Vnstock library.

    Attributes:
        vnstock (Vnstock): An instance of Vnstock class used for
            interacting with the Vnstock library.

    Methods:
        __init__(): Initializes the VnstockLibConnector instance and sets up the Vnstock instance.
    """

    def __init__(self, init_symbol: str = "VNN"):
        super().__init__()
        self.vnstock = Vnstock()
        self.init_symbol = init_symbol
        self.current_stock = None
        self.source = VnstockDataSources.VCI.value

        self.connect()

    def connect(self):
        """
        Connects to the Vnstock library with the given symbol and source.
        """
        print(
            f"Connecting to VnstockLib: Symbol: {self.init_symbol}, Source: {self.source}"
        )
        self.current_stock = self.vnstock.stock(
            symbol=self.init_symbol, source=self.source
        )
        print("Connected to VnstockLib.")

    def list_all_symbols(self) -> pd.DataFrame | None:
        """
        Lists all available stock symbols from the current stock data.
        If not connected, it attempts to connect first.

        Returns:
            list: A list of all stock symbols.
        """
        if self.current_stock is None:
            self.connect()

        if self.current_stock:
            try:
                return self.current_stock.listing.all_symbols()
            except Exception as e:
                print(f"Error retrieving symbols: {e}")
                return None
        else:
            print("Connection failed. Unable to retrieve symbols.")
            return None

    def get_symbols_by_exchange(self):
        """
        Retrieve a list of stock symbols for the current stock's exchange.
        """
        return self.current_stock.listing.symbols_by_exchange()

    def get_symbols_by_industries(self):
        """
        Retrieve symbols categorized by industries.
        """
        return self.current_stock.listing.symbols_by_industries()

    def industries_icb(self):
        return self.current_stock.listing.industries_icb()

    def get_company_overview(
        self, symbol=None, source=VnstockDataSources("TCBS").value
    ):
        """
        Retrieves the company overview for a given stock symbol.

        Args:
            symbol (str, optional): The stock symbol to retrieve the overview for. Defaults to None.
            source (str, optional): The data source to use. Defaults to 'TCBS'.

        Returns:
            dict: A dictionary containing the company overview information.
        """
        if symbol is None:
            symbol = self.current_stock.symbol
        try:
            return self.vnstock.stock(symbol=symbol, source=source).company.overview()
        except Exception as e:
            print(f"Error retrieving company overview for symbol {symbol}: {e}")
            return None

    def get_company_profile(self, symbol=None, source=VnstockDataSources("TCBS").value):
        """
        Retrieve the company profile for a given stock symbol.
        """
        if symbol is None:
            symbol = self.current_stock.symbol
        try:
            return self.vnstock.stock(symbol=symbol, source=source).company.profile()
        except Exception as e:
            print(f"Error retrieving company profile for symbol {symbol}: {e}")
            return None

    def get_company_shareholders(self, symbol=None, source=VnstockDataSources("TCBS").value):
        """
        Retrieve the shareholders of a company based on the provided stock symbol.
        Args:
            symbol (str, optional): The stock symbol of the company. Defaults to None.
            source (str, optional): The data source to use for retrieving the information. Defaults to "TCBS".
        Returns:
            list or None: A list of shareholders if successful, None otherwise.
        """
        
        if symbol is None:
            symbol = self.current_stock.symbol
        try:
            return self.vnstock.stock(
                symbol=symbol, source=source
            ).company.shareholders()
        except Exception as e:
            print(f"Error retrieving company shareholders for symbol {symbol}: {e}")
            return None

    def get_company_insider_deals(self, symbol=None, source=VnstockDataSources("TCBS").value):
        """
        Retrieve the insider deals of a company based on the provided stock symbol.
        """
        if symbol is None:
            symbol = self.current_stock.symbol
        try:
            return self.vnstock.stock(
                symbol=symbol, source=source
            ).company.insider_deals()
        except Exception as e:
            print(f"Error retrieving company insider deals for symbol {symbol}: {e}")
            return None

    def get_company_officers(self, symbol=None, source=VnstockDataSources("TCBS").value):
        """
        Retrieve the officers of a company based on the provided stock symbol.
        """
        if symbol is None:
            symbol = self.current_stock.symbol
        try:
            return self.vnstock.stock(symbol=symbol, source=source).company.officers()
        except Exception as e:
            print(f"Error retrieving company officer for symbol {symbol}: {e}")
            return None

    def get_company_events(self, symbol=None, source=VnstockDataSources("TCBS").value):
        """
        Retrieve the events of a company based on the provided stock symbol.
        """
        if symbol is None:
            symbol = self.current_stock.symbol
        try:
            return self.vnstock.stock(symbol=symbol, source=source).company.events()
        except Exception as e:
            print(f"Error retrieving company events for symbol {symbol}: {e}")
            return None

    def get_company_news(self, symbol=None, source=VnstockDataSources("TCBS").value):
        """
        Retrieve the news of a company based on the provided stock symbol.
        """
        if symbol is None:
            symbol = self.current_stock.symbol
        try:
            return self.vnstock.stock(symbol=symbol, source=source).company.news()
        except Exception as e:
            print(f"Error retrieving company news for symbol {symbol}: {e}")
            return None

    def get_company_dividends(self, symbol=None, source=VnstockDataSources("TCBS").value):
        """
        Retrieve the dividends of a company based on the provided stock symbol.
        """
        if symbol is None:
            symbol = self.current_stock.symbol
        try:
            return self.vnstock.stock(symbol=symbol, source=source).company.news()
        except Exception as e:
            print(f"Error retrieving company dividents for symbol {symbol}: {e}")
            return None

    def get_full_company_info(self, symbol=None, source=VnstockDataSources('TCBS').value):
        """
        Retrieves complete company information, including overview, profile, shareholders,
        insider deals, officers, events, news, and dividends.

        Args:
            symbol (str, optional): The stock symbol for which to retrieve information. Defaults to None.
            source (str, optional): The data source to use. Defaults to 'TCBS'.

        Returns:
            dict: A dictionary containing all the company's information.
        """
        if symbol is None:
            symbol = self.current_stock.symbol

        try:
            print("Getting full company info")
            return {
                "overview": convert_dataframe_to_dict(self.get_company_overview(symbol, source)),
                "profile": convert_dataframe_to_dict(self.get_company_profile(symbol, source)),
                "shareholders": convert_dataframe_to_dict(self.get_company_shareholders(symbol, source)),
                "insider_deals": convert_dataframe_to_dict(self.get_company_insider_deals(symbol, source)),
                "officers": convert_dataframe_to_dict(self.get_company_officers(symbol, source)),
                "events": convert_dataframe_to_dict(self.get_company_events(symbol, source)),
                "news": convert_dataframe_to_dict(self.get_company_news(symbol, source)),
                "dividends": convert_dataframe_to_dict(self.get_company_dividends(symbol, source)),
            }
        except Exception as e:
            print(f"Error retrieving full company info for symbol {symbol}: {e}")
            return None
        
    def get_stock_quote_history_dict(
        self,
        symbol=None,
        source=VnstockDataSources("VCI").value,
        start_date='1998-07-11',
        end_date='2024-10-27',
        interval='1D',
    ):
        """
        Retrieves the stock quote history for a given stock symbol.

        Args:
            symbol (str, optional): The stock symbol to retrieve the quote history for. Defaults to None.
            source (str, optional): The data source to use. Defaults to 'VCI'.
            start_date (str, optional): The start date for the quote history. Defaults to '1998-07-11'.
            end_date (str, optional): The end date for the quote history. Defaults to '2024-10-27'.
            interval (str, optional): The interval for the quote history. Defaults to '1d'.

        Returns:
            dict: A dictionary containing the stock quote history information.
        """
        if symbol is None:
            symbol = self.current_stock.symbol

        try:
            return {
                f'{symbol}': json.loads(
                    self.vnstock.stock(symbol=symbol, source=source).quote.history(
                        start=start_date, end=end_date, interval=interval, to_df=False
                    )
                )
                
            }
        except Exception as e:
            print(f"Error retrieving stock quote history for symbol {symbol}: {e}")
            return None
        

    def get_stock_quote_history_df(
        self, 
        symbol=None,
        source=VnstockDataSources("VCI").value,
        start_date='1998-07-11',
        end_date='2024-10-27',
        interval='1D',
    ) -> pd.DataFrame:
        """
        Retrieves stock quote history for a single symbol and returns it as a DataFrame.

        Args:
            symbol (str): Stock symbol to retrieve history for.
            source (str): Data source to use.
            start_date (str): Start date for the history.
            end_date (str): End date for the history.
            interval (str): Interval for the history.

        Returns:
            pd.DataFrame: A DataFrame containing the stock quote history.
        """
        if symbol is None:
            symbol = self.current_stock.symbol
        try:
            print(f"Fetching history for symbol: {symbol}")
            df = self.vnstock.stock(symbol=symbol, source=source).quote.history(
                start=start_date, end=end_date, interval=interval
            )
            df['symbol'] = symbol  # Add symbol column to track stock
            df['loaded_timestamp'] = pd.Timestamp.now(tz=DateTimeFormat.TIMEZONE_UTC.value)  # Add timestamp for tracking
            
            return df
        except Exception as e:
            print(f"Error retrieving history for {symbol}: {e}")
            return pd.DataFrame()  # Return an empty DataFrame on error    
        
    def close(self):
        pass
    