from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response

from app.notifications.models import Notification
from app.notifications.serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from app.utils.uniqe_caching import cached_response


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving and listing notifications.
    Delete is restricted to admin users only.
    """
    queryset = Notification.objects.select_related('product').all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminUser]

    @extend_schema(
        operation_id="List Notifications",
        description="Retrieve a list of all notifications",
        responses={200: NotificationSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return cached_response(self, request, queryset, self.get_serializer_class(), 'notifications')

    @extend_schema(
        operation_id="Retrieve Notification",
        description="Retrieve details of a specific notification by ID",
        responses={200: NotificationSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        return cached_response(self, request, obj, self.get_serializer_class(), 'notification', is_single_object=True)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        # Admin-only permission is already enforced by the IsAdminUser permission class
        self.perform_destroy(obj)
        return Response(status=204)

    def perform_destroy(self, instance):
        """
        Custom delete logic, but you can use the default method.
        """
        instance.delete()