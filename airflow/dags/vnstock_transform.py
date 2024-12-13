"""Ingest data from VNStock and store it in S3"""

import sys
from datetime import timedelta, datetime

from airflow.decorators import dag, task
from airflow.operators.dummy import DummyOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {
    "owner": "thu.phan",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="vnstock_transform",
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2024, 12, 10),
    catchup=False,
    description="Transform raw .json data from VNStock and parquet in S3 silver layer",
)
def vnstock_data_transform():
    """ """

    start = DummyOperator(task_id="start")

    @task()
    def pm_run_stock_notebook():
        print("installing papermill")

    # TODO: SparkSubmitOperator to run the Spark job
    spark_job = SparkSubmitOperator(
        task_id="process_stock_prices",
        application="/opt/airflow/spark/application/python/process_stock_price.py",
        conn_id="spark_default",
        jars='jars/delta-core_2.12-2.2.0.jar,jars/hadoop-aws-3.3.4.jar,jars/delta-storage-2.2.0.jar,jars/aws-java-sdk-1.12.367.jar,jars/s3-2.18.41.jar,jars/aws-java-sdk-bundle-1.11.1026.jar',
        conf={
            "spark.hadoop.fs.s3a.endpoint": "http://minio:9000",
            "spark.hadoop.fs.s3a.access.key": "minio",
            "spark.hadoop.fs.s3a.secret.key": "minio123",
            "spark.hadoop.fs.s3a.path.style.access": "true",
            "spark.hadoop.fs.s3a.connection.ssl.enabled": "false",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        },
        verbose=True,
        application_args=[],
    )

    (start >> [pm_run_stock_notebook(), spark_job])


vnstock_transform_dag = vnstock_data_transform()
