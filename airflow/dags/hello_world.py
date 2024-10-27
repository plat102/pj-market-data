from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def my_function():
    print("Hello, World!")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 10, 25),
}

with DAG('example_dag', default_args=default_args, schedule_interval='@daily') as dag:
    task1 = PythonOperator(
        task_id='run_my_function',
        python_callable=my_function,
    )
