# Contributing

The kit encodes one campaign's hard-won reporting discipline. Contributions that sharpen it are welcome; contributions that soften it into generic advice are not.

## New checks

A new validator check merges when it corresponds to a real rejection: a report closed, a maintainer complaint, or a policy requirement, with the case stated in the pull request. The check must ship with a failing fixture (a sample that fails only on that element) and a passing one, in the style of the existing single-element-removal test.

## Template changes

Template wording changes should come from reports actually sent: what a maintainer asked for that the template did not prompt, or what the template prompted that no reviewer ever used.

## Style and scope

- The validator stays dependency-free and single-file. That is a feature: it runs anywhere Python 3 does, including restricted VMs.
- Checks judge presence and shape, never truth, and their messages must say so honestly. No check may claim to verify that a reproduction actually works.
- Plain prose, short sentences, no filler.
