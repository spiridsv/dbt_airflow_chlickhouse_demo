from airflow.operators.empty import EmptyOperator

"""
Shows how to parse a dbt manifest file to "explode" the dbt DAG into Airflow

Each dbt model is run as a bash command.
"""

from pendulum import datetime

from airflow import DAG

from dbt_dag_parser import DbtDagParser

PROJ = '/opt/airflow/dags/core_bi/'

with DAG(
        "dbt_advanced_dag_utility",
        start_date=datetime(2020, 12, 23),
        description="A dbt wrapper for Airflow using a utility class to map the dbt DAG to Airflow tasks",
        schedule_interval=None,
        catchup=False,
        doc_md=__doc__
) as dag:
    start_dummy = EmptyOperator(task_id="start")
    end_dummy = EmptyOperator(task_id="end")

    # The parser parses out a dbt manifest.json file and dynamically creates tasks for "dbt run" and "dbt test"
    # commands for each individual model. It groups them into task groups which we can retrieve and use in the DAG.
    dag_parser = DbtDagParser(
        dbt_global_cli_flags='',
        dbt_project_dir=PROJ,
        dbt_profiles_dir=PROJ,
        dbt_target='dev',
    )
    dbt_run_group = dag_parser.get_dbt_run_group()
    dbt_test_group = dag_parser.get_dbt_test_group()

    start_dummy >> dbt_run_group >> dbt_test_group >> end_dummy
