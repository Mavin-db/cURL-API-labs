
# cURL-API-labs

Hands-on labs to learn HTTP + APIs using `curl` and Python, with a clear path from fundamentals → security controls → GRC-style evidence.

## What you’ll learn
- HTTP methods and status codes (GET/POST/PUT/PATCH/DELETE)
- Headers vs body vs cookies
- Stateless tokens vs stateful sessions
- Authentication vs authorisation
- Deny-by-default routing and predictable API behaviour
- How to capture evidence (curl transcripts) suitable for GRC-style reporting

## Who this is for
- Cybersecurity learners building real API literacy
- Students needing a structured, repeatable lab pack
- GRC-minded practitioners who want technical proof of control verification

## Labs
| Lab | Focus | What you prove |
|---|---|---|
| 01 | cURL + HTTP fundamentals (echo server) | You can see exactly what the server receives |
| 02 | Mini CRUD API (in-memory) | You understand resources, routes, and state change |
| 03 | Stateless bearer token for writes | 401 vs 403 vs 201 and access gates |
| 04 | Baseline “control exists” system (cookie sessions) | AuthN works, AuthZ works, least privilege enforced |

## Quick start
```
cd 01_cURL-API
python3 curl_lab_server.py
# then follow: command.md
```

## Evidence and GRC alignment

Each lab can be run and evidenced using saved curl outputs (e.g. `tee EVIDENCE/*.txt`).
Lab 04 is designed to support a baseline control verification story:

* unauthenticated access denied (401)
* authenticated access allowed (200)
* admin denied for normal user (403)
* object-level access enforced (403)

## License

See `LICENSE`.





