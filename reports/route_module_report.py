
import subprocess
import sys
from pathlib import Path

# HTML report location
report_dir = Path("reports/html")
report_dir.mkdir(parents=True, exist_ok=True)

report_file = report_dir / "routes_report.html"

# Execute route tests and generate an HTML report
command = [
    sys.executable,
    "-m",
    "pytest",
    "tests/test_route.py",
    f"--html={report_file}",
    "--self-contained-html",
]

result = subprocess.run(command)

print(f"\nRoute HTML report generated at: {report_file.resolve()}")

sys.exit(result.returncode)
