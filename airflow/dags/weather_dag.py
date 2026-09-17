from datetime import datetime
import pendulum

from airflow import DAG
from airflow.operators.python import PythonOperator

from app import get_params, conserve_data, transformer_data, save_data, nettoyage_data, categorie_data 

from insertData import insertData

local_tz = pendulum.timezone("Africa/Casablanca")

with DAG(
    dag_id="meteo_example",
    start_date=pendulum.datetime(2026, 9, 16, tz=local_tz),
    schedule="0 0 * * *",
    catchup=False,
) as dag:
    extract_task = PythonOperator(
        task_id="get_params",
        python_callable=get_params
    )

    conserve_task = PythonOperator(
        task_id="conserve_data",
        python_callable=conserve_data
    )

    transform_task = PythonOperator(
        task_id="transformer_data",
        python_callable=transformer_data
    )

    save_task = PythonOperator(
        task_id="save_data",
        python_callable=save_data
    )

    nettoyage_task = PythonOperator(
        task_id="nettoyage_data",
        python_callable=nettoyage_data
    )

    categorie_task = PythonOperator(
        task_id="categorie_data",
        python_callable=categorie_data
    )

    insert_data_task = PythonOperator(
        task_id="insertData",
        python_callable=insertData
    )

    extract_task >> conserve_task >> transform_task >> save_task >> nettoyage_task >> categorie_task >> insert_data_task
    