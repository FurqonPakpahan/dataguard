import yaml
from pathlib import Path


def load_contract(contract_path: str) -> dict:
    """
    Membaca file kontrak YAML dan mengembalikannya sebagai dictionary Python.

    Args:
        contract_path: path menuju file .yaml kontrak

    Returns:
        dict berisi isi kontrak (contract_name, table, rules, dst)
    """
    path = Path(contract_path)

    if not path.exists():
        raise FileNotFoundError(f"Contract file not found: {contract_path}")

    with open(path, "r") as f:
        contract = yaml.safe_load(f)

    return contract