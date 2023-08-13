from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

import sys
sys.path.append('/home/mik/deads1_project/scripts/')
from b_get_all_data import *

import requests


# Statische Informationen der Ladestationen (EVSEData) - kontinuierlich aktualisiert
# https://opendata.swiss/dataset/ladestationen-fuer-elektroautos
# https://opendata.swiss/dataset/ladestationen-fuer-elektroautos/resource/e33957be-180a-422b-90a5-fbfe9774927a
def data_charginstation_data():
    url = "https://data.geo.admin.ch/ch.bfe.ladestellen-elektromobilitaet/data/oicp/ch.bfe.ladestellen-elektromobilitaet.json"
    r = requests.get(url)
    with open("../data/bronze/data.ch.bfe.ladestellen-elektromobilitaet.json", "wb") as file:
        file.write(r.content)


# Verfügbarkeits-Informationen der Ladestationen (EVSEStatus) - kontinuierlich aktualisiert
# https://opendata.swiss/dataset/ladestationen-fuer-elektroautos
# https://opendata.swiss/dataset/ladestationen-fuer-elektroautos/resource/4d467a51-0bc9-48ce-aa2a-3d3bcaa7e7e9
def data_charginstation_avail():
    url = "https://data.geo.admin.ch/ch.bfe.ladestellen-elektromobilitaet/status/oicp/ch.bfe.ladestellen-elektromobilitaet.json"
    r = requests.get(url)
    with open("../data/bronze/status.ch.bfe.ladestellen-elektromobilitaet.json", "wb") as file:
        file.write(r.content)


# Ich tanke Strom, Kennzahlen Neuwagen und Ladeinfrastruktur
# https://www.uvek-gis.admin.ch/BFE/storymaps/MO_Kennzahlen_Fahrzeuge/Ladeinfrastruktur_Elektromobilitaet/
def data_tanke_strom_monthly():
    url = "https://www.uvek-gis.admin.ch/BFE/ogd/57/ich_tanke_strom_Kennzahlen_monatlich.csv"
    r = requests.get(url)
    with open("../data/bronze/ich_tanke_strom_monthly.csv", "wb") as file:
        file.write(r.content)


# Landesverbrauch und Endverbrauch
# https://opendata.swiss/de/dataset/energiedashboard-ch-stromverbrauch-swissgrid/resource/3569b65f-1afc-4541-876f-cd98f9256cb1
def data_lverbrauch_everbrauch():
    url = "https://bfe-energy-dashboard-ogd.s3.amazonaws.com/ogd103_stromverbrauch_swissgrid_lv_und_endv.csv"
    r = requests.get(url)
    with open("../data/bronze/landesverbrauch-endverbrauch.csv", "wb") as file:
        file.write(r.content)

# Stromverbrauch Prognose SDSC
# https://opendata.swiss/de/dataset/energiedashboard-ch-stromverbrauch-prognose-sdsc/resource/db0b4b38-fc9f-47e6-805e-c467337621f9
def data_stromverbrauch_prognose():
    url = "https://bfe-energy-dashboard-ogd.s3.amazonaws.com/ogd110_strom_verbrauch_prognose.csv"
    r = requests.get(url)
    with open("../data/bronze/stromverbrauch_prognose.csv", "wb") as file:
        file.write(r.content)


# Stromproduktion
# https://opendata.swiss/de/dataset/energiedashboard-ch-stromproduktion-swissgrid/resource/619e6fa0-7c2b-46dd-9633-7bd60fc5ec16
def data_stromproduktion():
    url = "https://bfe-energy-dashboard-ogd.s3.amazonaws.com/ogd104_stromproduktion_swissgrid.csv"
    r = requests.get(url)
    with open("../data/bronze/stromproduktion.csv", "wb") as file:
        file.write(r.content)

def backupdata():
    print()



def foobarstrom():
   data_tanke_strom_monthly()

with DAG(
    dag_id="getallData",
    start_date=datetime(2023,1,1),
    schedule_interval=None,
    catchup=False,
    tags=["load", "bronze"],
) as dag:
    task1 = PythonOperator(
    task_id="Strom_monthly",
    python_callable=data_tanke_strom_monthly
    )

    task2 = PythonOperator(
    task_id="CH_Stromproduktion",
    python_callable=data_stromproduktion
    )

task1 >> task2


