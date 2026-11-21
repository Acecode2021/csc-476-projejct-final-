# Maintenance Department Portal — CSC 476 prototype

## Project
Automation of Help Desk, Project Tracking and Field Reporting for the Maintenance Department, University of Ibadan.

## Supervisor and course lecturer
Professor Oladejo (CSC 476). HOD has not been confirmed.

## Group
- Ogundele, Tobiloba James — E054654 (team leader)
- Aderinto, Kunle Abraham — E055233
- Olusola, Ayomide Emmanuel — E055067
- Alonge, Ayobami Blessing — E054861

Individual contributions must be completed and approved by the team leader. The presence of a name here does not assign or certify a particular contribution.

## Status
Educational prototype using synthetic records. Not approved for real operational data or production use. No institutional interviews, user acceptance or operational evaluation have been conducted. No remote repository URL has been created or verified.

## Functions
Core ticket submission, assignment, comments and status updates; projects and tasks; simple average progress; field reports optionally linked to tickets; dashboard and ticket filters; login and administrator account creation.

## Dependencies
Python with Flask, Flask-SQLAlchemy, Flask-Login and pytest. HTML/CSS and Jinja2 form the server-rendered interface. SQLite stores records. The demonstration and verification environment used Python 3.13 on Linux.

## Local installation
Run commands inside this directory:

```sh
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows alternative: .venv\Scripts\activate
python -m pip install -r requirements.txt
python seed.py
python -m flask --app app run --host 127.0.0.1 --port 5000 --no-debugger --no-reload
```

Open http://127.0.0.1:5000 on the same computer. The seed script does not overwrite existing user data. Tables are created by the application; sample accounts are created by seed.py.

Demo logins only:
- admin@maintenance.local / admin123
- supervisor@maintenance.local / supervisor123
- tech@maintenance.local / tech123
- staff@maintenance.local / staff123

Do not use these credentials in production. Password resetting is not provided by the current interface.

## Configuration
config.py reads SECRET_KEY and DATABASE_URL from process environment variables. Merely copying .env.example to .env does NOT load that file. Set the variables in your shell or implement a documented loader. The default database is maintenance.db in this application directory. Use a strong private secret and appropriate deployment configuration before any non-demonstration use.

## Tests
```sh
python -m pytest tests/ -v
```
The verification run during report assembly returned 17 passed tests and 166 warnings in 8.24 seconds. Full output: test_evidence/pytest_verification.txt. Tests use an isolated in-memory database. Importing the application can also create its configured demonstration database.

Tests cover selected assertions only. The dashboard test checks rendering/labels, not all totals. The filter test checks status, not every date/priority combination. Technician comment and closure tests do not establish assigned-record restrictions. Passing tests do not imply full authorisation or production security.

## Known limitations
- Incomplete record-level authorisation and dashboard/summary scoping.
- No CSRF protection; input/date/role/linked-record validation incomplete.
- No account editing/deactivation/password-reset interface.
- No complete lifecycle, closure approval or report approval workflow.
- No direct ticket-to-project or report-to-task link.
- Task averaging is unweighted; project completion status is not automatic.
- Production configuration, load, recovery, representative-user usability and cross-browser evaluation remain pending.
- Deprecation warnings require maintenance work.

## Screenshots and documentation
The supplied group report includes eight actual screenshots with synthetic records, architecture and relationship diagrams, test interpretation and installation/user appendices. The screenshot capture helper uses Playwright and a workspace-specific output path; adapt that path and install Playwright/Chromium if reproducing screenshots on another computer. Those optional tools are not needed to run the application.

## Publication
Do not include real databases, credentials or private configuration in a public repository. Confirm licensing and institutional expectations before publishing. Refer to the report for cited literature; this repository does not claim staff participation or institutional approval.
