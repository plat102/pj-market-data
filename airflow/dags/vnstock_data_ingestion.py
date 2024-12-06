"""Ingest data from VNStock and store it in S3"""

import sys
from datetime import timedelta, datetime

from airflow.decorators import dag, task
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from fsspec import Callback

# Add the pipeline directory to the Python path
sys.path.append("/opt/airflow/src/pipeline")

# Import scripts
from pipeline.test_script import main as run_test_script
from pipeline.el_stocks import main as run_el_stocks

default_args = {
    "owner": "thu.phan",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="vnstock_data_ingestion",
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2024, 12, 6),
)
def vnstock_data_ingestion():
    start = DummyOperator(task_id="start")

    @task()
    def run_test_script_task():
        run_test_script()

    @task()
    def run_el_stocks_task():
        run_el_stocks()

    start >> [run_test_script_task(), run_el_stocks_task()]


vnstock_data_ingestion_dag = vnstock_data_ingestion()
