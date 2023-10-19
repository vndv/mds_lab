import os
from datetime import datetime
from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from ingestion_script import ingest_data

# https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2023-01.parquet

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

URL_PREFIX = "https://d37ci6vzurychx.cloudfront.net/trip-data"
URL_YELLOW_TEMPLATE = URL_PREFIX + "/yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.parquet"
URL_GREEN_TEMPLATE = URL_PREFIX + "/green_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.parquet"
OUTPUT_TEMPLATE_YELLOW = AIRFLOW_HOME + "/output_yellow{{ execution_date.strftime(\'%Y-%m\') }}.parquet"
OUTPUT_TEMPLATE_GREEN = AIRFLOW_HOME + "/output_green{{ execution_date.strftime(\'%Y-%m\') }}.parquet"
TABLE_YELLOW_TEMPLATE = "yellow_taxi_data"
TABLE_GREEN_TEMPLATE = "green_taxi_data"

workflow = DAG(
    dag_id="IngestionDag",
    schedule_interval="0 6 2 * *",
    start_date=datetime(2023,1,1),
    end_date = datetime(2023,7,1),
)

with workflow:

    wget_yellow_task = BashOperator(
        task_id='wget_yellow',
        bash_command=f'curl -sSL {URL_YELLOW_TEMPLATE} > {OUTPUT_TEMPLATE_YELLOW}'
    )

    wget_green_task = BashOperator(
        task_id='wget_green',
        bash_command=f'curl -sSL {URL_GREEN_TEMPLATE} > {OUTPUT_TEMPLATE_GREEN}'
    )

    ingest_yellow_task = PythonOperator(
        task_id='ingest_yellow',
        python_callable=ingest_data,
        op_kwargs=dict(
            pq_file=OUTPUT_TEMPLATE_YELLOW,
            table_name=TABLE_YELLOW_TEMPLATE

        )
    )

    ingest_green_task = PythonOperator(
        task_id='ingest_green',
        python_callable=ingest_data,
        op_kwargs=dict(
            pq_file=OUTPUT_TEMPLATE_GREEN,
            table_name=TABLE_GREEN_TEMPLATE

        )
    )

    wget_yellow_task >> ingest_yellow_task
    wget_green_task >> ingest_green_task