def check_not_null(rows: list[dict], column: str, max_null_percentage: float = 0) -> dict:
    """
    Mengecek apakah suatu kolom punya nilai null melebihi batas yang diizinkan.
    """
    total = len(rows)
    null_rows = [r for r in rows if r.get(column) is None]
    null_count = len(null_rows)
    null_percentage = (null_count / total * 100) if total > 0 else 0

    passed = null_percentage <= max_null_percentage

    return {
        "check_type": "not_null",
        "column": column,
        "passed": passed,
        "detail": f"{null_count} of {total} rows are null ({null_percentage:.2f}%), max allowed: {max_null_percentage}%",
        "violating_rows": null_rows,
    }


def check_unique(rows: list[dict], column: str) -> dict:
    """
    Mengecek apakah semua nilai di suatu kolom itu unik (tidak ada duplikat).
    """
    seen = set()
    duplicates = []

    for row in rows:
        value = row.get(column)
        if value in seen:
            duplicates.append(row)
        else:
            seen.add(value)

    passed = len(duplicates) == 0

    return {
        "check_type": "unique",
        "column": column,
        "passed": passed,
        "detail": f"Found {len(duplicates)} duplicate value(s) in column '{column}'",
        "violating_rows": duplicates,
    }


def check_value_range(rows: list[dict], column: str, min=None, max=None) -> dict:
    """
    Mengecek apakah nilai suatu kolom berada dalam rentang min-max yang diizinkan.
    """
    violations = []

    for row in rows:
        value = row.get(column)
        if value is None:
            continue
        if min is not None and value < min:
            violations.append(row)
        elif max is not None and value > max:
            violations.append(row)

    passed = len(violations) == 0

    return {
        "check_type": "value_range",
        "column": column,
        "passed": passed,
        "detail": f"Found {len(violations)} row(s) outside range [{min}, {max}] in column '{column}'",
        "violating_rows": violations,
    }


def check_allowed_values(rows: list[dict], column: str, values: list) -> dict:
    """
    Mengecek apakah nilai suatu kolom hanya berisi nilai-nilai yang diizinkan.
    """
    violations = [r for r in rows if r.get(column) not in values]

    passed = len(violations) == 0

    return {
        "check_type": "allowed_values",
        "column": column,
        "passed": passed,
        "detail": f"Found {len(violations)} row(s) with value not in {values} in column '{column}'",
        "violating_rows": violations,
    }