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
    assert "Locations" in response.text
    assert "Home vs Away" in response.text
    assert "Recordings by State" in response.text


def test_locations_shows_heatmap(client: FlaskClient) -> None:
    """Testing locations.all_locations_shows_heatmap."""
    response: TestResponse = client.get("/locations/all-locations-shows-heatmap")
    assert response.status_code == 200
    assert "All Locations Shows Heatmap" in response.text
    assert "plotly" in response.text


def test_away_shows_heatmap(client: FlaskClient) -> None:
    """Testing locations.away_shows_heatmap."""
    response: TestResponse = client.get("/locations/away-shows-heatmap")
    assert response.status_code == 200
    assert "Away Shows Heatmap" in response.text
    assert "plotly" in response.text


def test_home_shows_heatmap(client: FlaskClient) -> None:
    """Testing locations.home_shows_heatmap."""
    response: TestResponse = client.get("/locations/home-shows-heatmap")
    assert response.status_code == 200
    assert "Home Shows Heatmap" in response.text
    assert "plotly" in response.text


def test_home_remote_studios_shows_heatmap(client: FlaskClient) -> None:
    """Testing locations.home_remote_studios_shows_heatmap."""
    response: TestResponse = client.get("/locations/home-remote-studios-shows-heatmap")
    assert response.status_code == 200
    assert "Home/Remote Studios Shows Heatmap" in response.text
    assert "plotly" in response.text


def test_home_vs_away(client: FlaskClient) -> None:
    """Testing locations.home_vs_away."""
    response: TestResponse = client.get("/locations/home-vs-away")
    assert response.status_code == 200
    assert "Home vs Away" in response.text
    assert "Studios" in response.text


def test_recordings_by_state(client: FlaskClient) -> None:
    """Testing locations.recordings_by_state."""
    response: TestResponse = client.get("/locations/recordings-by-state")
    assert response.status_code == 200
    assert "Recordings by State" in response.text
    assert "choropleth" in response.text


def test_show_location_types(client: FlaskClient) -> None:
    """Testing locations.show_location_types."""
    response: TestResponse = client.get("/locations/show-location-types-by-year")
    assert response.status_code == 200
    assert "Show Location Types by Year" in response.text


@pytest.mark.parametrize("year", [2006, 2020, 2025])
def test_show_location_types_by_year(client: FlaskClient, year: int) -> None:
    """Testing locations.show_location_types_by_year."""
    response: TestResponse = client.get(
        f"/locations/show-location-types-by-year/{year}"
    )
    assert response.status_code == 200
    assert "Show Location Types by Year" in response.text
    assert "Home/Remote Studios" in response.text
    assert "plotly" in response.text
