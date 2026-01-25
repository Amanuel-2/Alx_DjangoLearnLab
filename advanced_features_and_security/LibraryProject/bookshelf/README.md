# Permissions and Groups Setup

This project implements Role-Based Access Control (RBAC) using Django permissions and groups.

## Custom Permissions
Defined in the Book model:
- can_view
- can_create
- can_edit
- can_delete

## Groups
- Viewers: can_view
- Editors: can_view, can_create, can_edit
- Admins: all permissions

## Enforcement
Views are protected using @permission_required decorators.

## Testing
Permissions were tested by logging in as users from each group and verifying access.
403 Forbidden responses confirm correct enforcement.


## Security Best Practices

- DEBUG disabled for production safety
- Secure cookies enforced via HTTPS
- CSRF protection enabled in all forms
- Django ORM used to prevent SQL injection
- Content Security Policy implemented via django-csp




## HTTPS and Security Configuration

This project enforces HTTPS and secure communication using Django security settings.

### Django HTTPS Settings
- SECURE_SSL_REDIRECT redirects all HTTP traffic to HTTPS.
- HSTS headers are enabled to prevent protocol downgrade attacks.
- Secure cookies ensure session and CSRF cookies are only sent over HTTPS.
- Security headers protect against clickjacking, XSS, and MIME sniffing.

### Deployment Notes
In production, HTTPS must be enabled at the web server level.

Example (Nginx):
- Configure SSL certificates using Let's Encrypt.
- Redirect HTTP (port 80) to HTTPS (port 443).
- Forward HTTPS requests to Django via WSGI.

These settings are activated only when DEBUG=False.



## Security Review

### Implemented Measures
- HTTPS enforcement
- Secure cookies
- HTTP security headers
- HSTS policy

### Benefits
- Prevents man-in-the-middle attacks
- Protects authentication cookies
- Mitigates common web vulnerabilities

### Future Improvements
- Content Security Policy (CSP)
- Rate limiting
- Automated security testing
