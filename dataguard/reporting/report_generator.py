from datetime import datetime, timezone


def generate_incident_report(validation_result: dict) -> str:
    """
    Mengubah hasil validasi (dictionary) menjadi laporan insiden
    dalam format Markdown yang mudah dibaca manusia.
    """
    contract_name = validation_result["contract_name"]
    table = validation_result["table"]
    total_rows = validation_result["total_rows_checked"]
    overall_passed = validation_result["overall_passed"]
    check_results = validation_result["check_results"]

    failed_checks = [c for c in check_results if c["passed"] is False]

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    status_label = "✅ PASSED" if overall_passed else "❌ FAILED"

    lines = [
        f"# Data Quality Incident Report",
        f"",
        f"**Contract:** `{contract_name}`",
        f"**Table:** `{table}`",
        f"**Generated at:** {timestamp}",
        f"**Overall Status:** {status_label}",
        f"**Total Rows Checked:** {total_rows}",
        f"",
    ]

    if not failed_checks:
        lines.append("No violations detected. All data quality checks passed.")
        return "\n".join(lines)

    lines.append(f"## Summary")
    lines.append(f"")
    lines.append(f"{len(failed_checks)} check(s) failed out of {len(check_results)} total checks.")
    lines.append(f"")
    lines.append(f"## Violation Details")
    lines.append(f"")

    for i, check in enumerate(failed_checks, start=1):
        lines.append(f"### {i}. {check['check_type']} on column `{check['column']}`")
        lines.append(f"")
        lines.append(f"**Detail:** {check['detail']}")
        lines.append(f"")

        violating_rows = check.get("violating_rows", [])
        if violating_rows:
            sample_size = min(3, len(violating_rows))
            lines.append(f"**Sample affected row(s)** (showing {sample_size} of {len(violating_rows)}):")
            lines.append(f"")
            for row in violating_rows[:sample_size]:
                lines.append(f"- `{dict(row)}`")
            lines.append(f"")

    return "\n".join(lines)


def save_report_to_file(report_content: str, output_path: str) -> None:
    """
    Menyimpan laporan insiden ke file.
    """
    with open(output_path, "w") as f:
        f.write(report_content)