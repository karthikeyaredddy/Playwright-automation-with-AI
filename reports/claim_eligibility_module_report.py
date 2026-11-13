
import subprocess
import sys
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).resolve().parent.parent

# Create the HTML reports directory
report_dir = project_root / "reports" / "html"
report_dir.mkdir(parents=True, exist_ok=True)

# Define the HTML report file
report_file = report_dir / "claim_eligibility_report.html"

# Define the test file
test_file = project_root / "tests" / "test_claim_eligibility.py"

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

print(f"\nClaim Eligibility HTML report saved at:\n{report_file.resolve()}")

sys.exit(result.returncode)
