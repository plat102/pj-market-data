"""Ingest data from VNStock and store it in S3"""
import os
from datetime import timedelta, datetime

from dotenv import load_dotenv

from airflow.decorators import dag, task
from airflow.operators.dummy import DummyOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.models import Connection

load_dotenv()

BRONZE_PATH = os.environ.get("BRONZE_PATH")
SILVER_PATH = os.environ.get("SILVER_PATH")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")

bronze_path = f"s3a:/{BRONZE_PATH}/vnstock3/stock_quote_history_daily/"
silver_path = f"s3a:/{SILVER_PATH}/vnstock3/daily_stock_prices/"


default_args = {
    "owner": "thu.phan",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Retrieve PostgreSQL credentials from Airflow connection
postgres_analytics_conn = Connection.get_connection_from_secrets("postgres_analytics")
db_url = f"jdbc:postgresql://{postgres_analytics_conn.host}:{postgres_analytics_conn.port}/{postgres_analytics_conn.schema}"
db_user = postgres_analytics_conn.login
db_password = postgres_analytics_conn.password


@dag(
    dag_id="vnstock_transform_stock_prices",
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2024, 12, 10),
    catchup=False,
    description="Transform raw .json data from VNStock and parquet in S3 silver layer",
)
def vnstock_transform_stock_prices():
    """ """

    start = DummyOperator(task_id="start")

    @task()
    def pm_run_stock_notebook():
        print("installing papermill")

    # SparkSubmitOperator to run the Spark job
    process_stock_prices = SparkSubmitOperator(
        task_id="process_stock_prices",
        application="/opt/airflow/spark/application/python/process_stock_price.py",
        conn_id="spark_default",
        jars="jars/delta-core_2.12-2.2.0.jar,jars/hadoop-aws-3.3.4.jar,jars/delta-storage-2.2.0.jar,jars/aws-java-sdk-1.12.367.jar,jars/s3-2.18.41.jar,jars/aws-java-sdk-bundle-1.11.1026.jar",
        conf={
            "spark.hadoop.fs.s3a.endpoint": "http://minio:9000",
            "spark.hadoop.fs.s3a.access.key": MINIO_ACCESS_KEY,
            "spark.hadoop.fs.s3a.secret.key": MINIO_SECRET_KEY,
            "spark.hadoop.fs.s3a.path.style.access": "true",
            "spark.hadoop.fs.s3a.connection.ssl.enabled": "false",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        },
        verbose=True,
        application_args=[],
    )

    load_stock_prices_to_pg = SparkSubmitOperator(
        task_id="load_stock_prices_to_pg",
        application="/opt/airflow/spark/application/python/load_from_s3_to_pg.py",
        name="ETL_Spark_Job",
        conn_id="spark_default",
        jars="jars/hadoop-aws-3.3.4.jar,jars/aws-java-sdk-1.12.367.jar,jars/s3-2.18.41.jar,jars/aws-java-sdk-bundle-1.11.1026.jar,jars/postgresql-42.5.0.jar",
        conf={"spark.executor.memory": "1g", "spark.executor.cores": "1"},
        application_args=[
            "--file_key", silver_path,
            "--app_name", "Stock_Parquet_to_PostgreSQL",
            "--db_url", db_url,
            "--db_user", db_user,
            "--db_password", db_password,
            "--db_schema", "staging",
            "--db_table", "stock_prices_history",
        ],
    )
    (
        start >> [pm_run_stock_notebook(), process_stock_prices]
        >> load_stock_prices_to_pg
    )


vnstock_transform_stock_prices_dag = vnstock_transform_stock_prices()
