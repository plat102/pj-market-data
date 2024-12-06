from pipeline.transform.base import BaseProcessor


class DailyStockPriceProcess(BaseProcessor):
    def __init__(self):
        super().__init__()

    def process(self):
        raw_df = self.read_raw_data()
        transformed_df = self.transform_data(raw_df)
        self.write_to_silver(transformed_df)

    def configure_spark(self):
        pass

    def read_raw_data(self):
        pass

    def transform_data(self, df):
        return df

    def write_to_silver(self, df):
        return df
