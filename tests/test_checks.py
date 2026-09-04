from dataguard.engine.checks import (
    check_not_null,
    check_unique,
    check_value_range,
    check_allowed_values,
)


def test_check_not_null_passes_when_no_nulls():
    rows = [{"amount": 100}, {"amount": 200}]
    result = check_not_null(rows, "amount", max_null_percentage=0)
    assert result["passed"] is True


def test_check_not_null_fails_when_over_threshold():
    rows = [{"amount": 100}, {"amount": None}]
    result = check_not_null(rows, "amount", max_null_percentage=0)
    assert result["passed"] is False
    assert len(result["violating_rows"]) == 1


def test_check_unique_detects_duplicates():
    rows = [
        {"transaction_id": "A"},
        {"transaction_id": "B"},
        {"transaction_id": "A"},
    ]
    result = check_unique(rows, "transaction_id")
    assert result["passed"] is False
    assert len(result["violating_rows"]) == 1


def test_check_unique_passes_when_all_unique():
    rows = [{"transaction_id": "A"}, {"transaction_id": "B"}]
    result = check_unique(rows, "transaction_id")
    assert result["passed"] is True


def test_check_value_range_detects_out_of_range():
    rows = [{"amount": 100}, {"amount": -50}]
    result = check_value_range(rows, "amount", min=0, max=1000)
    assert result["passed"] is False
    assert len(result["violating_rows"]) == 1


def test_check_allowed_values_detects_invalid_value():
    rows = [{"status": "success"}, {"status": "unknown"}]
    result = check_allowed_values(rows, "status", ["success", "pending", "failed"])
    assert result["passed"] is False
    assert len(result["violating_rows"]) == 1
