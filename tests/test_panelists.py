# Copyright (c) 2018-2026 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Panelists Module and Blueprint Views."""

import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing panelists.index."""
    response: TestResponse = client.get("/panelists/")
    assert response.status_code == 200
    assert b"Panelists" in response.data
    assert b"Aggregate Scores" in response.data
    assert b"Score Breakdown" in response.data


def test_aggregate_scores(client: FlaskClient) -> None:
    """Testing panelists.aggregate_scores."""
    response: TestResponse = client.get("/panelists/aggregate-scores")
    assert response.status_code == 200
    assert b"Panelists" in response.data
    assert b"Aggregate Scores" in response.data
    assert b"Aggregate Scores Breakdown" in response.data


def test_appearances_by_year(client: FlaskClient) -> None:
    """Testing panelists.appearances_by_year."""
    response: TestResponse = client.get("/panelists/appearances-by-year")
    assert response.status_code == 200
    assert b"Panelists" in response.data
    assert b"Appearances by Year" in response.data


@pytest.mark.parametrize("panelist_slug", ["adam-felber", "faith-salie"])
def test_appearances_by_year_details(client: FlaskClient, panelist_slug: str) -> None:
    """Testing main.appearances_by_year."""
    response: TestResponse = client.get(
        f"/panelists/appearances-by-year/{panelist_slug}"
    )
    assert response.status_code == 200
    assert b"Panelists" in response.data
    assert b"Appearances by Year:" in response.data


def test_score_breakdown(client: FlaskClient) -> None:
    """Testing panelists.score_breakdown."""
    response: TestResponse = client.get("/panelists/score-breakdown")
    assert response.status_code == 200
    assert b"Panelists" in response.data
    assert b"Score Breakdown" in response.data


@pytest.mark.parametrize("panelist_slug", ["adam-felber", "faith-salie"])
def test_score_breakdown_details(client: FlaskClient, panelist_slug: str) -> None:
    """Testing panelists.score_breakdown."""
    response: TestResponse = client.get(f"/panelists/score-breakdown/{panelist_slug}")
    assert response.status_code == 200
    assert b"Panelists" in response.data
    assert b"Score Breakdown:" in response.data


def test_scores_by_appearance(client: FlaskClient) -> None:
    """Testing panelists.scores_by_appearance."""
    response: TestResponse = client.get("/panelists/scores-by-appearance")
    assert response.status_code == 200
    assert b"Panelists" in response.data
    assert b"Scores by Appearance" in response.data


@pytest.mark.parametrize("panelist_slug", ["adam-felber", "faith-salie"])
def test_scores_by_appearance_details(client: FlaskClient, panelist_slug: str) -> None:
    """Testing panelists.scores_by_appearance."""
    response: TestResponse = client.get(
        f"/panelists/scores-by-appearance/{panelist_slug}"
    )
    assert response.status_code == 200
    assert b"Panelists" in response.data
    assert b"Scores by Appearance:" in response.data
