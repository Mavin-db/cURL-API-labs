
# Lab 03 — Stateless Token Auth (Writes Protected)

## What this lab is
A mini API where writes require:
`Authorization: Bearer <token>`

- missing token -> 401
- wrong token -> 403
- correct token -> 201/200

Runs in CLI; output viewable in browser.

## Why it matters (cybersecurity education)
This is the common API pattern in production systems.
It teaches how to validate access controls and interpret 401 vs 403.

## GRC alignment
Enables control verification with clear evidence:
“Unauthorised writes are denied; authorised writes succeed.”

## Outcomes
You can demonstrate a working access gate and produce audit-grade curl transcripts.

## License

This project is licensed under CC BY-NC 4.0.

You may use and adapt these labs for learning and non-commercial educational purposes.
Commercial resale or inclusion in paid training requires permission.

