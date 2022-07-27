import itertools
from datetime import date, timedelta, datetime
from uuid import UUID

import pytest
from django.contrib.auth.models import User
from model_bakery import baker, seq
from rest_framework.test import APIClient

from bookings.models import Booking
from gtfs.models import Agency, Departure, Route, Stop, StopTime, Trip
from gtfs.tests.utils import get_feed_for_maas_operator
from maas.models import MaasOperator, TicketingSystem
from maas.tests.utils import token_authenticate


@pytest.fixture
def user1():
    return baker.make(User, username='user1', _quantity=1)


@pytest.fixture
def maas_operator(user1):
    return baker.make(
        MaasOperator,
        name=seq("name of maas operator "),
        identifier=seq("identifier of maas operator "),
        users=user1
    )


@pytest.fixture
def ticketing_system(user1):
    return baker.make(
        TicketingSystem,
        name=seq("name of ticketing system "),
        users=user1
    )


@pytest.fixture
def booking(ticketing_system, maas_operator):
    booking = baker.make(
        Booking,
        maas_operator=maas_operator,
        agency_name="Test agency name",
        ticketing_system=ticketing_system,
    )
    booking.created_at = datetime(2022, 7, 27, 0, 0)
    booking.save()
    return booking


@pytest.fixture
def second_maas_operator():
    user = baker.make(User, username='user2', _quantity=1)
    return baker.make(
        MaasOperator,
        name=seq("name of maas operator 2"),
        identifier=seq("identifier of maas operator 2"),
        users=user
    )


@pytest.fixture
def maas_api_client(maas_operator):
    api_client = APIClient()
    token_authenticate(api_client, maas_operator.users.first())
    api_client.maas_operator = maas_operator
    return api_client


@pytest.fixture
def maas_unauthenticated_api_client():
    api_client = APIClient()
    return api_client


@pytest.fixture
def api_id_generator():
    return (UUID(int=i) for i in itertools.count())


@pytest.fixture
def route_for_maas_operator(maas_operator, api_id_generator):
    feed = get_feed_for_maas_operator(maas_operator, True)

    agency = baker.make(
        Agency,
        feed=feed,
        name="test agency",
        url="www.testagency.com",
        logo_url="www.testagency.com/logo",
        timezone="Europe/Helsinki",
        email="test-agency@example.com",
        phone="777777",
    )

    route = baker.make(
        Route,
        feed=feed,
        api_id=api_id_generator,
        agency=agency,
        desc="desc of test route ",
        url="url of test route ",
        capacity_sales=Route.CapacitySales.DISABLED,
    )

    return route


@pytest.fixture
def route_for_second_tsp(second_maas_operator, api_id_generator):
    feed = get_feed_for_maas_operator(maas_operator, False)

    agency = baker.make(
        Agency,
        feed=feed,
        name="test agency 2",
        url="www.testagency.com",
        logo_url="www.testagency.com/logo",
        timezone="Europe/Helsinki",
        email="test-agency@example.com",
        phone="777777",
    )

    route = baker.make(
        Route,
        feed=feed,
        api_id=api_id_generator,
        agency=agency,
        desc="desc of test route 2",
        url="url of test route 2",
        capacity_sales=Route.CapacitySales.DISABLED,
    )

    return route


@pytest.fixture
def stops_from_second_tsp(api_id_generator, route_for_second_tsp):
    """
    A route with 2 stops
    """
    feed = route_for_second_tsp.feed

    stops = baker.make(
        Stop,
        feed=feed,
        api_id=api_id_generator,
        name="stop ",
        tts_name="tts_name of stop ",
        code=seq("code of stop"),
        desc="desc of test stop ",
        _quantity=2,
    )

    return stops


@pytest.fixture
def route_with_departures(api_id_generator, route_for_maas_operator):
    """
    A route with
        * 2 trips:
          - #1: stop #1 13:00 -> stop #2 14:00
          - #2: stop #2 00:00 -> stop #1 01:00
        * 3 departures:
          - #1: trip #1 2021-02-18
          - #2: trip #2 2021-02-18
          - #3: trip #1 2021-02-19
    """
    route = route_for_maas_operator
    feed = route_for_maas_operator.feed

    trips = baker.make(
        Trip,
        route=route,
        feed=feed,
        source_id="source_id of test trip ",
        short_name="short_name of test trip ",
        headsign="headsign of test trip ",
        direction_id=itertools.cycle([0, 1]),
        block_id=seq("block_id of test trip "),
        _quantity=2,
    )

    stops = baker.make(
        Stop,
        feed=feed,
        api_id=api_id_generator,
        name="stop ",
        tts_name="tts_name of stop ",
        code=seq("code of stop"),
        desc="desc of test stop ",
        _quantity=2,
    )
    for i, trip in enumerate(trips):
        baker.make(
            StopTime,
            trip=trip,
            stop=iter(stops) if i % 2 == 0 else reversed(stops),
            feed=feed,
            # 13:00 -> 14:00, 00:00 -> 01:00 in Helsinki time
            arrival_time=iter(
                [
                    timedelta(hours=15 + i * 11),
                    timedelta(hours=15 + i * 11 + 1),
                ]
            ),
            # 13:00 -> 14:00, 00:00 -> 01:00 in Helsinki time
            departure_time=iter(
                [
                    timedelta(hours=15 + i * 11),
                    timedelta(hours=15 + i * 11 + 1),
                ]
            ),
            stop_headsign="stop_headsign of test stop time ",
            stop_sequence=seq(0),
            timepoint=StopTime.Timepoint.EXACT,
            _quantity=2,
        )

    departures = baker.make(
        Departure,
        api_id=api_id_generator,
        trip=iter(trips),
        date=date(2021, 2, 18),
        _quantity=2,
    )
    departures.append(
        baker.make(
            Departure,
            api_id=api_id_generator,
            trip=trips[0],
            date=date(2021, 2, 19),
        )
    )

    for trip in trips:
        trip.populate_stop_times_stops_after_this()

    return route
