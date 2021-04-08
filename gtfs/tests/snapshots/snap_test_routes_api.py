# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_routes_departures[filters2] 1"] = [
    {
        "arrival_time": "2021-02-18T13:00:00Z",
        "departure_headsign": "headsign of test trip 1",
        "departure_time": "2021-02-18T13:00:00Z",
        "direction_id": 0,
        "id": "00000000-0000-0000-0000-000000000001",
        "short_name": "short_name of test trip 1",
        "stop_headsign": "stop_headsign of test stop time 1",
        "stop_sequence": 1,
    },
    {
        "arrival_time": "2021-02-18T13:15:00Z",
        "departure_headsign": "headsign of test trip 2",
        "departure_time": "2021-02-18T13:15:00Z",
        "direction_id": 1,
        "id": "00000000-0000-0000-0000-000000000002",
        "short_name": "short_name of test trip 2",
        "stop_headsign": "stop_headsign of test stop time 2",
        "stop_sequence": 1,
    },
]

snapshots["test_routes_departures[filters2] 2"] = [
    {
        "arrival_time": "2021-02-18T14:00:00Z",
        "departure_headsign": "headsign of test trip 1",
        "departure_time": "2021-02-18T14:00:00Z",
        "direction_id": 0,
        "id": "00000000-0000-0000-0000-000000000001",
        "short_name": "short_name of test trip 1",
        "stop_headsign": "stop_headsign of test stop time 2",
        "stop_sequence": 2,
    },
    {
        "arrival_time": "2021-02-18T14:15:00Z",
        "departure_headsign": "headsign of test trip 2",
        "departure_time": "2021-02-18T14:15:00Z",
        "direction_id": 1,
        "id": "00000000-0000-0000-0000-000000000002",
        "short_name": "short_name of test trip 2",
        "stop_headsign": "stop_headsign of test stop time 3",
        "stop_sequence": 2,
    },
]

snapshots["test_routes_departures[filters3] 1"] = [
    {
        "arrival_time": "2021-02-19T13:00:00Z",
        "departure_headsign": "headsign of test trip 1",
        "departure_time": "2021-02-19T13:00:00Z",
        "direction_id": 0,
        "id": "00000000-0000-0000-0000-000000000003",
        "short_name": "short_name of test trip 1",
        "stop_headsign": "stop_headsign of test stop time 1",
        "stop_sequence": 1,
    }
]

snapshots["test_routes_departures[filters3] 2"] = [
    {
        "arrival_time": "2021-02-19T14:00:00Z",
        "departure_headsign": "headsign of test trip 1",
        "departure_time": "2021-02-19T14:00:00Z",
        "direction_id": 0,
        "id": "00000000-0000-0000-0000-000000000003",
        "short_name": "short_name of test trip 1",
        "stop_headsign": "stop_headsign of test stop time 2",
        "stop_sequence": 2,
    }
]

snapshots["test_routes_departures[filters4] 1"] = [
    {
        "arrival_time": "2021-02-18T13:00:00Z",
        "departure_headsign": "headsign of test trip 1",
        "departure_time": "2021-02-18T13:00:00Z",
        "direction_id": 0,
        "id": "00000000-0000-0000-0000-000000000001",
        "short_name": "short_name of test trip 1",
        "stop_headsign": "stop_headsign of test stop time 1",
        "stop_sequence": 1,
    }
]

snapshots["test_routes_departures[filters4] 2"] = [
    {
        "arrival_time": "2021-02-18T14:00:00Z",
        "departure_headsign": "headsign of test trip 1",
        "departure_time": "2021-02-18T14:00:00Z",
        "direction_id": 0,
        "id": "00000000-0000-0000-0000-000000000001",
        "short_name": "short_name of test trip 1",
        "stop_headsign": "stop_headsign of test stop time 2",
        "stop_sequence": 2,
    }
]

snapshots["test_routes_departures[filters5] 1"] = [
    {
        "arrival_time": "2021-02-18T13:15:00Z",
        "departure_headsign": "headsign of test trip 2",
        "departure_time": "2021-02-18T13:15:00Z",
        "direction_id": 1,
        "id": "00000000-0000-0000-0000-000000000002",
        "short_name": "short_name of test trip 2",
        "stop_headsign": "stop_headsign of test stop time 2",
        "stop_sequence": 1,
    }
]

snapshots["test_routes_departures[filters5] 2"] = [
    {
        "arrival_time": "2021-02-18T14:15:00Z",
        "departure_headsign": "headsign of test trip 2",
        "departure_time": "2021-02-18T14:15:00Z",
        "direction_id": 1,
        "id": "00000000-0000-0000-0000-000000000002",
        "short_name": "short_name of test trip 2",
        "stop_headsign": "stop_headsign of test stop time 3",
        "stop_sequence": 2,
    }
]

snapshots["test_routes_departures[filters6] 1"] = []

snapshots["test_routes_departures[filters6] 2"] = []