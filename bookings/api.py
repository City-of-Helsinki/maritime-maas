from collections import defaultdict

from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from rest_framework import generics, mixins, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from bookings.models import Booking
from bookings.serializers import (
    BookingDetailSerializer,
    BookingSerializer,
    PassthroughParametersSerializer,
)
from bookings.ticketing_system import TicketingSystemAPI
from gtfs.models import Departure
from maas.authentication import BearerTokenAuthentication
from maas.permissions import IsMaasOperator


class AvailabilityParamsSerializer(serializers.Serializer):
    departure_ids = serializers.ListField(
        child=serializers.UUIDField(), allow_empty=False
    )


@extend_schema_view(
    create=extend_schema(summary=_("Create a booking")),
    retrieve=extend_schema(summary=_("Retrieve information for a confirmed booking")),
    confirm=extend_schema(summary=_("Confirm a previously created booking")),
    availability=extend_schema(summary=_("List seat availability")),
)
class BookingViewSet(
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Booking.objects.none()  # Empty queryset for drf_spectacular
    serializer_class = BookingSerializer
    lookup_field = "api_id"

    def get_queryset(self):
        return Booking.objects.for_maas_operator(
            self.request.user.maas_operators.first()
        )

    def retrieve(self, request, *args, **kwargs):
        booking = self.get_object()

        passthrough_parameters = PassthroughParametersSerializer(
            data=request.query_params
        )
        passthrough_parameters.is_valid(raise_exception=True)
        tickets = booking.retrieve(passthrough_parameters.validated_data)

        booking_data = self.serializer_class(instance=booking).data
        booking_data["tickets"] = tickets

        return Response(booking_data)

    @action(detail=True, methods=["post"])
    def confirm(self, request, api_id=None):
        booking = self.get_object()

        passthrough_parameters = PassthroughParametersSerializer(data=request.data)
        passthrough_parameters.is_valid(raise_exception=True)
        tickets = booking.confirm(passthrough_parameters.validated_data)

        booking_data = self.serializer_class(instance=booking).data
        booking_data["tickets"] = tickets

        return Response(booking_data)

    @extend_schema(
        request=AvailabilityParamsSerializer,
        responses=inline_serializer(
            "AvailabilityResults",
            many=True,
            fields={
                "departure_id": serializers.UUIDField(),
                "available": serializers.IntegerField(min_value=0),
                "total": serializers.IntegerField(min_value=0, required=False),
            },
        ),
    )
    @action(detail=False, methods=["post"])
    def availability(self, request):
        serializer = AvailabilityParamsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        departures = sorted(
            Departure.objects.for_maas_operator(
                self.request.user.maas_operators.first()
            )
            .filter(api_id__in=serializer.validated_data["departure_ids"])
            .select_related("trip__feed__ticketing_system"),
            key=lambda x: serializer.validated_data["departure_ids"].index(x.api_id),
        )

        # group departures by ticketing system
        departures_by_ticketing_system = defaultdict(list)
        for departure in departures:
            departures_by_ticketing_system[departure.trip.feed.ticketing_system].append(
                departure
            )

        # fetch availability data from all of the involved ticketing systems
        # TODO doing this synchronically like this does not scale, so we probably
        # want to improve this when there are more ticket systems
        availability_data = []
        for ticketing_system, ts_departures in departures_by_ticketing_system.items():
            availability_data.extend(
                TicketingSystemAPI(
                    maas_operator=self.request.user.maas_operators.first(),
                    ticketing_system=ticketing_system,
                ).availability(ts_departures)
            )

        # convert trip + date pairs back to departures
        result = []
        for departure in departures:
            value = next(
                (
                    x
                    for x in availability_data
                    if x["trip_id"] == departure.trip.source_id
                    and x["date"] == departure.date
                ),
                None,
            )
            if value:
                result.append(
                    {
                        "departure_id": departure.api_id,
                        "available": value["available"],
                        "total": value.get("total"),
                    }
                )

        return Response(result)


class BookingFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="created_at", lookup_expr="date__gte")
    end_date = filters.DateFilter(field_name="created_at", lookup_expr="date__lte")
    agency_name = filters.CharFilter(lookup_expr="iexact")
    maas_operator_name = filters.CharFilter(
        field_name="maas_operator__name", lookup_expr="iexact"
    )
    ticketing_system_name = filters.CharFilter(
        field_name="ticketing_system__name", lookup_expr="iexact"
    )
    route_name = filters.CharFilter(field_name="route_name", lookup_expr="iexact")
    locale = filters.CharFilter(field_name="locale", lookup_expr="iexact")

    class Meta:
        model = Booking
        fields = []


class BookingListView(generics.ListAPIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsMaasOperator]
    queryset = Booking.objects.all()
    serializer_class = BookingDetailSerializer
    ordering_fields = [
        "agency_name",
        "maas_operator__name",
        "route_name",
        "locale",
        "ticket_count",
        "status",
        "route_capacity_sales",
    ]
    ordering = ["-created_at"]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookingFilter

    def get_queryset(self):
        maas_operators = self.request.user.maas_operators.values_list("id", flat=True)
        return Booking.objects.for_maas_operators(maas_operators)
