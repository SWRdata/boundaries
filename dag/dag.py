# ty: ignore[unresolved-import]

from datetime import timedelta

from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.cncf.kubernetes.operators.pod import (
    KubernetesPodOperator,
)
from airflow.utils.dates import days_ago
from airflow_basics.config_loader import load_config
from airflow_basics.datacatalog_update_bq import update_bq_entry
from airflow_basics.datacatalog_update_dataplex import update_dataplex
from airflow_basics.failure_reporting import check_failures, failure_reporter
from kubernetes.client import models as k8s

dag_name = "boundaries"

# Import parameters and configurations
config_path = f"/home/airflow/gcs/dags/{dag_name}/configuration.yaml"
configuration = load_config(config_path)

dag_tasks = configuration.get("dag_task_parameters", []) or []
trigger_tasks = configuration.get("trigger_task_parameters", []) or []
dag_metadata = configuration["dag_metadata"]
dataplex_metadata = configuration["dataplex_metadata"]
github_url = f"https://github.com/SWRdata/{dag_name}"

dag_metadata["default_args"]["retry_delay"] = timedelta(
    minutes=dag_metadata["default_args"]["retry_delay"]
)

with DAG(
    dag_id=dag_name,
    default_args=dag_metadata["default_args"],
    description=dag_metadata["description"],
    schedule_interval=dag_metadata["schedule_interval"],
    max_active_runs=dag_metadata["max_active_runs"],
    catchup=dag_metadata["catchup"],
    is_paused_upon_creation=dag_metadata["is_paused_upon_creation"],
    start_date=days_ago(dag_metadata["start_date"]),
) as dag:
    # dummy operators for flexibility
    pipeline_start = DummyOperator(task_id="pipeline_start")
    pipeline_end = DummyOperator(task_id="pipeline_end", trigger_rule="all_done")
    failure_report_task = PythonOperator(
        task_id="failure_report",
        python_callable=failure_reporter,
        trigger_rule="all_done",
        op_kwargs={"disable_reporting": True},
        provide_context=True,
    )
    task_list = []
    for task in dag_tasks:
        current_task = KubernetesPodOperator(
            namespace="composer-user-workloads",
            task_id=task.get("task_id"),
            image=f"{configuration['image_repo']}/{dag_name}_tasks_{task['image_suffix']}:latest",
            container_resources=k8s.V1ResourceRequirements(
                requests=task.get("container_resource").get("requests"),
                limits=task.get("container_resource").get("limits"),
            ),
            config_file="/home/airflow/composer_kube_config",
            is_delete_operator_pod=task.get("is_delete_operator_pod"),
            cmds=task.get("cmds"),
            env_vars=[
                k8s.V1EnvVar(name=key, value=value)
                for key, value in task.get("environment_variables", {}).items()
            ],
        )
        task_list.append(current_task)

    # tasks are run sequentially depending on the order they are defined in configuration.yaml
    chain(*task_list)
    if dataplex_metadata.get("dataset_id"):
        find_failures = PythonOperator(
            task_id="find_failures",
            python_callable=check_failures,
        )

        dataplex_updater = PythonOperator(
            task_id="update_dataplex",
            python_callable=update_dataplex,
            op_kwargs={
                "airflow_status": "{{ ti.xcom_pull(task_ids='check_failures', key='overall_status') }}",
                "configuration": configuration,
                "github_url": github_url,
            },
        )

        bq_updater = PythonOperator(
            task_id="update_bq",
            python_callable=update_bq_entry,
            op_kwargs={"configuration": configuration},
        )

        failure_report_task >> find_failures >> dataplex_updater >> bq_updater
    else:
        print(
            "No dataset_id provided in the configuration, skipping update_dataplex and update_bq"
        )

    (pipeline_start >> task_list >> pipeline_end)
    pipeline_end >> failure_report_task
