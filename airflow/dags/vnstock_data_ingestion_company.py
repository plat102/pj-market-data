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
    dag_id="vnstock_ingest_company_data",
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2024, 12, 21),
    catchup=False,
    description="Ingest data from VNStock and store it in S3",
)
def vnstock_ingest_company_data():
    """
    Airflow DAG to ingest company data for VNStock.
    This DAG consists of the following tasks:
    1. start: A dummy starting task.
    2. run_test_script_task: Executes the main function from the pipeline.test_script module.
    3. run_el_companies_task: Executes the el_companies function from the pipeline.el_companies module.
    Task Flow:
    start >> run_test_script_task >> run_el_companies_task
    Tasks:
    - run_test_script_task: Runs a test script and handles any exceptions that occur.
    - run_el_companies_task: Runs the el_companies function and handles any exceptions that occur.
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
    def run_el_companies_task():
        from pipeline.el_companies import el_companies as run_el_companies

        try:
            run_el_companies()
        except Exception as e:
            print(f"Error in run_el_companies_task: {e}")

    (start >> run_test_script_task() >> [run_el_companies_task()])

vnstock_ingest_company_data_dag = vnstock_ingest_company_data()
