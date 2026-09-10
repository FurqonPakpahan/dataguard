from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

from dataguard.operators.dataguard_operator import DataGuardOperator


def extract_and_load_data():
    """
    Simulasi task 'extract & load data'.
    Di dunia nyata, ini akan berisi logic ambil data dari sumber
    dan load ke tabel staging. Untuk demo ini, kita anggap data
    sudah ada di tabel 'transactions' (sudah kita siapkan manual).
    """
    print("Simulating data extraction and load into 'transactions' table...")
    print("(In this demo, the data is already pre-loaded for demonstration purposes)")


def generate_downstream_report():
    """
    Simulasi task 'downstream' yang bergantung pada data yang sudah divalidasi.
    Task ini TIDAK BOLEH jalan kalau validasi sebelumnya gagal.
    """
    print("Generating downstream business report from validated data...")


with DAG(
    dag_id="transactions_quality_pipeline",
    description="Example ETL pipeline demonstrating DataGuard fail-fast behavior",
    start_date=datetime(2026, 1, 1),
    schedule=None,  # manual trigger only, untuk demo
    catchup=False,
    tags=["dataguard", "example"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_and_load_data",
        python_callable=extract_and_load_data,
    )

    validate_task = DataGuardOperator(
        task_id="validate_data_quality",
        contract_path="/opt/airflow/dags/examples/contracts/transactions_daily.yaml",
    )

    report_task = PythonOperator(
        task_id="generate_downstream_report",
        python_callable=generate_downstream_report,
    )

    extract_task >> validate_task >> report_task