import datetime

from FaceitExport import main
from airflow import DAG
from airflow.operators.python import PythonOperator


args = {
    "owner": "Ali",
    "start_date": datetime.datetime(2022, 1, 1),
    "provide_context": True
}

with DAG('FaceitExport', description='Faceit Export',
         schedule_interval='* */1 * * *', catchup=False,
         default_args=args) as dag:
    etl = PythonOperator(task_id='etl', python_callable=main)

