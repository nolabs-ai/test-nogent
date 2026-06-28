# Reviewing this repository

This repo is a small **Python / Flask web service**. It is *not* a Rust crate
and has nothing to do with sandboxing, Landlock, Seatbelt, FFI, or
capability-based isolation — ignore any guidance in the base reviewer prompt
that assumes that domain.

## Focus

Treat this as a web-app code review. The high-value finding categories here
are:

- **Web vulns:** SQL injection, command injection, path traversal, open
  redirects, SSRF, XSS, CSRF, unsafe deserialization, insecure direct object
  references.
- **Auth / credentials:** hardcoded secrets, plaintext password storage,
  non-constant-time comparisons, weak/predictable tokens, missing rate
  limiting, secrets in URLs/query strings.
- **Cryptography:** non-CSPRNG sources for security-sensitive values, weak
  algorithms, missing iv/nonce reuse checks.
- **Input handling:** missing type/shape validation on `request.json` /
  `request.args`, unbounded sizes, eval/exec on user input.
- **Runtime posture:** `debug=True`, verbose error pages, listening on
  `0.0.0.0` without intent, swallowed exceptions, info disclosure via error
  messages.
- **Python correctness:** mutable default arguments, `== None` vs `is None`,
  resource leaks (unclosed files/connections), race conditions on shared
  module-level state.

## What not to report

- Style nits, import ordering, formatting (e.g. line length) — out of scope.
- Library version pinning / supply-chain concerns — handled separately.
- "This is a prototype, consider tests" type suggestions — we know.

## Severity

Use `high` for anything an unauthenticated attacker can exploit remotely
(injection, RCE, auth bypass). Use `medium` for issues that require an
adjacent foothold or are latent. `low` for correctness bugs that have no
security impact.
