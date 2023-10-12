# bash_command="cd /ny_taxi && dbt run"

from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.models.baseoperator import chain
from airflow_dbt.operators.dbt_operator import DbtRunOperator, DbtDocsGenerateOperator


default_args = {
    "owner": "iamatveev",
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=1),
    "start_date": days_ago(1),
    "schedule_interval": "0 0 * * *",
    "dir": "/ny_taxi",
}


with DAG(
    dag_id="dbt_pipeline",
    default_args=default_args,
) as dag:


    dbt_run_model_1 = DbtRunOperator(
        task_id="dbt_run_my_second_dbt_model",
        select="my_first_dbt_model.sql",
        profiles_dir=default_args["dir"],
        dir=default_args["dir"],
    )


    dbt_docs_generate = DbtDocsGenerateOperator(
        task_id="dbt_docs_generate",
    )


    chain(dbt_run_model_1, dbt_docs_generate)