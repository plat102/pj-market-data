import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession

load_dotenv()

BRONZE_PATH = os.environ.get("BRONZE_PATH")
SILVER_PATH = os.environ.get("SILVER_PATH")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")

bronze_path_exchange = f"s3a:/{BRONZE_PATH}/vnstock3/symbol_exchange"
bronze_path_industry = f"s3a:/{BRONZE_PATH}/vnstock3/symbol_industry"
silver_path = f"s3a:/{SILVER_PATH}/vnstock3/symbol"

# Setup Spark sesssion
spark = (SparkSession.builder
    .master("spark://spark-master:7077")
    .appName("CompanyDataProcess")
    .getOrCreate()
)

from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType, IntegerType, DateType
from pyspark.sql.functions import col, from_unixtime

schema_exchange = StructType([
    StructField("symbol", StringType(), False),
    StructField("id", IntegerType(), True),
    StructField("type", StringType(), True),
    StructField("exchange", StringType(), True),
    StructField("en_organ_name", StringType(), True),
    StructField("en_organ_short_name", StringType(), True),
    StructField("organ_short_name", StringType(), True),
    StructField("organ_name", StringType(), True),
    StructField("loaded_timestamp", StringType(), True),
    StructField("updated_at", DateType(), True)
])

raw_df_exchange = spark.read.schema(schema_exchange).json(bronze_path_exchange)

raw_df_exchange = (raw_df_exchange
    .withColumn(
        "loaded_timestamp",
        from_unixtime(col("loaded_timestamp").cast("long") / 1000).cast(TimestampType())  # Convert milliseconds to seconds
    )
)

# drop na
df_exchange = raw_df_exchange.dropna(subset=["symbol", "loaded_timestamp"])

# drop duplicate
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number

window_spec = Window.partitionBy("symbol").orderBy(col("updated_at"), col("loaded_timestamp").desc())

df_exchange = df_exchange.withColumn("row_number",
                  row_number().over(window_spec))

df_exchange = df_exchange.filter(col("row_number") == 1) \
                .drop("row_number")

schema_industry = StructType([
    StructField("symbol", StringType(), False),
    StructField("organ_name", StringType(), True),
    StructField("en_organ_name", StringType(), True),
    StructField("icb_name3", StringType(), True),
    StructField("en_icb_name3", StringType(), True),
    StructField("icb_name2", StringType(), True),
    StructField("en_icb_name2", StringType(), True),
    StructField("icb_name4", StringType(), True),
    StructField("en_icb_name4", StringType(), True),
    StructField("com_type_code", StringType(), True),
    StructField("icb_code1", StringType(), True),
    StructField("icb_code2", StringType(), True),
    StructField("icb_code3", StringType(), True),
    StructField("icb_code4", StringType(), True),
    StructField("loaded_timestamp", StringType(), True),
    StructField("updated_at", DateType(), True)
])

raw_df_industry = spark.read.schema(schema_industry).json(bronze_path_industry)

raw_df_industry = (raw_df_industry
    .withColumn(
        "loaded_timestamp",
        from_unixtime(col("loaded_timestamp").cast("long") / 1000).cast(TimestampType())  # Convert milliseconds to seconds
    )
)

# drop na
df_industry = raw_df_industry.dropna(subset=["symbol", "loaded_timestamp"])

# drop duplicate
df_industry = df_industry.withColumn("row_number",
                  row_number().over(window_spec))

df_industry = df_industry.filter(col("row_number") == 1) \
                .drop("row_number")
                
                
# Perform the left outer join
df_joined = df_exchange.join(
    df_industry,
    on="symbol", 
    how="left" 
)

# Select or rename columns to remove ambiguity
df = df_joined.select(
    df_exchange["symbol"],
    df_exchange["id"],
    df_exchange["type"],
    df_exchange["exchange"],
    df_exchange["en_organ_name"].alias("exchange_en_organ_name"),
    df_exchange["en_organ_short_name"],
    df_exchange["organ_short_name"],
    df_exchange["organ_name"].alias("exchange_organ_name"),
    df_industry["icb_name3"],
    df_industry["en_icb_name3"],
    df_industry["icb_name2"],
    df_industry["en_icb_name2"],
    df_industry["icb_name4"],
    df_industry["en_icb_name4"],
    df_industry["com_type_code"],
    df_industry["icb_code1"],
    df_industry["icb_code2"],
    df_industry["icb_code3"],
    df_industry["icb_code4"],
    df_exchange["loaded_timestamp"].alias("exchange_loaded_timestamp"),
    df_industry["loaded_timestamp"].alias("industry_loaded_timestamp"),
    df_exchange["updated_at"]
)

from pyspark.sql.functions import current_timestamp
df = df.withColumn(
    "processed_time",
    current_timestamp()
)
df.show(20, truncate=False)
df.printSchema()


df.write \
    .partitionBy("type") \
    .mode("overwrite") \
    .parquet(silver_path)

print(f"Data written to silver path at {silver_path}")
