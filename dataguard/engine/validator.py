from dataguard.contracts.loader import load_contract
from dataguard.engine.db import fetch_all_rows
from dataguard.engine import checks

# Pemetaan: nama 'type' di YAML -> fungsi Python yang sesuai
CHECK_REGISTRY = {
    "not_null": checks.check_not_null,
    "unique": checks.check_unique,
    "value_range": checks.check_value_range,
    "allowed_values": checks.check_allowed_values,
}


def run_validation(contract_path: str) -> dict:
    """
    Menjalankan validasi penuh berdasarkan sebuah file kontrak YAML.

    Alurnya:
    1. Baca kontrak YAML
    2. Ambil data dari tabel yang disebutkan di kontrak
    3. Untuk tiap kolom & check yang didefinisikan, jalankan fungsi check yang sesuai
    4. Kumpulkan semua hasil jadi satu laporan
    """
    contract = load_contract(contract_path)
    table_name = contract["table"]
    rows = fetch_all_rows(table_name)

    check_results = []

    for rule in contract["rules"]:
        column = rule["column"]

        for check_def in rule["checks"]:
            check_type = check_def["type"]

            # Ambil semua parameter tambahan selain 'type' (misal: max_null_percentage, min, max, values)
            params = {k: v for k, v in check_def.items() if k != "type"}

            check_function = CHECK_REGISTRY.get(check_type)

            if check_function is None:
                # Kalau ada type yang belum kita implementasikan (misal 'data_type'),
                # kita catat sebagai 'skipped', bukan bikin program crash
                check_results.append({
                    "check_type": check_type,
                    "column": column,
                    "passed": None,
                    "detail": f"Check type '{check_type}' is not yet implemented, skipped",
                    "violating_rows": [],
                })
                continue

            result = check_function(rows, column, **params)
            check_results.append(result)

    overall_passed = all(r["passed"] for r in check_results if r["passed"] is not None)

    return {
        "contract_name": contract["contract_name"],
        "table": table_name,
        "total_rows_checked": len(rows),
        "overall_passed": overall_passed,
        "check_results": check_results,
    }