# test_script.py
from pipeline.extract.vnstock_lib import VnstockLibExtractor
from pipeline.commons.connectors.vnstock_lib import VnstockLibConnector

def main():
    print("Hello, this is a test script!")
    extractor = VnstockLibExtractor()
    connector = VnstockLibConnector()
    connector.connect()



if __name__ == "__main__":
    main()
