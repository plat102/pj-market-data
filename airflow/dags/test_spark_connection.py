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
    dag_id="test_spark_connection",
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2024, 12, 10),
    catchup=False,
    description="Test Spark connection",
)
def test_spark_con():
    """
    Test Spark connection
    """
    
    start = DummyOperator(task_id="start")

    @task()
    def pm_run_stock_notebook():
        print('installing papermill')

    test_spark_submit = SparkSubmitOperator(
        task_id='test_spark_submit',
        application='/opt/bitnami/spark/jobs/test_connection.py',
        # application='/opt/airflow/spark/application/python/test_job.py',
        conn_id='spark_default',
        verbose=True,
    )

    test_spark_connection_bash = BashOperator(
        task_id='test_spark_connection_bash',
        bash_command='nc -zv spark-master 8080 && nc -zv spark-master 7077'
    )

    spark_submit = BashOperator(
        task_id='test_spark_submit_bash',
        # bash_command='spark-submit --master spark://spark-master:7077 /opt/airflow/spark/application/python/test_job.py',
        bash_command='spark-submit --master spark://spark-master:7077 /opt/bitnami/spark/jobs/test_connection.py',
    )
    

    (start >> [test_spark_submit, test_spark_connection_bash, spark_submit] 
    )


test_spark_conn_dag = test_spark_con()
