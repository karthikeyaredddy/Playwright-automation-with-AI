import pytest
import sys

PRIORITY_TESTS = {
    "smoke": [
        "tests/test_login.py",
        "tests/test_dashboard.py",
    ],
    "high": [
        ""
    ],
    "all": [
        "tests/test_login.py",
        "tests/test_dashboard.py",
        "tests/test_fieldexecutivedashboard.py",
        "tests/test_route.py",
        "tests/test_meetvisits.py",
        "tests/test_HREM.py",
        "tests/test_partnerusermanagement.py",
        "tests/test_partnerverification.py",
        "tests/test_claim_eligibility.py",
        "tests/test_policiesandprocedures.py",
        "tests/test_leavemanagement.py"
    ],
    "firstweek": [
        "tests/test_login.py",
        "tests/test_route.py",
        "tests/test_policiesandprocedures.py",
    ],
    "secondweek": [
        "tests/test_login.py",
        "tests/test_leavemanagement.py",
        #employeepolicies integrated with policiesandprocedures
    ],

}

if __name__ == "__main__":
    priority = sys.argv[1] if len(sys.argv) > 1 else "all"

    if priority not in PRIORITY_TESTS:
        print(f"Unknown priority: {priority}")
        print(f"Available priorities: {', '.join(PRIORITY_TESTS)}")
        sys.exit(1)

    test_files = PRIORITY_TESTS[priority]

    pytest.main([
        "-v",
        "-s",
        "--no-header",
        *test_files,
    ])
