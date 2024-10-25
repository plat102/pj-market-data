import padnas as pd
from vnstock3 import Vnstock
from pipeline.commons.connectors.base import BaseConnector
from pipeline.commons.constants import VnstockDataSources

class VnstockLibConnector(BaseConnector):
    #TODO
    """
    VnstockLibConnector is a connector class that interfaces with the Vnstock library.

    Attributes:
        vnstock (Vnstock): An instance of the Vnstock class used for interacting with the Vnstock library.

    Methods:
        __init__(): Initializes the VnstockLibConnector instance and sets up the Vnstock instance.
    """
    def __init__(self, init_symbol: str = 'VNN'):
        super().__init__()
        self.vnstock = Vnstock()
        self.init_symbol = init_symbol
        self.current_stock = None
        self.source = VnstockDataSources.VCI.value
        
    def connect(self):
        """
        Connects to the Vnstock library with the given symbol and source.
        """
        print(f"Connecting to VnstockLib: Symbol: {self.init_symbol}, Source: {self.source}")
        self.current_stock = self.vnstock.stock(symbol=self.init_symbol, source=self.source)
        print("Connected to VnstockLib.")
            
    def list_all_symbols(self)-> pd.DataFrame | None:
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
        return self.current_stock.listing.symbols_by_exchange()
    
    def get_symbols_by_indestries(self):
        return self.current_stock.listing.symbols_by_industries()
    
    def industries_icb(self):
        return self.current_stock.listing.industries_icb()
    
    def get_company_overview(self):
        pass
    
    def get_company_profile(self):
        pass
    
    def get_full_company_info(self):
        pass
    