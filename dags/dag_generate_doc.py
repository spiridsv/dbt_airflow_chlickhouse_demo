import shutil

from airflow import DAG
from cosmos.config import ProfileConfig
from cosmos.operators import DbtDocsOperator
from pendulum import datetime

with DAG(
        "generate_docs_all_models",
        start_date=datetime(2020, 12, 23),
        description="Generate DOCS for all models",
        schedule_interval=None,
        catchup=False,
        doc_md=__doc__
) as dag:
    profile_config = ProfileConfig(
        profile_name="ch_profile",
        target_name="dev",
        profiles_yml_filepath="/opt/airflow/dags/core_bi/profiles.yml"
    )


    def upload_docs(project_dir):
        # upload docs to a storage of your choice
        # you only need to upload the following files:
        # - f"{project_dir}/target/index.html"
        # - f"{project_dir}/target/manifest.json"
        # - f"{project_dir}/target/graph.gpickle"
        # - f"{project_dir}/target/catalog.json"
        DOCS_DIR = '/opt/airflow/core_bi_docs/'

        shutil.copy(f"{project_dir}/target/index.html", DOCS_DIR)
        shutil.copy(f"{project_dir}/target/manifest.json", DOCS_DIR)
        shutil.copy(f"{project_dir}/target/graph.gpickle", DOCS_DIR)
        shutil.copy(f"{project_dir}/target/catalog.json", DOCS_DIR)


    generate_dbt_docs = DbtDocsOperator(
        task_id="generate_all_dbt_docs",
        project_dir="/opt/airflow/dags/core_bi",
        profile_config=profile_config,
        callback=upload_docs,
    )
