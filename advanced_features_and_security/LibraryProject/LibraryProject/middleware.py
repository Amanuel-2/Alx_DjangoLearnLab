"""Simple middleware to add a Content-Security-Policy header.

This is a minimal implementation for demonstration. For more advanced
policies, use the `django-csp` package (recommended) and configure
`CSP_DEFAULT_SRC`, `CSP_SCRIPT_SRC`, etc., in settings.
"""
from django.conf import settings


class ContentSecurityPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        policy = getattr(settings, 'CSP_POLICY', None)
        if policy:
            response.setdefault('Content-Security-Policy', policy)
        return response
