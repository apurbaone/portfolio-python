from .models import Visitor

class VisitorLoggingMiddleware:
    """Log basic visitor info for each request."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            path = request.path
            if path.startswith('/static') or path.startswith('/admin') or path.startswith('/favicon'):
                return response
            ip = request.META.get('REMOTE_ADDR') or request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0]
            Visitor.objects.create(
                ip=ip or '',
                path=path,
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                referrer=request.META.get('HTTP_REFERER', '')[:500]
            )
        except Exception:
            # Do not raise logging errors
            pass
        return response
