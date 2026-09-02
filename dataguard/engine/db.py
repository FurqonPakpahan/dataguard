import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """
    Membuka koneksi ke PostgreSQL menggunakan kredensial dari file .env
    """
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        cursor_factory=RealDictCursor,
    )
    return conn


def fetch_all_rows(table_name: str) -> list[dict]:
    """
    Mengambil semua baris dari sebuah tabel, dikembalikan sebagai list of dict
    (misal: [{'transaction_id': 'TRX001', 'amount': 150000, ...}, ...])
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {table_name}")
            rows = cur.fetchall()
        return rows
    finally:
        conn.close()