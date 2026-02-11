
# Lab 04 — GRC Baseline System (Control Exists)

## What this lab is
A baseline “good” system designed to be assessed:
- `/register` creates a user (server controls role assignment)
- `/login` issues a session cookie (stateful auth)
- `/me` shows authenticated identity
- `/api/posts` CRUD scoped to the authenticated user (ownership enforced)
- `/admin` is admin-only (least privilege)

Runs in CLI. 

## Why it matters (cybersecurity education)
This is the bridge from “HTTP knowledge” to “control verification”:
- prove authentication works
- prove authorisation works (role + ownership)
- capture evidence using curl transcripts

## GRC alignment
- Asset identification: endpoints + data objects are explicit
- Controls: authentication, authorisation, deny-by-default routing
- Evidence: saved curl outputs support audit traceability
- Baseline state: establishes “expected secure behaviour” before introducing vulnerabilities

## Outcomes
You can produce evidence of:
- unauthenticated access denied (401)
- authenticated access allowed (200)
- admin access denied for normal user (403)
- object-level access enforced (403)

## License

This project is licensed under CC BY-NC 4.0.

You may use and adapt these labs for learning and non-commercial educational purposes.
Commercial resale or inclusion in paid training requires permission.

