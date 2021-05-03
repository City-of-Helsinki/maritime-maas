from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from bookings.models import Booking
from bookings.serializers import BookingSerializer


class BookingViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = BookingSerializer
    lookup_field = "api_id"

    def get_queryset(self):
        return Booking.objects.for_maas_operator(self.request.user.maas_operator)

    @action(detail=True, methods=["post"])
    def confirm(self, request, api_id=None):
        booking = self.get_object()
        tickets = booking.confirm()

        booking_data = self.serializer_class(instance=booking).data
        booking_data["tickets"] = tickets

        return Response(booking_data)
