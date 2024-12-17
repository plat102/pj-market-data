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
        print("installing papermill")

    test_spark_connection_bash = BashOperator(
        task_id="test_spark_connection_bash",
        bash_command="nc -zv spark-master 8080 && nc -zv spark-master 7077",
    )

    submit_script_spark_bash = BashOperator(
        task_id="submit_script_spark_bash",
        bash_command='spark-submit --master spark://172.21.0.3:7077 /opt/airflow/spark/application/python/test_connection.py',
        # bash_command="spark-submit --master spark://spark-master:7077 /opt/bitnami/spark/jobs/test_connection.py",
    )
    
    submit_script_spark = SparkSubmitOperator(
        task_id="submit_script_spark",
        application="/opt/bitnami/spark/jobs/test_connection.py",
        # application='/opt/airflow/spark/application/python/test_connection.py',
        conn_id="spark_default",
        verbose=True,
    )
    submit_script_airflow = SparkSubmitOperator(
        task_id="submit_script_airflow",
        # application='/opt/bitnami/spark/jobs/test_connection.py',
        application="/opt/airflow/spark/application/python/test_connection.py",
        conn_id="spark_default",
        verbose=True,
    )
    
    # TODO: SparkSubmitOperator 

    (
        start
        >> test_spark_connection_bash
        >> submit_script_spark_bash
        >> [
            submit_script_spark,
            submit_script_airflow,
        ]
    )


test_spark_conn_dag = test_spark_con()
