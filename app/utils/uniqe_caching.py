from django.core.cache import cache
from rest_framework.response import Response
from config.settings.base import CACHE_TTL


def cached_response(view_instance, request, data_source, serializer_class, cache_key_prefix, is_single_object=False):
    """
    Utility function to handle caching for list and retrieve views.

    Args:
        view_instance: The viewset instance
        request: The current HTTP request
        data_source: The queryset for list views or the object instance for retrieve views
        serializer_class: The serializer to serialize the data
        cache_key_prefix: The prefix to use for cache keys (usually the name of the model or view)
        is_single_object: Boolean flag to indicate if the request is for a single object (retrieve) or multiple (list)

    Returns:
        A Response object with the cached or fresh data.
    """
    if is_single_object:
        # For single object retrieval (retrieve view), generate cache key based on object ID and user
        obj_id = view_instance.kwargs.get('pk')
        cache_key = f"{cache_key_prefix}_{request.user.id}_{obj_id}"
    else:
        # For list view, cache based on user ID
        cache_key = f"{cache_key_prefix}_list_{request.user.id}"

    # Check if data is cached
    cached_data = cache.get(cache_key)
    if cached_data:
        return Response(cached_data)

    # Serialize the data (single object or list of objects)
    if is_single_object:
        # For single object, pass the instance directly
        serializer = serializer_class(data_source)
    else:
        # For list, pass the queryset
        serializer = serializer_class(data_source, many=True)

    # Cache the serialized data
    cache.set(cache_key, serializer.data, CACHE_TTL)

    return Response(serializer.data)
