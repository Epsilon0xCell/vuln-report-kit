# WidgetLib 2.4.1: signed download tokens accepted after expiry for the full account

## Summary

WidgetLib verifies the signature on download tokens but not the expiry claim
inside them. A token issued for one file stays valid forever and, because the
file identifier is a plain claim, can be re-pointed at any file in the account.

## Boundary

The project documentation for the token feature states that tokens are
"short-lived, single-file authorisations" and that expiry is enforced by the
library, not the caller. SECURITY.md names token verification as part of the
library's security boundary. Accepting an expired token falls outside that
documented behaviour.

## Affected versions

Tested on 2.4.1 (current release). The flaw is present in 2.3.0, the release
that introduced tokens; 2.2.x has no token feature and is not affected.

## Preconditions

The attacker needs one legitimately issued token for any file in the account.
No other access, configuration change, or non-default setting is required.

## Reproduction

```sh
# 1. Issue a token for file A with the demo app (token expires in 60 seconds)
TOKEN=$(widget-demo issue --file A --ttl 60)
# 2. Wait 120 seconds, then edit the payload claim file_id to file B
#    (the payload is unsigned-editable in the demo harness; signature is
#     computed over the header only in the vulnerable build)
# 3. Redeem
widget-demo redeem --token "$EDITED_TOKEN"   # returns file B's contents
```

## Control

With the token unedited and unexpired, redemption returns file A. With the
token unedited and expired, the vulnerable build still returns file A, which
is the flaw in its smallest form; the edited-token run above shows the full
impact.

## Anchor comparison

The identical edited-token proof run against the tokenless 2.2.x line does
not trigger (the feature does not exist), and against a local build with the
expiry check restored it is rejected with "token expired". 

## Impact

An attacker holding any single expired token can read every file in the
account, including files the token was never issued for. The gain was
demonstrated end to end: file B's contents, which the test account's token
never authorised, were returned and are shown in the run log.

## Severity

CVSS 7.5 (AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N). The score follows from the
demonstrated read access; no write or availability impact is claimed.

## Deduplication

Searched before filing: the GitHub Advisory Database and OSV for WidgetLib
token issues, the project's issue tracker and pull requests for "token" and
"expiry", and the 2.3.0 and 2.4.0 changelogs. No existing report describes
expiry not being enforced; the nearest issue, #412, concerns token length and
is unrelated.

## Suggested fix

Verify the expiry claim inside the signed payload during redemption, and bind
the file identifier into the signed region so claims cannot be re-pointed.
Reject expired tokens with the same error path as bad signatures.

## Credit

Gavin Blacklock, contact via the address this report was sent from.
