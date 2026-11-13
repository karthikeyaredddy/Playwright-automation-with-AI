
import subprocess
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
report_dir = project_root / "reports" / "html"
report_dir.mkdir(parents=True, exist_ok=True)

report_file = report_dir / "policies_procedures_report.html"
test_file = project_root / "tests" / "test_policiesandprocedures.py"

command = [
    sys.executable,
    "-m",
    "pytest",
    str(test_file),
    f"--html={report_file}",
    "--self-contained-html",
]

result = subprocess.run(command, cwd=project_root)

print(f"\nPolicies HTML report: {report_file.resolve()}")

sys.exit(result.returncode)
