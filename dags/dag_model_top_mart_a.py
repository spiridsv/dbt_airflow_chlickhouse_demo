from airflow import DAG
import shutil

from airflow import DAG
from cosmos import DbtTaskGroup
from cosmos.config import ProfileConfig, ProjectConfig, RenderConfig
from cosmos.constants import TestBehavior
from cosmos.operators import DbtDocsOperator
from pendulum import datetime

MODEL = 'top_mart_a'


def upload_docs(project_dir):
    DOCS_DIR = '/opt/airflow/core_bi_docs/'
    shutil.copy(f"{project_dir}/target/index.html", DOCS_DIR)
    shutil.copy(f"{project_dir}/target/manifest.json", DOCS_DIR)
    shutil.copy(f"{project_dir}/target/graph.gpickle", DOCS_DIR)
    shutil.copy(f"{project_dir}/target/catalog.json", DOCS_DIR)


profile_config = ProfileConfig(
    profile_name="ch_profile",
    target_name="dev",
    profiles_yml_filepath="/opt/airflow/dags/core_bi/profiles.yml"
)

# shared_execution_config = ExecutionConfig(
#     invocation_mode=InvocationMode.SUBPROCESS,
# )

with DAG(
        f"gen_{MODEL}",
        start_date=datetime(2020, 12, 23),
        schedule_interval=None,
        catchup=False,
        doc_md=__doc__
) as dag:
    model = DbtTaskGroup(
        group_id=f"grp_{MODEL}",
        project_config=ProjectConfig("/opt/airflow/dags/core_bi/"),
        render_config=RenderConfig(
            test_behavior=TestBehavior.AFTER_EACH,
            select=[f'+{MODEL}'],
            # enable_mock_profile=False,
            # airflow_vars_to_purge_dbt_ls_cache=["purge"],
        ),
        # execution_config=shared_execution_config,
        operator_args={"install_deps": True},
        profile_config=profile_config,
        # default_args={"retries": 2},
    )

    generate_dbt_docs = DbtDocsOperator(
        task_id=f"generate_{MODEL}_docs",
        project_dir="/opt/airflow/dags/core_bi",
        profile_config=profile_config,
        callback=upload_docs,
        select=[MODEL]
    )

    model >> generate_dbt_docs
