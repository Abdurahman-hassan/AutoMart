from django.core.cache import cache
from config.settings.base import CACHE_TTL
from rest_framework.response import Response


def cached_response(view_instance, method_name, request, *args, **kwargs):
    """
    Utility function to handle caching for list and retrieve views while preserving all ModelViewSet behaviors.

    Args:
        view_instance: The viewset instance.
        method_name: The name of the method being wrapped ('list' or 'retrieve').
        request: The current HTTP request.
        *args: Additional arguments passed to the view.
        **kwargs: Keyword arguments passed to the view.

    Returns:
        A Response object with the cached or fresh data, preserving all behavior of the original method.
    """
    cache_key = f"{view_instance.__class__.__name__}_{request.user.id}_{method_name}_{request.query_params.get('page', 1)}_{kwargs.get('pk', 'all')}"

    # Check if the response is cached
    cached_data = cache.get(cache_key)
    if cached_data:
        return Response(cached_data)

    # Call the original method (e.g., super().list or super().retrieve)
    original_method = getattr(super(view_instance.__class__, view_instance), method_name)
    response = original_method(request, *args, **kwargs)

    # Cache the response data
    cache.set(cache_key, response.data, CACHE_TTL)

    return response
