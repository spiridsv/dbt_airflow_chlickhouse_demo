import os
from datetime import datetime
from pathlib import Path

# from cosmos.profiles import ClickhouseUserPasswordProfileMapping


from cosmos import DbtDag, ProjectConfig, ProfileConfig

profile_config = ProfileConfig(
    profile_name="ch_profile",
    target_name="dev",
    profiles_yml_filepath='/opt/airflow/dags/core_bi/profiles.yml'
)

simple_dag = DbtDag(
    # dbt/cosmos-specific parameters
    project_config=ProjectConfig('/opt/airflow/dags/core_bi'),
    profile_config=profile_config,
    # execution_config=venv_execution_config,
    # normal dag parameters
    schedule_interval="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    dag_id="all_models",
)
