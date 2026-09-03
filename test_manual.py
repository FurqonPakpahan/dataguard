from dataguard.engine.validator import run_validation

result = run_validation("examples/contracts/transactions_daily.yaml")
print("Overall passed:", result["overall_passed"])
print()

for r in result["check_results"]:
    status = "PASSED" if r["passed"] else ("SKIPPED" if r["passed"] is None else "FAILED")
    print(f"{r['check_type']} - {r['column']} - {status}")