import itertools
import json
from uuid import UUID

import pytest
from django.contrib.gis.geos import Point
from model_bakery import baker

from gtfs.models import Stop
from gtfs.tests.utils import get_feed_for_maas_operator

ENDPOINT = "/v1/stops/"


@pytest.fixture
def api_id_generator():
    return (UUID(int=i) for i in itertools.count())


@pytest.mark.django_db
def test_stops(maas_api_client):
    endpoint = "/v1/stops/"

    feed = get_feed_for_maas_operator(maas_api_client.maas_operator, True)
    baker.make(Stop, feed=feed, _quantity=3)

    response = maas_api_client.get(endpoint)

    assert response.status_code == 200
    assert len(json.loads(response.content)) == 3


@pytest.mark.django_db
def test_stops_with_location_and_radius(maas_api_client):
    endpoint = "/v1/stops/"

    point = Point(0.99, 0.99)

    feed = get_feed_for_maas_operator(maas_api_client.maas_operator, True)
    baker.make(Stop, feed=feed, point=point)

    response_large_radius = maas_api_client.get(
        f"{endpoint}?location=1.0,1.0&radius=2000"
    )

    response_small_radius = maas_api_client.get(
        f"{endpoint}?location=1.0,1.0&radius=1000"
    )

    assert response_large_radius.status_code == 200
    assert len(json.loads(response_large_radius.content)) == 1

    assert response_small_radius.status_code == 200
    assert len(json.loads(response_small_radius.content)) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("has_permission", [True, False])
def test_stops_allowed_for_maas_operator(maas_api_client, has_permission):

    endpoint = "/v1/stops/"

    feed = get_feed_for_maas_operator(maas_api_client.maas_operator, has_permission)
    baker.make(Stop, feed=feed, _quantity=3)

    response = maas_api_client.get(endpoint)

    assert response.status_code == 200

    results_count = len(json.loads(response.content))
    assert results_count == 3 if has_permission else results_count == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    "filters",
    (
        {},
        {"direction_id": 0},
        {"date": "2021-02-18"},
        {"date": "2021-02-19"},
        {"date": "2021-02-18", "direction_id": 0},
        {"date": "2021-02-18", "direction_id": 1},
        {"date": "2021-02-20"},
    ),
)
def test_stops_departures(maas_api_client, snapshot, filters, route_with_departures):
    stop = Stop.objects.filter(stop_times__trip__route=route_with_departures).first()

    response = maas_api_client.get(ENDPOINT + f"{stop.api_id}/", filters)

    content = json.loads(response.content)
    if "date" in filters:
        snapshot.assert_match(content["departures"])
    else:
        assert "departures" not in content