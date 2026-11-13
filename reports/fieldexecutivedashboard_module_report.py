
import subprocess
import sys
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).resolve().parent.parent

# Create the HTML reports directory
report_dir = project_root / "reports" / "html"
report_dir.mkdir(parents=True, exist_ok=True)

# Define the HTML report file
report_file = report_dir / "fieldexecutivedashboard_report.html"

# Define the test file
test_file = project_root / "tests" / "test_fieldexecutivedashboard.py"

# Run tests and generate the HTML report
command = [
    sys.executable,
    "-m",
    "pytest",
    str(test_file),
    f"--html={report_file}",
    "--self-contained-html",
]

result = subprocess.run(command, cwd=project_root)

print(
    f"\nField Executive Dashboard HTML report saved at:\n"
    f"{report_file.resolve()}"
)

sys.exit(result.returncode)
