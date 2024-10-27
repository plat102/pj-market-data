from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add the pipeline directory to the Python path
sys.path.append('/opt/airflow/src/pipeline')

# Import the script function
from pipeline.test_script import main as run_test_script

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='test_python_script_execution',
    default_args=default_args,
    description='A simple DAG to test Python script execution',
    schedule_interval=None,  # Runs every minute
    start_date=datetime(2024, 10, 24),  # Set to a past date to trigger immediately
    catchup=False,
) as dag:

    # Define the Python task
    execute_script = PythonOperator(
        task_id='run_test_script',
        python_callable=run_test_script,
    )

    execute_script
