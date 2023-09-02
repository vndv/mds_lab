from datetime import datetime, timedelta

import pendulum

from airflow import DAG

from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from airflow.providers.postgres.hooks.postgres import PostgresHook


LOCAL_TZ = pendulum.timezone('Europe/Moscow')

args = {
    'owner': 'imatveev',
    'start_date': datetime(2023, 1, 1, tzinfo=LOCAL_TZ),
    'catchup': True,
    'retries': 3,
    'retry_delay': timedelta(hours=1),
}


def check_pg_connect(**context):
    pg = PostgresHook('ny_taxi')

    df = pg.get_pandas_df('SELECT 1 AS one')

    if len(df) == 1:
        print('Connect to database')

with DAG(
        dag_id='check_pg',
        schedule_interval='10 0 * * *',
        default_args=args,
        tags=['check_pg_connect', 'test'],
        concurrency=1,
        max_active_tasks=1,
        max_active_runs=1,
) as dag:

    start = EmptyOperator(
        task_id='start',
        pool='db_connection'
    )

    check_pg_connect = PythonOperator(
        task_id='check_pg_connect',
        python_callable=check_pg_connect,
        pool='db_connection'
    )

    end = EmptyOperator(
        task_id='end',
        pool='db_connection'
    )

    start >> check_pg_connect >> end