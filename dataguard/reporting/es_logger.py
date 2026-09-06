import os
from datetime import datetime, timezone
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()

INDEX_NAME = "dataguard-validation-results"


def get_es_client() -> Elasticsearch:
    """
    Membuat koneksi ke Elasticsearch menggunakan alamat dari .env
    """
    es_host = os.getenv("ELASTICSEARCH_HOST")
    return Elasticsearch(es_host)


def log_validation_result(validation_result: dict) -> None:
    """
    Mengirim hasil validasi ke Elasticsearch, dengan tambahan timestamp
    supaya bisa dilacak kapan validasi ini terjadi.
    """
    es = get_es_client()

    document = {
        **validation_result,
        "logged_at": datetime.now(timezone.utc).isoformat(),
    }

    es.index(index=INDEX_NAME, document=document)