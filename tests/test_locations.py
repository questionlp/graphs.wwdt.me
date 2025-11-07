# Copyright (c) 2018-2025 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Locations Module and Blueprint Views."""

from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing locations.index."""
    response: TestResponse = client.get("/locations/")
    assert response.status_code == 200
    assert b"Locations" in response.data
    assert b"Home vs Away" in response.data
    assert b"Recordings by State" in response.data


def test_home_vs_away(client: FlaskClient) -> None:
    """Testing locations.home_vs_away."""
    response: TestResponse = client.get("/locations/home-vs-away")
    assert response.status_code == 200
    assert b"Home vs Away" in response.data
    assert b"Studios" in response.data


def test_recordings_by_state(client: FlaskClient) -> None:
    """Testing locations.recordings_by_state."""
    response: TestResponse = client.get("/locations/recordings-by-state")
    assert response.status_code == 200
    assert b"Recordings by State" in response.data
    assert b"choropleth" in response.data
