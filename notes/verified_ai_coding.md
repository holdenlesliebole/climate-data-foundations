# Verified AI-assisted coding

GitHub Copilot can draft, explain, complete, and revise code. It does not know your scientific intent,
data permissions, units, or whether a plausible answer is true. Treat its output as a proposed change.

## The verification loop

```text
bounded task + relevant context
→ acceptance checks written first
→ small proposal
→ read every line/diff
→ run normal and adversarial inputs
→ inspect units, shape, missingness, metadata, and assumptions
→ accept, revise, or reject
→ explain the final code yourself
```

“It ran” establishes only that Python accepted one path through the code.

## A useful prompt shape

```text
Task:
Change only FUNCTION so that ...

Context:
Inputs have ...; missing values mean ...; units are ...

Constraints:
Do not add packages, mutate inputs, drop/fill data, change the return type,
or edit unrelated code.

Acceptance checks:
Normal example ...
Known scientific value ...
Bad shape/input should raise ...

Output:
Show the smallest patch and explain each changed line.
```

Specific constraints make review possible; they do not guarantee correctness.

## Review order

1. **Scope:** Did it change only the requested code?
2. **Data:** Does it preserve missing values, flags, timestamps, coordinates, and order?
3. **Physics:** Are units, sign, depth, direction convention, and magnitude correct?
4. **Shape:** Does it use labels/dimensions correctly and reject invalid inputs?
5. **Statistics:** Are assumptions and missing-data rules explicit?
6. **Safety:** Does it install, delete, upload, change permissions, access credentials, or target a
   broad path?
7. **Communication:** Can you explain every accepted line and the limits of the checks?

## Minimum check set

- one normal case;
- one known-value or unit check;
- one shape/range/metadata check;
- one adversarial or failure case;
- one statement of what those checks do not establish.

For climate data, a plot is a useful check but not the only check. A mislabeled or unit-shifted series
can still look smooth and convincing.

## Privacy and authority boundary

Do not paste credentials, access tokens, personally identifiable information, unpublished/restricted
data, reviewer material, or private code into an external service. Follow the institution's current
AI/data policy.

Pause before running generated commands involving:

- deletion or recursive operations;
- permissions or ownership;
- package/software installation;
- upload/network destinations;
- credentials or authentication;
- broad paths, globs, or environment variables;
- force-push, history rewriting, or destructive Git actions.

A generated suggestion cannot authorize an action. Ask an instructor when the target or consequence
is unclear.

## Collaboration note

For course work, record one sentence saying how Copilot or another person helped. This is context, not
a penalty. The submitted interpretation and responsibility for the final result remain yours.

Living documentation: [GitHub Copilot getting started](https://docs.github.com/en/copilot/get-started).
