#!/usr/bin/env python3
"""vuln_report_check.py - completeness validator for vulnerability reports.

Checks a draft report (Markdown or plain text) against the sections and
statements that reviewers actually reject reports for missing:

  title                 a title line naming the problem
  boundary              a boundary statement sourced from the project's own
                        documentation, threat model, or security policy
  versions              affected versions, with at least one concrete version
  reproduction          reproduction steps with a fenced code block or script
  control               a benign control run beside the proof
  anchor                an anchor comparison: the fixed or unaffected version
                        where the same proof does not trigger
  dedup                 a deduplication note: what was searched, and the result
  impact                an impact section with a capability sentence stating
                        what the attacker gains that they did not already have
  severity              a severity statement (CVSS score or named level)
  preconditions         preconditions and required attacker position
  fix                   a suggested fix or mitigation

Usage:
  python3 vuln_report_check.py REPORT [--strict]

Exit code is 0 when every required check passes, 1 otherwise.
With --strict, warnings also fail the run.

The validator checks for the presence and shape of content. It cannot check
that the content is true. That part is still yours.
"""

import re
import sys

CHECKS = [
    (
        "title",
        "Title line",
        lambda t: bool(re.search(r"^#\s+\S", t, re.M)) or len(t.strip().splitlines()[0]) > 10 if t.strip() else False,
        "Start the report with a title that names the problem in one line.",
    ),
    (
        "boundary",
        "Boundary statement from the project's own docs",
        lambda t: bool(re.search(r"boundar|intended behavio|threat model", t, re.I))
        and bool(re.search(r"SECURITY\.md|documentation|docs|security policy", t, re.I)),
        "State what the project documents as intended behaviour, and cite the "
        "source (SECURITY.md, docs, threat model). If the behaviour is "
        "documented as intended, it is not a vulnerability.",
    ),
    (
        "versions",
        "Affected versions, concretely named",
        lambda t: bool(re.search(r"affected|versions?", t, re.I)) and bool(re.search(r"\d+\.\d+(\.\d+)?", t)),
        "Name the affected versions with at least one concrete version number, "
        "and how the range was established.",
    ),
    (
        "reproduction",
        "Reproduction with a runnable artifact",
        lambda t: bool(re.search(r"reproduc|steps to reproduce|proof of concept|\bPoC\b", t, re.I))
        and "```" in t,
        "Give ordered reproduction steps and a fenced code block or script a "
        "reviewer can run as-is.",
    ),
    (
        "control",
        "Benign control beside the proof",
        lambda t: bool(re.search(r"\bcontrol\b", t, re.I)),
        "Run the same steps with the trigger removed and report the result. "
        "A proof without its control is an anecdote.",
    ),
    (
        "anchor",
        "Anchor comparison against the fixed or unaffected version",
        lambda t: bool(re.search(r"anchor|fixed version|patched|negative test|does not trigger|not affected", t, re.I)),
        "Run the identical proof against the claimed fixed or unaffected "
        "version and state that it does not trigger there. If it does, that "
        "is a separate incomplete-fix finding.",
    ),
    (
        "dedup",
        "Deduplication note",
        lambda t: bool(re.search(r"dedup|duplicat|already (reported|known|filed)|existing (issue|advisory)|searched", t, re.I)),
        "Say what you searched before filing (advisory database, issues, "
        "changelog, the project's own tracker) and what you found.",
    ),
    (
        "impact",
        "Impact as a demonstrated capability",
        lambda t: bool(re.search(r"impact", t, re.I))
        and bool(re.search(r"(attacker|requester|unauthenticated user|any user).{0,80}\bcan\b|\ballows\b.{0,80}\bto\b", t, re.I | re.S)),
        "State the impact as what the attacker gains that they did not "
        "already have, demonstrated end to end. A crash or an error message "
        "is not impact.",
    ),
    (
        "severity",
        "Severity stated once, with its basis",
        lambda t: bool(re.search(r"CVSS", t, re.I)) and bool(re.search(r"\b\d\.\d\b", t))
        or bool(re.search(r"severity\s*[:\-]?\s*(critical|high|medium|low)", t, re.I)),
        "State the severity once, with the vector or the reasoning. Score "
        "from the proven impact, never from the size of the crash.",
    ),
    (
        "preconditions",
        "Preconditions and attacker position",
        lambda t: bool(re.search(r"precondition|prerequisite|requires|attacker position", t, re.I)),
        "List what must be true for the proof to work: accounts, "
        "configuration, network position, non-default settings.",
    ),
    (
        "fix",
        "Suggested fix or mitigation",
        lambda t: bool(re.search(r"suggested fix|remediat|mitigat|\bfix\b", t, re.I)),
        "Offer the smallest fix you can state in two or three sentences, or "
        "the mitigation a user can apply today.",
    ),
]


def check(text):
    results = []
    for key, label, fn, hint in CHECKS:
        try:
            ok = bool(fn(text))
        except Exception:
            ok = False
        results.append((key, label, ok, hint))
    return results


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    strict = "--strict" in argv
    if len(args) != 1:
        print("usage: vuln_report_check.py REPORT [--strict]", file=sys.stderr)
        return 2
    try:
        text = open(args[0], encoding="utf-8", errors="ignore").read()
    except OSError as e:
        print(f"cannot read {args[0]}: {e}", file=sys.stderr)
        return 2
    results = check(text)
    passed = 0
    for key, label, ok, hint in results:
        print(f"{'PASS' if ok else 'FAIL'}  {label}")
        if ok:
            passed += 1
        else:
            print(f"      -> {hint}")
    total = len(results)
    print(f"\n{passed}/{total} checks passed")
    if passed == total:
        print("RESULT: PASS - the draft carries every required element")
        return 0
    print("RESULT: FAIL - fix the FAIL lines before this report goes anywhere")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
