"""Load data from S3 silver layer to PostgreSQL using Spark"""

import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

import os
from dotenv import load_dotenv

load_dotenv()

MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")

def run_spark_etl(bucket, file_key, app_name, db_url, db_user, db_password, db_schema, db_table):
    # Initialize Spark Session
    spark = SparkSession.builder \
        .master("spark://spark-master:7077") \
        .appName(app_name) \
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
        .config("spark.hadoop.fs.s3a.access.key", MINIO_ACCESS_KEY) \
        .config("spark.hadoop.fs.s3a.secret.key", MINIO_SECRET_KEY) \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.jars", "jars/hadoop-aws-3.3.4.jar,jars/aws-java-sdk-1.12.367.jar,jars/postgresql-42.5.0.jar") \
        .getOrCreate()

    # Extract: Read Parquet from S3
    if file_key.startswith("s3a://"):
        s3_path = file_key
    elif not bucket:
        s3_path = f"s3a://{bucket}/{file_key}"
    else:
        s3_path = f"s3a://{file_key}"
    print(f"Reading data from: {s3_path}")
    df = spark.read.parquet(s3_path)

    # Load: Write to PostgreSQL
    db_properties = {
        "user": db_user,
        "password": db_password,
        "driver": "org.postgresql.Driver",
    }
    db_table_path = f"{db_schema}.{db_table}"
    print(f"Writing data to: {db_url}, table: {db_table_path}")

    df.write \
        .jdbc(
            url=db_url,
            table=db_table_path,
            mode="overwrite",
            properties=db_properties,
        )

    print("ETL process completed successfully.")
    
    spark.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", default=None, help="S3 bucket name (optional)")
    parser.add_argument("--file_key", required=True, help="Parquet file key in S3")
    parser.add_argument("--app_name", required=True, help="Spark application name")
    parser.add_argument("--db_url", required=True, help="PostgreSQL JDBC URL")
    parser.add_argument("--db_user", required=True, help="PostgreSQL user name")
    parser.add_argument("--db_password", required=True, help="PostgreSQL user password")
    parser.add_argument("--db_schema", required=True, help="PostgreSQL schema name")
    parser.add_argument("--db_table", required=True, help="PostgreSQL table name")
    args = parser.parse_args()

    run_spark_etl(
        bucket=args.bucket,
        file_key=args.file_key,
        app_name=args.app_name,
        db_url=args.db_url,
        db_user=args.db_user,
        db_password=args.db_password,
        db_schema=args.db_schema,
        db_table=args.db_table
    )
    