"""Ingest data from VNStock and store it in S3"""

import sys
from datetime import timedelta, datetime

from airflow.decorators import dag, task
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
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
    """
    """
    
    start = DummyOperator(task_id="start")

    @task()
    def pm_run_stock_notebook():
        print('installing papermill')
    
    # TODO: BashOperator to run the simple test Spark job
    spark_submit = BashOperator(
        task_id='test_spark_submit',
        bash_command='spark-submit --master spark://spark-master:7077 /opt/airflow/spark/application/python/process_stock_price.py',
    )
    
    # Test cmd docker exec -it arrow-spark /opt/airflow/spark/application/python/process_stock_price.py
    
    # TODO: SparkSubmitOperator to run the Spark job
    spark_job = SparkSubmitOperator(
        task_id='process_stock_prices',
        application='/opt/airflow/spark/application/python/process_stock_price.py',
        conn_id='spark_default',
        conf={
            'spark.executor.memory': '2g',
            'spark.driver.memory': '2g'
        },
        verbose=True,
        application_args=[]
    )

    start >> [pm_run_stock_notebook(), spark_job]


vnstock_transform_dag = vnstock_data_transform()
