"""Ingest data from VNStock and store it in S3"""

import sys
from datetime import timedelta, datetime

from airflow.decorators import dag, task
from airflow.operators.dummy import DummyOperator

# Add the pipeline directory to the Python path
sys.path.append("/opt/airflow/src/pipeline")

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
    catchup=False,
)
def vnstock_data_ingestion():
    start = DummyOperator(task_id="start")

    @task()
    def run_test_script_task():
        from pipeline.test_script import main as run_test_script
        try:
            run_test_script()
        except Exception as e:
            print(f"Error in run_test_script_task: {e}")
            raise

    @task()
    def run_el_stocks_task():
        from pipeline.el_stocks import main as run_el_stocks
        try:
            run_el_stocks()
        except Exception as e:
            print(f"Error in run_el_stocks_task: {e}")
            raise

    start >> [run_test_script_task(), run_el_stocks_task()]


vnstock_data_ingestion_dag = vnstock_data_ingestion()
