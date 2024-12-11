import os
from dotenv import load_dotenv

load_dotenv()

BRONZE_PATH = os.environ.get("BRONZE_PATH")
SILVER_PATH = os.environ.get("SILVER_PATH")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")

bronze_path = f"s3a:/{BRONZE_PATH}/vnstock3/stock_quote_history_daily/"
silver_path = f"s3a:/{SILVER_PATH}/vnstock3/daily_stock_prices/"


from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, from_unixtime



# Setup Spark sesssion
spark = (SparkSession.builder
    .master("spark://spark-master:7077")
    .appName("DailyStockPriceProcessor")
    .getOrCreate()
)

print(f"Spark session created: {spark}")

data = [("Alice", 1), ("Bob", 2), ("Cathy", 3)]
df = spark.createDataFrame(data, ["Name", "Id"])


from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType, IntegerType, DateType

schema = StructType([
    StructField("time", StringType(), True),
    StructField("open", FloatType(), True),
    StructField("high", FloatType(), True),
    StructField("low", FloatType(), True),
    StructField("close", FloatType(), True),
    StructField("volume", IntegerType(), True),
    StructField("symbol", StringType(), True),
    StructField("loaded_timestamp", StringType(), True),
    StructField("updated_at", DateType(), True)
])

# Read the raw data from the bronze path in MinIO
raw_df = spark.read.schema(schema).json(bronze_path)


# Convert 'loaded_timestamp' from string (epoch time in milliseconds) to TimestampType
raw_df = (raw_df
    .withColumn(
        "loaded_timestamp",
        from_unixtime(col("loaded_timestamp").cast("long") / 1000).cast(TimestampType())  # Convert milliseconds to seconds
    )
    .withColumn(
        "time",
        from_unixtime(col("time").cast("long") / 1000).cast(TimestampType())  # Convert milliseconds to seconds
    )
)


# drop na

df = raw_df.dropna(subset=["time", "open", "high", "low", "close", "volume", "symbol"])


# drop duplicate
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number

window_spec = Window.partitionBy("symbol", "time").orderBy(col("updated_at"), col("loaded_timestamp").desc())

df = df.withColumn("row_number",
                  row_number().over(window_spec))

df_drop_dup = df.filter(col("row_number") == 1) \
                .drop("row_number")


df_drop_dup.filter((col("symbol") == "TV2") & (col("time") == "2024-11-01")).show(20, truncate=False)


# Calculate the daily price range (high - low)
df_cal = df_drop_dup.withColumn(
    "price_range",
    df.high - df.low
)


from pyspark.sql import functions as F


# Calculate the percentage change from open to close
df_cal = df_cal.withColumn(
    "price_percent_change",
    (F.col("close") - F.col("open")) / F.col("open")
)


# Add metadata - processing time

df_cal = df_cal.withColumn(
    "processing_time",
    F.current_timestamp()
)


print(bronze_path) 
print(silver_path)

df_cal.write.mode("overwrite").parquet(silver_path)
