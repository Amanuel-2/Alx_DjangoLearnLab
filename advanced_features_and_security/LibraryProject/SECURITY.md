Security hardening applied

Summary of changes:

- `LibraryProject/settings.py`
  - `DEBUG` now respects the `DJANGO_DEBUG` environment variable (defaults to False).
  - Added `SECURE_BROWSER_XSS_FILTER`, `X_FRAME_OPTIONS`, `SECURE_CONTENT_TYPE_NOSNIFF`.
  - Set `CSRF_COOKIE_SECURE` and `SESSION_COOKIE_SECURE` to True.
  - Added example `CSP_POLICY` and registered a simple middleware to set the header.

- `LibraryProject/middleware.py` - simple middleware to set `Content-Security-Policy` header.
- Templates for forms now include `{% csrf_token %}` to protect against CSRF.

Notes and testing:

- Run migrations and use a secure HTTPS-enabled deployment when enabling cookie security.
- To test CSP, inspect the response headers in the browser devtools Network tab and confirm
  `Content-Security-Policy` is present.
- Use `django-csp` for production-grade CSP configuration.
