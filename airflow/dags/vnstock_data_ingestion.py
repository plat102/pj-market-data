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
    dag_id="vnstock_ingest_stock",
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2024, 12, 6),
    catchup=False,
    description="Ingest data from VNStock and store it in S3",
)
def vnstock_ingest_stock():
    """
    an Airflow DAG for VNStock data ingestion.
    This function sets up a DAG with the following tasks:
    - start: A dummy operator to mark the beginning of the workflow.
    - run_test_script_task: A task that runs the main function from the pipeline.test_script module.
    - run_el_stocks_task: A task that runs the main function from the pipeline.el_stocks module.
    Each task is wrapped in a try-except block to catch and print any exceptions that occur during execution.
    The task dependencies are defined such that both run_test_script_task and run_el_stocks_task
    are executed after the start task.
    Raises:
        Exception: If an error occurs in either run_test_script_task or run_el_stocks_task.
    """

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
        from pipeline.el_stocks import el_stocks as run_el_stocks

        try:
            run_el_stocks()
        except Exception as e:
            print(f"Error in run_el_stocks_task: {e}")
            raise

    (start >> run_test_script_task() >> [run_el_stocks_task()])

vnstock_ingest_stock_dag = vnstock_ingest_stock()
