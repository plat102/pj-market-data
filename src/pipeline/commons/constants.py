"""
Storing constants of the project
"""

from enum import Enum

class VnstockDataSources(Enum):
    VCI = 'VCI'
    TCBS = 'TCBS'
    MSN = 'MSN'

class VnstockSymbolGroups(Enum):
    VN30 = 'VN30'
    HNX30 = 'HNX30'
    UPCOM = 'UPCOM'
    HNX = 'HNX'
    HOSE = 'HOSE'
    VNMIDCAP = 'VNMidCap'
    VNSMAILLCAP = 'VNSmallCap'
    VNALLSHARE = 'VNAllShare'
    VN100 = 'VN100'
    ETF = 'ETF'
    HNXFIN = 'HNXFin'
    HNXMSCAP = 'HNXMSCap'
    HNXLCAP = 'HNXLCap'
    HNXMAN = 'HNXMan'
    HNXCON = 'HNXCon'
    FU_INDEX = 'FU_INDEX'
    CW = 'CW'
    

class S3FileTypes(Enum):
    """
    Supported file types for S3BucketConnector.
    
    This Enum class defines the supported file types for the S3BucketConnector.
    
    Attributes:
        CSV (str): Represents CSV file type.
        PARQUET (str): Represents Parquet file type.
    """
    CSV: str = 'csv'
    PARQUET: str = 'parquet'
    
class MetaProcessFormat(Enum):
    """
    Formater for meta file
    Args:
        Enum (_type_): _description_
    """
    META_DATE_FORMAT = '%Y-%m-%d'
    META_PROCESS_DATE_FORMAT = '%Y-%m-%d %H-%M-%S'
    META_SOURCE_DATE_COL = 'source_date'
    META_PROCESS_COL = 'datetime_of_processing'
    META_FILE_FORMAT = 'csv'
    