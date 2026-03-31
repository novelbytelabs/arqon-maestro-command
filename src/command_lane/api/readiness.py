from pathlib import Path


DEPENDENCY_AUDIT_REPORT = Path("artifacts/reports/dependency-audit.md")


def get_dependency_audit() -> dict:
    text = DEPENDENCY_AUDIT_REPORT.read_text() if DEPENDENCY_AUDIT_REPORT.exists() else ""
    deferred_count = text.count("deferred")
    return {
        "report_path": str(DEPENDENCY_AUDIT_REPORT),
        "blocked": deferred_count > 0,
        "deferred_count": deferred_count,
    }
