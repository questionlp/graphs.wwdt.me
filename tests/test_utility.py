# Copyright (c) 2018-2025 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Utilities Modules."""

from datetime import datetime

import pytest

from app import utility

TEST_UMAMI_ANALYTICS: dict[str, str | bool] = {
    "enabled": True,
    "url": "https://analytics.example.org",
    "data_website_id": "1234567890",
    "data_domains": "example.org",
    "data_host_url": "example.org",
    "data_auto_track": True,
}


def test_format_umami_analytics() -> None:
    """Testing utility.format_umami_analytics."""
    _analytics: str = utility.format_umami_analytics(
        umami_analytics=TEST_UMAMI_ANALYTICS
    )
    assert _analytics
    assert "script" in _analytics
    assert TEST_UMAMI_ANALYTICS["url"] in _analytics
    assert TEST_UMAMI_ANALYTICS["data_website_id"] in _analytics


@pytest.mark.parametrize("date_string", ["2000-01-01", "1970-01-01"])
def test_date_string_to_date(date_string: str) -> None:
    """Testing utility.date_string_to_date."""
    _date: datetime = utility.date_string_to_date(date_string=date_string)
    assert _date
    assert isinstance(_date, datetime)


@pytest.mark.parametrize("time_zone", ["America/Chicago", "UTC"])
def test_time_zone_parser(time_zone: str) -> None:
    """Testing utility.time_zone_parser."""
    _time_zone_object, _time_zone_string = utility.time_zone_parser(time_zone=time_zone)
    assert _time_zone_object
    assert time_zone in _time_zone_string


@pytest.mark.parametrize("time_zone", ["Chicago/Illinois"])
def test_time_zone_parser_error(time_zone: str) -> None:
    """Testing utility.time_zone_parser with invalid time zone string."""
    _time_zone_object, _time_zone_string = utility.time_zone_parser(time_zone=time_zone)
    assert _time_zone_object
    assert "UTC" in _time_zone_string
