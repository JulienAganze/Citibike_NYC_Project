import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from datetime import datetime

from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
import pyarrow.csv as pv
import pyarrow.parquet as pq

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
#dataset_file = "yellow_tripdata_2021-01.csv"
#dataset_url = f"https://s3.amazonaws.com/nyc-tlc/trip+data/{dataset_file}"

url = "https://s3.amazonaws.com/tripdata/JC-201509-citibike-tripdata.csv.zip"

zip_url_prefix = 'https://s3.amazonaws.com/tripdata'
zip_url_template = zip_url_prefix + '/JC-{{ execution_date.strftime(\'%Y%m\') }}-citibike-tripdata.csv.zip'
zip_output_file_template = 'JC-{{ execution_date.strftime(\'%Y%m\') }}-citibike-tripdata.csv.zip'



url_prefix = 'https://s3.amazonaws.com/nyc-tlc/trip+data'
url_template = url_prefix + '/yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.csv'
output_file_template = 'JC-{{ execution_date.strftime(\'%Y%m\') }}-citibike-tripdata.csv'
#output_file_template = path_to_local_home + '/output_{{ execution_date.strftime(\'%Y-%m\') }}.csv'

parquet_file = output_file_template.replace('.csv', '.parquet')
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'trips_data')


def format_to_parquet(src_file):
    if not src_file.endswith('.csv'):
        logging.error("Can only accept source files in CSV format, for the moment")
        return
    table = pv.read_csv(src_file)
    pq.write_table(table, src_file.replace('.csv', '.parquet'))


# NOTE: takes 20 mins, at an upload speed of 800kbps. Faster if your internet has a better upload speed
def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(bucket)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="data_ingestion_gcs_dag_citibike",
    schedule_interval="0 6 2 * *",
    start_date=datetime(2022, 11, 1),
    default_args=default_args,
    catchup=True,
    max_active_runs=3,
    tags=['citibike-gcp-data-ingestion'],
) as dag:
    
    download_dataset_task = BashOperator(
        task_id="download_dataset_task",
        bash_command=f"curl -sSLf {zip_url_template} > {path_to_local_home}/{zip_output_file_template}"
    )

    unzip_dataset_task = BashOperator(
        task_id="unzip_dataset_task",
        bash_command=f"unzip -o {path_to_local_home}/{zip_output_file_template} -d {path_to_local_home}"# && mv {path_to_local_home}/{output_file_template} {path_to_local_home}/{output_file_template}"
    )

    format_to_parquet_task = PythonOperator(
        task_id="format_to_parquet_task",
        python_callable=format_to_parquet,
        op_kwargs={
            "src_file": f"{path_to_local_home}/{output_file_template}",
        },
    )

    # TODO: Homework - research and try XCOM to communicate output values between 2 tasks/operators
    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"raw/{parquet_file}",
            "local_file": f"{path_to_local_home}/{parquet_file}",
        },
    )

    bigquery_external_table_task = BigQueryCreateExternalTableOperator(
        task_id="bigquery_external_table_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": "external_table",
            },
            "externalDataConfiguration": {
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET}/raw/JC-*"],
            },
        },
    )

    




    remove_files_task = BashOperator(
        task_id="remove_files_task",
        bash_command=f"rm {path_to_local_home}/{output_file_template} {path_to_local_home}/{parquet_file} {path_to_local_home}/{zip_output_file_template}"
    )

    download_dataset_task >> unzip_dataset_task >> format_to_parquet_task >> local_to_gcs_task >> bigquery_external_table_task >> remove_files_task