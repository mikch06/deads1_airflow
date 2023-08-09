from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

import sys
sys.path.append('/home/mik/deads1_project/scripts/')
from b_get_all_data import *

def helloWorld():
    print("Hello World")

#data_charginstation_data()
#data_tanke_strom_monthly()
def foobarstrom():
   data_tanke_strom_monthly()

with DAG(
    dag_id="mik_dag1",
    start_date=datetime(2023,1,1),
    schedule_interval=None,
    catchup=False,
    tags=["load", "bronze"],
) as dag:
    task1 = PythonOperator(
    task_id="hello_world",
    python_callable=helloWorld
    )

    task2 = PythonOperator(
    task_id="dataload",
    python_callable=foobarstrom
    )

task1 >> task2


