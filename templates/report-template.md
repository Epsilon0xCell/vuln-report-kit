# <Product and version>: <the problem in one line>

## Summary

<Three or four sentences. What the flaw is, who it affects, and what the
attacker gains. Write this last, when the rest is true.>

## Boundary

<What the project's own documentation, SECURITY.md, or threat model says is
intended behaviour in this area, quoted or closely paraphrased with the source
named. Then one sentence: why this behaviour falls outside that boundary.
If it does not fall outside, stop: this is a bug report, not a vulnerability
report, and it should be filed as one.>

## Affected versions

<Tested version(s), the affected range, and how the range was established:
release testing, an introducing commit, or an honest "earliest affected
version unknown because" with the reason.>

## Preconditions

<Accounts, configuration, network position, non-default settings. Everything
that must be true for the reproduction to work.>

## Reproduction

<Ordered steps a reviewer can follow as-is, plus the runnable artifact:>

```text
<commands or script, exactly as run>
```

## Control

<The same steps with the trigger removed, and the result. The control is what
turns the reproduction from an anecdote into evidence.>

## Anchor comparison

<The identical proof run against the claimed fixed or unaffected version,
and the result. It must not trigger there. If it does, that is a separate
incomplete-fix report, not a footnote in this one.>

## Impact

<One capability sentence: the attacker, who starts authorised for X, can
<gain> Y. Then the demonstration: the impact shown end to end, not argued
from proximity. A crash is not impact. An error message is not impact.>

## Severity

<Stated once. CVSS score with its vector, or a named level with the reasoning.
The score follows the proven impact and the preconditions above.>

## Deduplication

<What was searched before filing: the advisory database, the project's
issues and pull requests, the changelog, recent commits, in that order where
possible, and what was found. Name the nearest existing report and how this
one differs, or state plainly that none exists.>

## Suggested fix

<The smallest change that closes the hole, in two or three sentences, or the
mitigation a user can apply today.>

## Credit

<Your name and contact, as you want them to appear.>
