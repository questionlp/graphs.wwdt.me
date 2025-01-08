# Copyright (c) 2018-2025 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Panelists Routes for Wait Wait Graphs Site."""
import json

from flask import Blueprint, Response, current_app, render_template, url_for
from mysql.connector import connect
from slugify import slugify
from wwdtm.panelist import (
    Panelist,
    PanelistAppearances,
    PanelistDecimalScores,
    PanelistScores,
)

from app.reports.panel import aggregate_scores as agg
from app.utility import redirect_url

blueprint = Blueprint("panelists", __name__, template_folder="templates")


@blueprint.route("/")
def index() -> str:
    """View: Panelists Index."""
    return render_template("panelists/index.html")


@blueprint.route("/aggregate-scores")
def aggregate_scores() -> str:
    """View: Aggregate Scores."""
    _aggregate_scores = agg.retrieve_score_spread(
        use_decimal_scores=current_app.config["app_settings"]["use_decimal_scores"]
    )
    return render_template(
        "panelists/aggregate-scores/graph.html", aggregate_scores=_aggregate_scores
    )


@blueprint.route("/appearances-by-year")
def appearances_by_year() -> str:
    """View: Appearances by Year."""
    database_connection = connect(**current_app.config["database"])
    _panelist = Panelist(database_connection=database_connection)
    all_panelists = _panelist.retrieve_all()
    database_connection.close()
    return render_template(
        "panelists/appearances-by-year/index.html", panelists=all_panelists
    )


@blueprint.route("/appearances-by-year/<string:panelist>")
def appearances_by_year_details(panelist: str) -> Response | str:
    """View: Appearances by Year Details."""
    panelist_slug = slugify(panelist)
    if panelist and panelist != panelist_slug:
        return redirect_url(
            url_for("panelists.appearances_by_year_details", panelist=panelist_slug)
        )

    database_connection = connect(**current_app.config["database"])
    _panelist = Panelist(database_connection=database_connection)
    _appearances = PanelistAppearances(database_connection=database_connection)
    info = _panelist.retrieve_by_slug(panelist)

    if not info:
        return redirect_url(url_for("panelists.appearances_by_year"))

    appearances = _appearances.retrieve_yearly_appearances_by_slug(panelist)
    database_connection.close()

    years = list(appearances.keys())
    count = list(appearances.values())

    return render_template(
        "panelists/appearances-by-year/details.html",
        info=info,
        years=years,
        count=count,
    )


@blueprint.route("/score-breakdown")
def score_breakdown() -> str:
    """View: Score Breakdown."""
    database_connection = connect(**current_app.config["database"])
    _panelist = Panelist(database_connection=database_connection)
    panelists = _panelist.retrieve_all()
    database_connection.close()
    return render_template("panelists/score-breakdown/index.html", panelists=panelists)


@blueprint.route("/score-breakdown/<string:panelist>")
def score_breakdown_details(panelist: str) -> Response | str:
    """View: Score Breakdown Details."""
    panelist_slug = slugify(panelist)
    if panelist and panelist != panelist_slug:
        return redirect_url(
            url_for("panelists.score_breakdown_details", panelist=panelist_slug)
        )

    database_connection = connect(**current_app.config["database"])
    _panelist = Panelist(database_connection=database_connection)
    info = _panelist.retrieve_by_slug(panelist)

    if not info:
        return redirect_url(url_for("panelists.score_breakdown"))

    if current_app.config["app_settings"]["use_decimal_scores"]:
        _panelist_scores = PanelistDecimalScores(
            database_connection=database_connection
        )
        scores = _panelist_scores.retrieve_scores_grouped_list_by_slug(panelist)
    else:
        _panelist_scores = PanelistScores(database_connection=database_connection)
        scores = _panelist_scores.retrieve_scores_grouped_list_by_slug(panelist)

    database_connection.close()

    return render_template(
        "panelists/score-breakdown/details.html",
        info=info,
        scores=scores,
    )


@blueprint.route("/scores-by-appearance")
def scores_by_appearance() -> str:
    """View: Scores by Appearances."""
    database_connection = connect(**current_app.config["database"])
    _panelist = Panelist(database_connection=database_connection)
    panelists = _panelist.retrieve_all()
    database_connection.close()
    return render_template(
        "panelists/scores-by-appearance/index.html", panelists=panelists
    )


@blueprint.route("/scores-by-appearance/<string:panelist>")
def scores_by_appearance_details(panelist: str) -> Response | str:
    """View: Scores by Appearances."""
    panelist_slug = slugify(panelist)
    if panelist and panelist != panelist_slug:
        return redirect_url(
            url_for("panelists.scores_by_appearance_details", panelist=panelist_slug)
        )

    database_connection = connect(**current_app.config["database"])
    _panelist = Panelist(database_connection=database_connection)
    info = _panelist.retrieve_by_slug(panelist)

    if current_app.config["app_settings"]["use_decimal_scores"]:
        _panelist_scores = PanelistDecimalScores(
            database_connection=database_connection
        )
        scores = _panelist_scores.retrieve_scores_list_by_slug(panelist)
    else:
        _panelist_scores = PanelistScores(database_connection=database_connection)
        scores = _panelist_scores.retrieve_scores_list_by_slug(panelist)

    database_connection.close()

    if not info:
        return redirect_url(url_for("panelists.scores_by_appearance"))

    if scores:
        shows_json = json.dumps(scores["shows"])
        if current_app.config["app_settings"]["use_decimal_scores"]:
            scores_float = []
            for score in scores["scores"]:
                scores_float.append(round(float(score), 5))
            scores_json = json.dumps(scores_float)
        else:
            scores_json = json.dumps(scores["scores"])

        return render_template(
            "panelists/scores-by-appearance/details.html",
            info=info,
            shows=shows_json,
            scores=scores_json,
        )

    return render_template(
        "panelists/scores-by-appearance/details.html",
        info=info,
        shows=None,
        scores=None,
    )
