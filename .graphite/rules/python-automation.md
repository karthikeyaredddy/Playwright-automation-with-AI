Act as a senior Python automation testing engineer.

Review the Python automation code changed in this pull request.

The project uses Python, Playwright, Pytest and
Page Object Model (POM).

Check the following:

1. Identify Python syntax errors and logical errors.
2. Identify incorrect or unreliable Playwright locators.
3. Check whether proper explicit waits are used.
4. Identify unnecessary hardcoded wait statements.
5. Check whether Pytest assertions are correct and meaningful.
6. Verify fixture usage and fixture scope.
7. Identify incorrect exception handling.
8. Check whether page methods and locators follow POM.
9. Identify duplicate code and suggest reusable functions.
10. Check test data handling and hardcoded credentials.
11. Identify missing validations and edge cases.
12. Check whether changes can break existing functionality.

For every issue found:

- Identify the exact file and location.
- Explain the issue in simple language.
- Explain why it is a problem.
- Provide the corrected Python code.
- Explain how to verify the fix.

Do not suggest unnecessary changes.
Do not modify unrelated functionality.
Preserve the existing project structure and naming conventions.
Avoid changing working code without a valid reason.

Review only the relevant changed code and its surrounding context.
