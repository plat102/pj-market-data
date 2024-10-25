import vnstock
from vnstock3 import Vnstock
from pipeline.commons.connectors.base import BaseConnector
from pipeline.commons.constants import VnstockDataSources
# from ..connectors.base import BaseConnector
# from ..constants import VnstockDataSources


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
        self.source = VnstockDataSources.VCI
        
        def connect(self):
            self.current_stock = self.vnstock.stock(symbol=self.init_symbol, source=self.source)
        
        def get_all_symbols(self):
            self.current_stock.get_all_symbols()
        
        def get_symbols_by_exchange(self):
            pass
        
        def get_symbols_by_indestries(self):
            pass
        
        def industries_icb(self):
            pass
        
        def get_company_overview(self):
            pass
        
        def get_company_profile(self):
            pass
        
        def get_full_company_info(self):
            pass
        