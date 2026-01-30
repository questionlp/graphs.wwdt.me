# Copyright (c) 2018-2026 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Locations Module and Blueprint Views."""

import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing locations.index."""
    response: TestResponse = client.get("/locations/")
    assert response.status_code == 200
    assert b"Locations" in response.data
    assert b"Home vs Away" in response.data
    assert b"Recordings by State" in response.data


def test_all_locations_shows_heatmap(client: FlaskClient) -> None:
    """Testing locations.all_locations_shows_heatmap."""
    response: TestResponse = client.get("/locations/all-locations-shows-heatmap")
    assert response.status_code == 200
    assert b"All Locations Shows Heatmap" in response.data
    assert b"plotly" in response.data


def test_away_shows_heatmap(client: FlaskClient) -> None:
    """Testing locations.away_shows_heatmap."""
    response: TestResponse = client.get("/locations/away-shows-heatmap")
    assert response.status_code == 200
    assert b"Away Shows Heatmap" in response.data
    assert b"plotly" in response.data


def test_home_shows_heatmap(client: FlaskClient) -> None:
    """Testing locations.home_shows_heatmap."""
    response: TestResponse = client.get("/locations/home-shows-heatmap")
    assert response.status_code == 200
    assert b"Home Shows Heatmap" in response.data
    assert b"plotly" in response.data


def test_home_remote_studios_shows_heatmap(client: FlaskClient) -> None:
    """Testing locations.home_remote_studios_shows_heatmap."""
    response: TestResponse = client.get("/locations/home-remote-studios-shows-heatmap")
    assert response.status_code == 200
    assert b"Home/Remote Studios Shows Heatmap" in response.data
    assert b"plotly" in response.data


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


def test_show_location_types(client: FlaskClient) -> None:
    """Testing locations.show_location_types."""
    response: TestResponse = client.get("/locations/show-location-types-by-year")
    assert response.status_code == 200
    assert b"Show Location Types by Year" in response.data


@pytest.mark.parametrize("year", [2006, 2020, 2025])
def test_show_location_types_by_year(client: FlaskClient, year: int) -> None:
    """Testing locations.show_location_types_by_year."""
    response: TestResponse = client.get(
        f"/locations/show-location-types-by-year/{year}"
    )
    assert response.status_code == 200
    assert b"Show Location Types by Year" in response.data
    assert b"Home/Remote Studios" in response.data
    assert b"plotly" in response.data
