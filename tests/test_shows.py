# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2023 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
"""Testing Shows Module and Blueprint Views"""
from flask.testing import FlaskClient
import pytest
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing shows.index"""
    response: TestResponse = client.get("/shows/")
    assert response.status_code == 200
    assert b"Shows" in response.data
    assert b"All Scores" in response.data
    assert b"Counts by Year" in response.data


def test_all_scores(client: FlaskClient) -> None:
    """Testing shows.all_scores"""
    response: TestResponse = client.get("/shows/all-scores")
    assert response.status_code == 200
    assert b"Shows" in response.data
    assert b"All Scores" in response.data


@pytest.mark.parametrize("year", [2020])
def test_all_scores_by_year(client: FlaskClient, year: int) -> None:
    """Testing shows.all_scores_by_year"""
    response: TestResponse = client.get(f"/shows/all-scores/{year}")
    assert response.status_code == 200
    assert b"Shows" in response.data
    assert b"All Scores for" in response.data


def test_bluff_counts(client: FlaskClient) -> None:
    """Testing shows.bluff_counts"""
    response: TestResponse = client.get("/shows/bluff-counts")
    assert response.status_code == 200
    assert b"Shows" in response.data
    assert b"Bluff the Listener Counts" in response.data


def test_bluff_counts_all(client: FlaskClient) -> None:
    """Testing shows.bluff_counts_all"""
    response: TestResponse = client.get("/shows/bluff-counts/all")
    assert response.status_code == 200
    assert b"Shows" in response.data
    assert b"Bluff the Listener Counts by Year and Month" in response.data
    assert b"Correct" in response.data


@pytest.mark.parametrize("year", [2020])
def test_bluff_counts_by_year(client: FlaskClient, year: int) -> None:
    """Testing shows.bluff_counts_by_year"""
    response: TestResponse = client.get(f"/shows/bluff-counts/{year}")
    assert response.status_code == 200
    assert b"Shows" in response.data
    assert b"Bluff the Listener Counts for" in response.data
    assert b"Correct" in response.data


def test_counts_by_day_of_month(client: FlaskClient) -> None:
    """Testing shows.counts_by_day_of_month"""
    response: TestResponse = client.get("/shows/counts-by-day-month")
    assert response.status_code == 200
    assert b"Shows" in response.data
    assert b"Counts by Day of Month" in response.data


def test_counts_by_day_of_month_all(client: FlaskClient) -> None:
    """Testing shows.counts_by_day_of_month_all"""
    response: TestResponse = client.get("/shows/counts-by-day-month/all")
    assert response.status_code == 200
    assert b"Shows" in response.data
    assert b"Counts by Day of Month for All Months" in response.data
    assert b"Regular" in response.data


@pytest.mark.parametrize("month", [8])
def test_counts_by_day_of_month_by_month(client: FlaskClient, month: int) -> None:
    """Testing shows.counts_by_day_of_month_by_month"""
    response: TestResponse = client.get(f"/shows/counts-by-day-month/{month}")
    assert response.status_code == 200
    assert b"Shows" in response.data
    assert b"Counts by Day of Month for" in response.data
    assert b"Regular" in response.data


def test_counts_by_year(client) -> None:
    """Testing shows.counts_by_year"""
    response: TestResponse = client.get("/shows/counts-by-year")
    assert response.status_code == 200
    assert b"Shows" in response.data
    assert b"Counts by Year" in response.data
    assert b"Regular" in response.data


def test_monthly_aggregate_score_heatmap(client: FlaskClient) -> None:
    """Testing shows.monthly_aggregate_score_heatmap"""
    response: TestResponse = client.get("/shows/monthly-aggregate-score-heatmap")
    assert response.status_code == 200
    assert b"Shows" in response.data
    assert b"Monthly Aggregate Score Heatmap" in response.data
    assert b"Month" in response.data
    assert b"Year" in response.data


def test_monthly_average_score_heatmap(client: FlaskClient) -> None:
    """Testing shows.monthly_average_score_heatmap"""
    response: TestResponse = client.get("/shows/monthly-average-score-heatmap")
    assert response.status_code == 200
    assert b"Shows" in response.data
    assert b"Monthly Average Score Heatmap" in response.data
    assert b"Month" in response.data
    assert b"Year" in response.data


def test_panel_gender_mix(client: FlaskClient) -> None:
    """Testing shows.panel_gender_mix"""
    response: TestResponse = client.get("/shows/panel-gender-mix")
    assert response.status_code == 200
    assert b"Shows" in response.data
    assert b"Panel Gender Mix" in response.data
    assert b"2W / 1M" in response.data
    assert b"Year" in response.data
