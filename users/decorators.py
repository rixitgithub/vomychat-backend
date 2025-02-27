from django.core.cache import cache
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from functools import wraps
import time

def ratelimit(key='ip', rate='5/m', method=None):
    """
    Rate-limiting decorator.
    key: What to limit by (e.g., 'ip' or 'user')
    rate: String specifying the maximum number of requests allowed in a time period
          e.g., '5/m' means 5 requests per minute
    method: Optional HTTP method to apply rate limiting to. If None, applies to all methods.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            # Parse rate
            count, period = rate.split('/')
            count = int(count)
            
            if period == 's':
                period_seconds = 1
            elif period == 'm':
                period_seconds = 60
            elif period == 'h':
                period_seconds = 3600
            elif period == 'd':
                period_seconds = 86400
            else:
                raise ValueError("Invalid rate period. Use 's', 'm', 'h', or 'd'.")
            
            # Only apply to specified method, if given
            if method and request.method != method:
                return view_func(self, request, *args, **kwargs)
            
            # Get the cache key
            if key == 'ip':
                ident = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
            elif key == 'user' and request.user.is_authenticated:
                ident = str(request.user.id)
            else:
                ident = request.META.get('REMOTE_ADDR', '')
            
            cache_key = f"ratelimit:{ident}:{request.path}"
            
            # Get current request count
            request_history = cache.get(cache_key, [])
            
            # Clean up old requests
            now = time.time()
            cutoff = now - period_seconds
            request_history = [t for t in request_history if t > cutoff]
            
            # Check if too many requests
            if len(request_history) >= count:
                return Response(
                    {"error": "Too many requests, please try again later."},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )
            
            # Add current request and update cache
            request_history.append(now)
            cache.set(cache_key, request_history, period_seconds)
            
            # Process the request
            return view_func(self, request, *args, **kwargs)
        
        return _wrapped_view
    
    return decorator