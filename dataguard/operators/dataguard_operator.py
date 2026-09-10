from airflow.models import BaseOperator
from airflow.exceptions import AirflowFailException

from dataguard.engine.validator import run_validation
from dataguard.reporting.es_logger import log_validation_result


class DataGuardOperator(BaseOperator):
    """
    Custom Airflow Operator untuk menjalankan validasi data quality
    berdasarkan file kontrak YAML.

    Behavior:
    - Menjalankan validasi terhadap tabel yang didefinisikan di kontrak.
    - Mengirim hasilnya ke Elasticsearch untuk riwayat.
    - Jika ada pelanggaran kontrak, task ini GAGAL (fail-fast),
      sehingga task-task turunan di DAG tidak akan berjalan.
    """

    def __init__(self, contract_path: str, **kwargs):
        super().__init__(**kwargs)
        self.contract_path = contract_path

    def execute(self, context):
        self.log.info(f"Running DataGuard validation using contract: {self.contract_path}")

        result = run_validation(self.contract_path)

        self.log.info(f"Validation result: overall_passed = {result['overall_passed']}")
        for check in result["check_results"]:
            status = "PASSED" if check["passed"] else ("SKIPPED" if check["passed"] is None else "FAILED")
            self.log.info(f"  - {check['check_type']} on '{check['column']}': {status}")

        log_validation_result(result)
        self.log.info("Validation result logged to Elasticsearch.")

        if not result["overall_passed"]:
            raise AirflowFailException(
                f"Data quality contract '{result['contract_name']}' violated. "
                f"Check the incident details above or in Elasticsearch."
            )

        return result