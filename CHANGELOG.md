# Changelog

## v0.1.0, 2026-11-12

First release.

- `vuln_report_check.py`: a dependency-free completeness validator that checks a draft report for the eleven elements reviewers reject reports for missing: title line, boundary statement, concrete affected versions, reproduction with a runnable artifact, benign control, anchor comparison, deduplication note, capability-shaped impact, severity with its basis, preconditions, and a suggested fix. Exit code 0 on pass, 1 on fail, with a plain-language remedy printed per failure.
- `templates/report-template.md`: the full report skeleton with the reasoning for each section written into it.
- `templates/cover-note.txt`: a short plain-text cover note for email disclosure routes.
- `samples/`: a complete passing report and a thin failing one, used by the test suite and readable as a contrast pair.
- `tests/`: five unit tests, including a single-element-removal case proving the deduplication check can fail on its own.
